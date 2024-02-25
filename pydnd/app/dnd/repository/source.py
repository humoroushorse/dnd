"""Repository: source."""

from app.dnd.models.source import Source
from app.dnd.repository.base import RepositoryBase
from app.dnd.schemas.source import SourceCreate, SourceUpdate


class RepositorySource(RepositoryBase[Source, SourceCreate, SourceUpdate]):
    """Repository for the source table."""

    # Declare model specific CRUD operation methods.


source = RepositorySource(Source)
