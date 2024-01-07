"""SQLAlchemy Table: jt_spell_to_class definition."""
from dnd import schemas
from dnd.database.base_class import DbBase
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship


class JtSpellToClass(DbBase):
    """SQLAlchemy jt_spell_to_class model."""

    # keys
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(
        Integer, ForeignKey(f"{schemas.enums.DbSchemaEnum.DND.value}.source.id")
    )
    spell_id = Column(
        Integer, ForeignKey(f"{schemas.enums.DbSchemaEnum.DND.value}.spell.id")
    )
    dnd_class_id = Column(
        Integer, ForeignKey(f"{schemas.enums.DbSchemaEnum.DND.value}.dnd_class.id")
    )
    # relationships
    source = relationship("Source")
    spell = relationship("Spell")
    dnd_class = relationship("DndClass")
    # constraints
    UniqueConstraint("source_id", "spell_id", "class_id", name="ux_jtspelltoclass")
