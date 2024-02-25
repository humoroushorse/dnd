"""Repository: spell."""

from typing import Any, Dict, List, Optional, Tuple, Union

from app.dnd import models
from app.dnd.models.spell import Spell
from app.dnd.repository.base import RepositoryBase
from app.dnd.schemas.spell import SpellCreate, SpellUpdate
from sqlalchemy.orm import Session


class RepositorySpell(RepositoryBase[Spell, SpellCreate, SpellUpdate]):
    """Repository for the spell table."""

    # Declare model specific CRUD operation methods.
    def query_special(
        self,
        db: Session,
        params: Dict[str, Union[List[Any], str, bool, None]],
        *,
        order_by: Optional[Any] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
        class_names: Optional[List[str]] = None,
        source_names: Optional[List[str]] = None,
    ) -> Tuple[List[models.spell.Spell], int]:
        """Query spells with foreign key information.

        Args:
            db (Session): A SQLAlchemy Session.
            params (Dict[str, Union[List[Any], str]]): A dictionary of params for Spell.
            order_by (Optional[Any], optional): SQL 'ORDER BY' input. Defaults to None.
            limit (Optional[int], optional): SQL 'LIMIT'. Defaults to 100.
            offset (Optional[int], optional): SQL 'OFFSET'. Defaults to 0.
            class_names (Optional[List[str]], optional): A list of names from the class table. Defaults to None.
            source_names (Optional[List[str]], optional): A list of names from the source table. Defaults to None.

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
