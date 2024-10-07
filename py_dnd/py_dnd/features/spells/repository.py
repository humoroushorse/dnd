"""Spell repository."""

from __future__ import annotations

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_dnd.features.core.repository import RepositoryBase
from py_dnd.features.spells.models import Spell
from py_dnd.features.spells.schemas import SpellCreate, SpellUpdate


class SpellRepository(RepositoryBase[Spell, SpellCreate, SpellUpdate]):
    """Spell Repository.

    Args:
        RepositoryBase (_type_): _description_
    """

    def __init__(self, session: AsyncSession, logger: loguru.Logger | None = None):
        super().__init__(session=session, model=Spell)
        self.logger.trace("{} created!", self.__class__.__name__)


# def get_spell_repository(session: AsyncSession) -> SpellRepository:
#     # This function will return an instance of the SpellRepository class
#     return SpellRepository(session)
