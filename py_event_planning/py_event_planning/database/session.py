"""A sqlalchemy.orm Session."""

import contextlib
from typing import AsyncIterator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from py_event_planning.database.base_class import EventPlanningSchemaBase

# ik-todo remove doc link https://dev.to/akarshan/asynchronous-database-sessions-in-fastapi-with-sqlalchemy-1o7e


class DatabaseSessionManager:
    """Database session manager (async)."""

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        # self.session = None

    def init(self, host: str) -> None:
        """Class startup connections.

        Args:
            host (str): database connection string.
        """
        # Database connection parameters...

        # Creating an asynchronous engine
        self.engine = create_async_engine(host, pool_size=100, max_overflow=0, pool_pre_ping=False)
        # TODO: look at pool_pre_ping=True (I think this is a sqllite thing)

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(autocommit=False, autoflush=False, future=True, bind=self.engine)

        # Creating a scoped session
        # self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

        logger.debug("DatabaseSessionManager initialized!")

    async def close(self) -> None:
        """Close database connection.

        Raises:
            Exception: generic exception handling
        """
        # Closing the database session...
        if self.engine is None:
            raise ConnectionError("DatabaseSessionManager is not initialized")
        await self.engine.dispose()
        self.engine = None
        self.engine = None
        # self.session = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Connect to database.

        Raises:
            Exception: _description_

        Returns:
            AsyncIterator[AsyncConnection]: _description_

        Yields:
            Iterator[AsyncIterator[AsyncConnection]]: _description_
        """
        if self.engine is None:
            raise ConnectionError("DatabaseSessionManager is not initialized")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Get a database async-session instance.

        Raises:
            Exception: _description_

        Returns:
            AsyncIterator[AsyncSession]: _description_

        Yields:
            Iterator[AsyncIterator[AsyncSession]]: _description_
        """
        if self.session_maker is None:
            raise ConnectionError("DatabaseSessionManager is not initialized")

        session = self.session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection) -> None:
        """(Used for testing) create all database metadata.

        Args:
            connection (AsyncConnection): database connection.
        """
        await connection.run_sync(EventPlanningSchemaBase.metadata.create_all)

    # Used for testing
    async def drop_all(self, connection: AsyncConnection) -> None:
        """(Used for testing) remove all database metadata.

        Args:
            connection (AsyncConnection): database connection.
        """
        await connection.run_sync(EventPlanningSchemaBase.metadata.drop_all)


# Initialize the DatabaseSessionManager
master_sessionmanager = DatabaseSessionManager()
replica_sessionmanager = DatabaseSessionManager()
