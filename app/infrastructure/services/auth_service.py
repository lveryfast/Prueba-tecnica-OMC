from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings
from app.presentation.middleware.logging import get_logger

logger = get_logger(__name__)


class AuthService:
    def create_access_token(self, email: str, rol: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": email, "rol": rol, "exp": expire}
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except JWTError as e:
            logger.warning("JWT token verification failed", extra={"error": str(e)})
            return None