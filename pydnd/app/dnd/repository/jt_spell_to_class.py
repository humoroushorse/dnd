"""Repository: jt_spell_to_class."""
from dnd.models.jt_spell_to_class import JtSpellToClass
from dnd.repository.base import RepositoryBase
from dnd.schemas.jt_spell_to_class import JtSpellToClassCreate, JtSpellToClassUpdate


class RepositoryJtSpellToClass(
    RepositoryBase[JtSpellToClass, JtSpellToClassCreate, JtSpellToClassUpdate]
):
    """Repository for the jt_spell_to_class table."""

    # Declare model specific CRUD operation methods.


jt_spell_to_class = RepositoryJtSpellToClass(JtSpellToClass)
