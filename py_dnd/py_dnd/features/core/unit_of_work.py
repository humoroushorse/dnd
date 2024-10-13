"""Unit of Work (uow) classes and funcitons."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_dnd.features.sources.repository import SourceRepository

# from py_dnd.features import spells
from py_dnd.features.spells.repository import SpellRepository


class SqlAlchemyUnitOfWork:
    """SQLAlchemy Unit of Work (UOW)."""

    def __init__(self, db_session: AsyncSession, logger: loguru.Logger | None = None):
        self.db_session = db_session
        self.logger = logger if logger else loguru.logger
        self.spell_repo = SpellRepository(db_session)
        self.source_repo = SourceRepository(db_session)
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
