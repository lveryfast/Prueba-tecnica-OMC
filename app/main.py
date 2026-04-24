from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.infrastructure.database.connection import engine, Base
from app.presentation.routes.leads import router as leads_router
from app.presentation.handlers.exceptions import register_exception_handlers
from app.presentation.middleware.rate_limit import register_rate_limiter
from app.presentation.middleware.logging import setup_logging, get_logger


# Initialize structured logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application", extra={"event": "app_start"})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Shutting down application", extra={"event": "app_shutdown"})


app = FastAPI(
    title="Lead Management API",
    version="1.0.0",
    description="API REST para gestión de leads con análisis de IA",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

register_exception_handlers(app)
register_rate_limiter(app)

app.include_router(leads_router, prefix="/api")


@app.get("/health")
async def health():
    try:
        async with engine.connect() as conn:
            logger.info("Health check successful")
            return JSONResponse({
                "status": "healthy",
                "database": "connected",
                "version": settings.APP_NAME
            })
    except Exception as e:
        logger.error("Health check failed", extra={"error": str(e)})
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )


@app.get("/")
async def root():
    return {
        "message": "Lead Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }