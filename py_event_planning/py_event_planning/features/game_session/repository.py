"""Game Session repository."""

from __future__ import annotations

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_event_planning.features.core.repository import RepositoryBase
from py_event_planning.features.game_session.models import GameSession
from py_event_planning.features.game_session.schemas import (
    GameSessionCreate,
    GameSessionSchema,
    GameSessionSchemaBase,
    GameSessionUpdate,
)


class GameSessionRepository(
    RepositoryBase[GameSession, GameSessionSchema, GameSessionSchemaBase, GameSessionCreate, GameSessionUpdate]
):
    """Game Session Repository.

    Args:
        RepositoryBase (_type_): _description_
    """

    def __init__(self, session: AsyncSession, logger: loguru.Logger | None = None):
        super().__init__(
            session=session, model=GameSession, schema=GameSessionSchema, schema_base=GameSessionSchemaBase
        )
        self.logger.trace("{} created!", self.__class__.__name__)
