from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENV: Literal["development", "testing", "production"] = "development"    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 48001

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Boilerplate"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = """
    FastAPI boilerplate with the best developer experience.
    
    ## Features
    
    * **FastAPI** - Modern, fast web framework for building APIs
    * **SQLAlchemy** - SQL toolkit and ORM
    * **Alembic** - Database migrations
    * **Pydantic** - Data validation
    * **JWT** - Authentication
    * **pytest** - Testing
    """
      # CORS
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000", "http://localhost:48001"])
      # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # Security
    SECRET_KEY: str = "d82e94136952152c89239dc6f9b27d746dc56d7e7714ab53f282b71ddc8ff2cf"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Environment specific settings
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str, info) -> str:
        """Make SQLite URLs work with async SQLAlchemy."""
        if v.startswith("sqlite:///"):
            return v.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()


settings = get_settings()
