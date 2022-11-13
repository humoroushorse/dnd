"""Repository: source."""
from dnd.models.source import Source
from dnd.repository.base import RepositoryBase
from dnd.schemas import SourceCreate, SourceUpdate


class RepositorySource(RepositoryBase[Source, SourceCreate, SourceUpdate]):
    """Repository for the source table."""

    # Declare model specific CRUD operation methods.


source = RepositorySource(Source)
