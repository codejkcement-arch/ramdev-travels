from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Ramdev Travels"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite+aiosqlite:///./ramdev.db"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    CORS_ORIGIN_REGEX: str | None = None
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""
    ADMIN_EMAIL: str = ""
    ADMIN_PASSWORD: str = ""
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    AUTO_CREATE_TABLES: bool = False
    BOOKING_HOLD_MINUTES: int = 15
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

if settings.ENVIRONMENT.lower() == "production":
    if len(settings.SECRET_KEY) < 32:
        raise RuntimeError("SECRET_KEY must be at least 32 characters in production")
    if settings.AUTO_CREATE_TABLES:
        raise RuntimeError("AUTO_CREATE_TABLES must be false in production; run Alembic migrations")
