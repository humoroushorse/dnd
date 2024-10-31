"""SQLAlchemy Table: dnd_events definition."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_event_planning.database.base_class import EventPlanningSchemaBase
from py_event_planning.shared.models import MixinBookeeping

if TYPE_CHECKING:
    from py_event_planning.features.game_session.models import GameSession
    from py_event_planning.features.jt_user_game_session.models import JtUserGameSession
else:
    GameSession = "GameSession"


class User(MixinBookeeping, EventPlanningSchemaBase):
    """SQLAlchemy user model."""

    __tablename__ = "user"

    # keys
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    # relationships
    #   user(n) : jt_user_game_session(1)
    jt_user_game_session: Mapped[list[JtUserGameSession]] = relationship("JtUserGameSession")
    # fields
    username: Mapped[str] = mapped_column(nullable=False)
    # game_sesions_as_game_master: Mapped[list["GameSession"]] = relationship(back_populates="game_master")
    profile_picture_url: Mapped[str | None] = mapped_column(default=None, nullable=True)
