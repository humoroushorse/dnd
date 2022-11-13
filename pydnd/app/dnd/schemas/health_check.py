"""Schemas for /health."""
from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Model for /health."""

    name: str
    version: str
    description: str
