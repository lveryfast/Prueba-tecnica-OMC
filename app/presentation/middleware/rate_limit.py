from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse


limiter = Limiter(key_func=get_remote_address)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": {
                "type": "rate_limit_exceeded",
                "detail": f"Has excedido el límite de requests. Intenta de nuevo en {exc.detail}"
            },
            "message": "Demasiadas solicitudes. Por favor espera antes de continuar.",
            "retry_after": getattr(exc, "retry_after", 60)
        }
    )


def register_rate_limiter(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)