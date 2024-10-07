"""SQLAlchemy Table: source definition."""

from sqlalchemy.orm import Mapped, mapped_column

from py_dnd.database.base_class import DndSchemaBase
from py_dnd.shared.models import MixinBookeeping


class Source(MixinBookeeping, DndSchemaBase):
    """SQLAlchemy source model."""

    # keys
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    # fields
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    name_short: Mapped[str] = mapped_column(nullable=False, unique=True)
    dnd_version: Mapped[str] = mapped_column(nullable=False)
    dnd_version_year: Mapped[int] = mapped_column(default=None)
    publish_year: Mapped[int | None] = mapped_column(default=None)
