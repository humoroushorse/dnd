"""Database."""

from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .session import sessionmanager


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session (async)."""
    async with sessionmanager.session() as session:
        yield session


AsyncSessionDependency = Annotated[async_sessionmaker, Depends(get_db)]
