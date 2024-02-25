"""Models module attributes (SQLAlchemy DB generation Objects)."""

from app.dnd.models.dnd_class import DndClass  # noqa: W0611
from app.dnd.models.jt_spell_to_class import JtSpellToClass  # noqa: W0611
from app.dnd.models.source import Source  # noqa: W0611
from app.dnd.models.spell import Spell  # noqa: W0611
from loguru import logger

logger = logger.bind(name=__name__)
