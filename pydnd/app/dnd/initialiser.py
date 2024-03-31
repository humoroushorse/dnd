"""API initalization steps."""

from dnd.database.initialise import initialise
from dnd.database.session import SessionLocal


def init() -> None:
    """Initialise database."""
    db = SessionLocal()
    initialise(db)


def main() -> None:
    """Initialise steps for API."""
    init()


if __name__ == "__main__":
    main()
