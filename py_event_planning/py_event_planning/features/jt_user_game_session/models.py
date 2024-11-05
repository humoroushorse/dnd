"""SQLAlchemy Table: dnd_events definition."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_event_planning.database.base_class import EventPlanningSchemaBase
from py_event_planning.shared.enums import DbSchemaEnum
from py_event_planning.shared.models import MixinBookeeping

if TYPE_CHECKING:
    from py_event_planning.features.game_session.models import GameSession
    from py_event_planning.features.user.models import User
else:
    User = "User"
    GameSession = "GameSession"


class JtUserGameSession(MixinBookeeping, EventPlanningSchemaBase):
    """SQLAlchemy game_session_user join table model."""

    __tablename__ = "jt_user_game_session"

    # keys
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    # Relationships
    #    user(n) : jt_user_game_session(1)
    user_id: Mapped[str] = mapped_column(ForeignKey(f"{DbSchemaEnum.EVENT_PLANNING.value}.user.id"))
    user: Mapped[User] = relationship("User", lazy="selectin")
    #    game_session(1) : jt_user_game_session(1)
    game_session_id: Mapped[str] = mapped_column(ForeignKey(f"{DbSchemaEnum.EVENT_PLANNING.value}.game_session.id"))
    game_session: Mapped[GameSession] = relationship("GameSession", back_populates="jt_user_game_session")
