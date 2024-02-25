"""Repository: jt_spell_to_class."""

from app.dnd.models.jt_spell_to_class import JtSpellToClass
from app.dnd.repository.base import RepositoryBase
from app.dnd.schemas.jt_spell_to_class import JtSpellToClassCreate, JtSpellToClassUpdate


class RepositoryJtSpellToClass(RepositoryBase[JtSpellToClass, JtSpellToClassCreate, JtSpellToClassUpdate]):
    """Repository for the jt_spell_to_class table."""

    # Declare model specific CRUD operation methods.


jt_spell_to_class = RepositoryJtSpellToClass(JtSpellToClass)
