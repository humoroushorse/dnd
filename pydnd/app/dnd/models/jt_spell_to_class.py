"""SQLAlchemy Table: jt_spell_to_class definition."""

from dnd.database.base_class import DbBase
from dnd.schemas.enums import DbSchemaEnum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class JtSpellToClass(DbBase):
    """SQLAlchemy jt_spell_to_class model."""

    # keys
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey(f"{DbSchemaEnum.DND.value}.source.id"))
    spell_id: Mapped[int] = mapped_column(ForeignKey(f"{DbSchemaEnum.DND.value}.spell.id"))
    dnd_class_id: Mapped[int] = mapped_column(ForeignKey(f"{DbSchemaEnum.DND.value}.dnd_class.id"))
    # relationships
    source = relationship("Source")
    spell = relationship("Spell")
    dnd_class = relationship("DndClass")
    # constraints
    UniqueConstraint("source_id", "spell_id", "class_id", name="ux_jtspelltoclass")
