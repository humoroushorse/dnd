"""SQLAlchemy Table: dnd_events definition."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_event_planning.database.base_class import EventPlanningSchemaBase
from py_event_planning.shared.enums import DbSchemaEnum
from py_event_planning.shared.models import MixinBookeeping

if TYPE_CHECKING:
    from py_event_planning.features.game_system.models import GameSystem
    from py_event_planning.features.jt_user_game_session.models import JtUserGameSession
    from py_event_planning.features.user.models import User
else:
    GameSystem = "GameSystem"
    JtUserGameSession = "JtUserGameSession"
    User = "User"


class GameSession(MixinBookeeping, EventPlanningSchemaBase):
    """SQLAlchemy game_session model."""

    __tablename__ = "game_session"

    # keys
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    # relationships
    #    game_session(n) : game_system(1)
    game_system_id: Mapped[str] = mapped_column(ForeignKey(f"{DbSchemaEnum.EVENT_PLANNING.value}.game_system.id"))
    game_system: Mapped[GameSystem] = relationship("GameSystem", back_populates="game_sessions")
    #    game_session(1) : jt_user_game_session(1)
    jt_user_game_session: Mapped[JtUserGameSession] = relationship("JtUserGameSession", back_populates="game_session")
    game_master_id: Mapped[str] = mapped_column(ForeignKey(f"{DbSchemaEnum.EVENT_PLANNING.value}.user.id"))
    game_master: Mapped[User] = relationship()
    # fields
    # game_master: Mapped[str] = mapped_column(nullable=False) # ik- remove
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    max_players: Mapped[int | None] = mapped_column(nullable=True)
    image_url: Mapped[str | None] = mapped_column(nullable=True)
    image_url_description: Mapped[str | None] = mapped_column(nullable=True)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    # constraints
