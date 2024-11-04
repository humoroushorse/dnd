"""Join Table User/GameSystem repository."""

from __future__ import annotations

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_event_planning.features.core.repository import RepositoryBase
from py_event_planning.features.jt_user_game_session.models import JtUserGameSession
from py_event_planning.features.jt_user_game_session.schemas import (
    JtUserGameSessionCreate,
    JtUserGameSessionSchema,
    JtUserGameSessionSchemaBase,
    JtUserGameSessionUpdate,
)


class JtUserGameSystemRepository(
    RepositoryBase[
        JtUserGameSession,
        JtUserGameSessionSchema,
        JtUserGameSessionSchemaBase,
        JtUserGameSessionCreate,
        JtUserGameSessionUpdate,
    ]
):
    """Join Table User/GameSystem Repository.

    Args:
        RepositoryBase (_type_): _description_
    """

    def __init__(self, session: AsyncSession, logger: loguru.Logger | None = None):
        super().__init__(
            session=session,
            model=JtUserGameSession,
            schema=JtUserGameSessionSchema,
            schema_base=JtUserGameSessionSchemaBase,
        )
        self.logger.trace("{} created!", self.__class__.__name__)
