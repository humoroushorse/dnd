"""Game Session repository."""

from __future__ import annotations

import loguru
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from py_event_planning.database.exceptions import handle_sqlalchemy_errors_decorator
from py_event_planning.features.core.repository import RepositoryBase
from py_event_planning.features.game_session.models import GameSession
from py_event_planning.features.game_session.schemas import (
    GameSessionCreate,
    GameSessionSchema,
    GameSessionSchemaBase,
    GameSessionUpdate,
)
from py_event_planning.features.jt_user_game_session.models import JtUserGameSession
from py_event_planning.features.user.models import User


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

    @handle_sqlalchemy_errors_decorator
    async def read_multi_full(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[GameSessionSchema]:
        # ) -> AsyncIterator[ModelType]:
        """Get multiple entities (pagination optional).

        Args:
            offset (int, optional): _description_. Defaults to 0.
            limit (int, optional): _description_. Defaults to 100.

        Returns:
            AsyncIterator[ModelType]: _description_

        Yields:
            Iterator[AsyncIterator[ModelType]]: _description_
        """
        self.logger.debug("RepositoryBase::read_multi() called with offset={}, limit={}", offset, limit)
        stmt = select(self.model)
        stmt = stmt.options(selectinload(self.model.jt_user_game_session).selectinload(JtUserGameSession.user))
        stmt = stmt.join(JtUserGameSession, JtUserGameSession.game_session_id == self.model.id, isouter=True).join(
            User, User.id == JtUserGameSession.user_id, isouter=True
        )
        stmt = stmt.offset(offset)
        stmt = stmt.limit(limit)
        res = await self.session.scalars(stmt.order_by(self.model.id))
        return [GameSessionSchema.model_validate(e) for e in res]

    @handle_sqlalchemy_errors_decorator
    async def read_by_id_full(
        self,
        entity_id: int,
    ) -> GameSessionSchema | None:
        """Get an entity by id.

        Args:
            entity_id (int): _description_

        Returns:
            ModelSchemaType | None: _description_
        """
        stmt = select(self.model)
        stmt = stmt.options(selectinload(self.model.jt_user_game_session).selectinload(JtUserGameSession.user))
        stmt = stmt.join(JtUserGameSession, JtUserGameSession.game_session_id == self.model.id, isouter=True).join(
            User, User.id == JtUserGameSession.user_id, isouter=True
        )
        stmt = stmt.where(self.model.id == entity_id)
        model = await self.session.scalar(stmt.order_by(self.model.id))
        schema = GameSessionSchema.model_validate(model)
        return schema
