"""API initalization steps."""

from app.dnd.database.initialise import initialise
from app.dnd.database.session import SessionLocal


def init() -> None:
    """Initialise database."""
    db = SessionLocal()
    initialise(db)


def main() -> None:
    """Initialise steps for API."""
    init()


if __name__ == "__main__":
    main()
