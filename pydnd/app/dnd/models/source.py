"""SQLAlchemy Table: source definition."""

from dnd.database.base_class import DbBase
from sqlalchemy.orm import Mapped, mapped_column


class Source(DbBase):
    """SQLAlchemy source model."""

    # keys
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # fields
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(nullable=False, unique=True)
