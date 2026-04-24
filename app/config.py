from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Lead Management API"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/leads_db"
    JWT_SECRET_KEY: str = "change-this-secret-key-min-32-characters"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"


settings = Settings()