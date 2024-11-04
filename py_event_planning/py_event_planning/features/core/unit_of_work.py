"""Unit of Work (uow) classes and funcitons."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_event_planning.features.game_session.repository import GameSessionRepository
from py_event_planning.features.game_system.repository import GameSystemRepository
from py_event_planning.features.jt_user_game_session.repository import (
    JtUserGameSystemRepository,
)
from py_event_planning.features.user.repository import UserRepository


class SqlAlchemyUnitOfWork:
    """SQLAlchemy Unit of Work (UOW)."""

    def __init__(self, db_session: AsyncSession, logger: loguru.Logger | None = None):
        self.db_session = db_session
        self.logger = logger if logger else loguru.logger
        self.game_session_repo = GameSessionRepository(db_session)
        self.game_system_repo = GameSystemRepository(db_session)
        self.user_repo = UserRepository(db_session)
        self.jt_user_game_system_repo = JtUserGameSystemRepository(db_session)
        self.logger.trace("{} created!", self.__class__.__name__)

    async def __aenter__(self) -> SqlAlchemyUnitOfWork:
        """Context enter (async)."""
        return self

    async def __aexit__(self, exc_type: str, exc_value: str, traceback: str) -> None:
        """Context exit (async)."""
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.db_session.close()

    async def commit(self) -> None:
        """Commit transaction."""
        await self.db_session.commit()

    async def rollback(self) -> None:
        """Rollback transaction."""
        await self.db_session.rollback()


@asynccontextmanager
async def sqlalchemy_uow(
    db_session: AsyncSession, logger: loguru.Logger | None = None
) -> AsyncGenerator[SqlAlchemyUnitOfWork]:
    """A SQLAlchemy Unit of Work (UOW) Context Manager.

    Args:
        db_session (AsyncSession): database session (async)
        logger (loguru.Logger | None, optional): logger uow will use, uses loguru,logger if None. Defaults to None.

    Returns:
        AsyncGenerator[SqlAlchemyUnitOfWork]: _description_

    Yields:
        Iterator[AsyncGenerator[SqlAlchemyUnitOfWork]]: _description_
    """
    uow = SqlAlchemyUnitOfWork(db_session=db_session, logger=logger)
    try:
        yield uow
    finally:
        await uow.db_session.close()
