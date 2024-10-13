"""Database app startup functions."""

from loguru import logger
from sqlalchemy import text

from py_event_planning import shared
from py_event_planning.core.config import Settings
from py_event_planning.database.session import sessionmanager


async def get_all_schemas() -> list[str]:
    """Fetch list of schemas in the connected database."""
    async with sessionmanager.session() as session:
        result = await session.execute(
            text(
                """
                SELECT schema_name
                FROM information_schema.schemata
                """
            )
        )
        schemas = [row[0] for row in result.fetchall()]
        return schemas


async def init(_settings: Settings) -> None:
    """Verify that the required database schema(s) exist.

    Args:
        _settings (Settings): application environment variables.
    """
    target_schema: str = shared.enums.DbSchemaEnum.EVENT_PLANNING.value
    schemas = await get_all_schemas()

    if target_schema in schemas:
        logger.info("Connected to database cluster.")
    else:
        logger.error(
            f"Missing database schemas={[target_schema]}. Existing schemas={schemas}",
        )
