"""Message class for returning a string from an API endpoint."""
from pydantic import BaseModel


class Message(BaseModel):
    """Response message."""

    message: str
