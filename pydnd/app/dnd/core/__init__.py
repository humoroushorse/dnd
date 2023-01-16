"""Core API modules."""
from dnd.core.config import settings  # noqa: W0611
from loguru import logger

logger = logger.bind(name=__name__)
