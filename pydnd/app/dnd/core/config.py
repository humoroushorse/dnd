"""App configuration file."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """API settings and environment variables."""

    PROJECT_NAME: str | None = "Dungeons & Dragons FastAPI"
    DESCRIPTION: str | None = "Personal project for DnD"
    VERSION: str | None = "0.1.0"
    API_V1_STR: str | None = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    POSTGRES_DATABASE_URI: str | None = "postgresql://postgres:admin@localhost:5432/ttrpg-pg"
    POSTGRES_TESTING_DATABASE_URI: str | None = "postgresql://postgres:admin@localhost:5433/ttrpg-pg"
    LOG_LEVEL: str | None = "INFO"
    HOST: str | None = "0.0.0.0"
    PORT: int | None = 8001

    class Config:
        """BaseSettings Config overrides."""

        env_file = ".env"


uncached_settings = Settings()
