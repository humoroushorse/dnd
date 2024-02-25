"""API dependencies."""

from typing import Generator

from app.dnd.database.session import SessionLocal


def get_db() -> Generator:
    """Get a database session."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
