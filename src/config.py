from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field
from typing import Annotated


class Settings(BaseSettings):
    """Глобальные настройки приложения."""

    # Database
    DATABASE_URL: Annotated[PostgresDsn, Field(description="URL подключения к PostgreSQL")]

    # Application
    APP_ENV: str = "development"
    DEBUG: bool = False
    JWT_SECRET_KEY: str = Field(..., description="Секретный ключ для JWT токенов")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ISSUER: str = "stock_simulator_api"
    JWT_AUDIENCE: str = "frontend_app"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore",  # Игнорировать лишние переменные из .env
    }


settings = Settings()