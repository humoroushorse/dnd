"""SQLAlchemy Table: user definition."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from py_dnd.database.base_class import DndSchemaBase

if TYPE_CHECKING:
    pass
else:
    pass


class User(DndSchemaBase):
    """SQLAlchemy user model."""

    __tablename__ = "user"

    # keys
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    # relationships
    # fields
    username: Mapped[str | None] = mapped_column(default=None, nullable=True)
    profile_picture_url: Mapped[str | None] = mapped_column(default=None, nullable=True)
