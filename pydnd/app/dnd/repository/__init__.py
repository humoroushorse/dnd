"""Repository module list of repositories for interacting with SQLAchemy Tables."""

from app.dnd.repository.dnd_class import dnd_class  # noqa: W0611
from app.dnd.repository.jt_spell_to_class import jt_spell_to_class  # noqa: W0611
from app.dnd.repository.source import source  # noqa: W0611
from app.dnd.repository.spell import spell  # noqa: W0611
from loguru import logger

logger = logger.bind(name=__name__)
