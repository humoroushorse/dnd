"""App configuration file."""
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    """API settings and environment variables."""

    PROJECT_NAME: str = "Dungeons & Dragons FastAPI"
    DESCRIPTION: str = "Personal project for DnD"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "postgresql://localhost/postgres"
    SQLALCHEMY_TESTING_DATABASE_URI: str = "postgresql://postgres:admin@localhost:5433"

    class Config:
        """BaseSettings Config overrides."""

        env_file = ".env"


settings = Settings()
