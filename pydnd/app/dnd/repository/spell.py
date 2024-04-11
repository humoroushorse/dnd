"""Repository: spell."""

from typing import Any, Dict, List, Tuple

from dnd import models
from dnd.models.spell import Spell
from dnd.repository.base import RepositoryBase
from dnd.schemas.spell import SpellCreate, SpellUpdate
from sqlalchemy.orm import Session


class RepositorySpell(RepositoryBase[Spell, SpellCreate, SpellUpdate]):
    """Repository for the spell table."""

    # Declare model specific CRUD operation methods.
    def query_special(
        self,
        db: Session,
        params: Dict[str, List[Any] | str | bool | None],
        *,
        order_by: Any | None = None,
        limit: int | None = 100,
        offset: int | None = 0,
        class_names: List[str] | None = None,
        source_names: List[str] | None = None,
    ) -> Tuple[List[models.spell.Spell], int]:
        """Query spells with foreign key information.

        Args:
            db (Session): A SQLAlchemy Session.
            params (Dict[str, List[Any] | str | bool | None]): A dictionary of params for Spell.
            order_by (Any | None, optional): SQL 'ORDER BY' input. Defaults to None.
            limit (int | None, optional): SQL 'LIMIT'. Defaults to 100.
            offset (int | None, optional): SQL 'OFFSET'. Defaults to 0.
            class_names (List[str] | None, optional): A list of names from the class table. Defaults to None.
            source_names (List[str] | None, optional): A list of names from the source table. Defaults to None.

        Returns:
            Tuple[List[models.spell.Spell], int]: A list of spells and the total count.
        """
        spells = db.query(self.model)
        if class_names or source_names:
            spells = spells.join(models.JtSpellToClass)
            if class_names:
                spells = spells.join(models.DndClass).filter(
                    models.DndClass.name.in_([name.lower() for name in class_names])
                )
            if source_names:
                spells = spells.join(models.Source).filter(
                    models.Source.name.in_([name.lower() for name in source_names])
                )
        if params:
            spells = self.apply_param_filters_to_model(model=spells, params=params)
        if order_by is not None:
            spells = spells.order_by(order_by)
        total_count = spells.count()
        if offset:
            spells = spells.offset(offset)
        if limit:
            spells = spells.limit(limit)
        spells = spells.all()
        return spells, total_count


spell = RepositorySpell(Spell)
