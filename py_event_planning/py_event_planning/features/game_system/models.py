"""SQLAlchemy Table: dnd_events definition."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_event_planning.database.base_class import EventPlanningSchemaBase
from py_event_planning.shared.models import MixinBookeeping

if TYPE_CHECKING:
    from py_event_planning.features.game_session.models import GameSession
else:
    GameSession = "GameSession"


class GameSystem(MixinBookeeping, EventPlanningSchemaBase):
    """SQLAlchemy game_system model."""

    __tablename__ = "game_system"

    # keys
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    # relationships
    #    game_session(n) : game_system(1)
    game_sessions: Mapped[list[GameSession]] = relationship("GameSession", back_populates="game_system")
    # fields
    name: Mapped[str] = mapped_column(nullable=False)
    version: Mapped[str] = mapped_column(nullable=False)
    release_year: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    __table_args__: tuple | dict = (
        UniqueConstraint("name", "version", "release_year"),
        EventPlanningSchemaBase.__table_args__,  # this dict has to be last (dev time lost 30 minutes)
    )
