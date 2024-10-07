"""Sources repository."""

from __future__ import annotations

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_dnd.features.core.repository import RepositoryBase
from py_dnd.features.sources.models import Source
from py_dnd.features.sources.schemas import SourceCreate, SourceUpdate


class SourceRepository(RepositoryBase[Source, SourceCreate, SourceUpdate]):
    """Source Repository.

    Args:
        RepositoryBase (_type_): _description_
    """

    def __init__(self, session: AsyncSession, logger: loguru.Logger | None = None):
        super().__init__(session=session, model=Source)
        self.logger.trace("{} created!", self.__class__.__name__)


# def get_spell_repository(session: AsyncSession) -> SpellRepository:
#     # This function will return an instance of the SpellRepository class
#     return SpellRepository(session)
