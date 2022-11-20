"""Repository: dnd_class (to avoid 'class' keword)."""
from dnd.models.dnd_class import DndClass
from dnd.repository.base import RepositoryBase
from dnd.schemas.dnd_class import DndClassCreate, DndClassUpdate


class RepositoryDndClass(RepositoryBase[DndClass, DndClassCreate, DndClassUpdate]):
    """Repository for the dnd_class table."""

    # Declare model specific CRUD operation methods.


dnd_class = RepositoryDndClass(DndClass)
