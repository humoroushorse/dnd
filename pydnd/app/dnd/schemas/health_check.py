"""Schemas for /health."""
from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Model for /health."""

    name: str
    description: str
    version: str
    docs_url: str
