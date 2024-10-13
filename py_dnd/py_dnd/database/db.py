"""Database."""

from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .session import sessionmanager

# TODO: ik-remove doc link https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html

# ik-todo remove doc link https://dev.to/akarshan/asynchronous-database-sessions-in-fastapi-with-sqlalchemy-1o7e

# async def get_session() -> AsyncIterator[AsyncSession]:
#     """Get databaase session instance.

#     Raises:
#         Exception: _description_

#     Returns:
#         AsyncIterator[AsyncSession]: an async db session

#     Yields:
#         Iterator[AsyncIterator[AsyncSession]]: an async session

#     Usage:
#         session: AsyncSession = Depends(get_db)

#     Example Usage:
#         async def delete_spells(spell_ids: list[int]):
#             async for db_session in get_db():
#                 async with db_session as session:
#                     await delete_spells_batch(session, spell_ids)
#     """
#     session = sessionmanager.session()
#     if session is None:
#         raise Exception("DatabaseSessionManager is not initialized")
#     try:
#         # Setting the search path and yielding the session...
#         await session.execute(
#             text(f"SET search_path TO {enums.DbSchemaEnum.DND.value}")
#         )
#         yield session
#     except Exception:
#         await session.rollback()
#         raise
#     finally:
#         # Closing the session after use...
#         await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session (async)."""
    async with sessionmanager.session() as session:
        yield session


AsyncSessionDependency = Annotated[async_sessionmaker, Depends(get_db)]
