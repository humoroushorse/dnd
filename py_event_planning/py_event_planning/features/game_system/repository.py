"""Game Session repository."""

from __future__ import annotations

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_event_planning.features.core.repository import RepositoryBase
from py_event_planning.features.game_system.models import GameSystem
from py_event_planning.features.game_system.schemas import (
    GameSystemCreate,
    GameSystemSchema,
    GameSystemSchemaBase,
    GameSystemUpdate,
)


class GameSystemRepository(
    RepositoryBase[GameSystem, GameSystemSchema, GameSystemSchemaBase, GameSystemCreate, GameSystemUpdate]
):
    """Game System Repository.

    Args:
        RepositoryBase (_type_): _description_
    """

    def __init__(self, session: AsyncSession, logger: loguru.Logger | None = None):
        super().__init__(session=session, model=GameSystem, schema=GameSystemSchema, schema_base=GameSystemSchemaBase)
        self.logger.trace("{} created!", self.__class__.__name__)
