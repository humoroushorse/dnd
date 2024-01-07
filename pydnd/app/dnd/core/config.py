"""App configuration file."""
# import secrets
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """API settings and environment variables."""

    PROJECT_NAME: Optional[str] = "Dungeons & Dragons FastAPI"
    DESCRIPTION: Optional[str] = "Personal project for DnD"
    VERSION: Optional[str] = "0.1.0"
    API_V1_STR: Optional[str] = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: Optional[str] = "ostgresql://postgres:admin@localhost:5432"
    SQLALCHEMY_TESTING_DATABASE_URI: Optional[
        str
    ] = "postgresql://postgres:admin@localhost:5433"
    LOG_LEVEL: Optional[str] = "INFO"
    HOST: Optional[str] = "0.0.0.0"
    PORT: Optional[int] = 8001

    class Config:
        """BaseSettings Config overrides."""

        env_file = ".env"


uncached_settings = Settings()
