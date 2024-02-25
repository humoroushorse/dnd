"""Schema module attributes. (Pydantic Objects)."""

from app.dnd.schemas import dnd_class  # noqa: W0611
from app.dnd.schemas import enums  # noqa: W0611
from app.dnd.schemas import health_check  # noqa: W0611
from app.dnd.schemas import jt_spell_to_class  # noqa: W0611
from app.dnd.schemas import responses  # noqa: W0611
from app.dnd.schemas import source  # noqa: W0611
from app.dnd.schemas import spell  # noqa: W0611
from loguru import logger

logger = logger.bind(name=__name__)
