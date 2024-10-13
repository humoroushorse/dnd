"""Schemas that only apply to core features (non-shared)."""

from pydantic import BaseModel, Field


class AppBaseRouteSchema(BaseModel):
    """Model for /health."""

    name: str | None = Field(default=None, description="API Name")
    description: str | None = Field(default=None, description="API Description")
    version: str | None = Field(default=None, description="API Version")
    swagger_url: str | None = Field(default=None, description="API Swagger Docs URL")
    redoc_url: str | None = Field(default=None, description="API ReDoc URL")
    python_version: str | None = Field(default=None, description="API Python Version")
