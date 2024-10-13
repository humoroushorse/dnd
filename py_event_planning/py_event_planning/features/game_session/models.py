"""SQLAlchemy Table: dnd_events definition."""

from sqlalchemy.orm import Mapped, mapped_column

from py_event_planning.database.base_class import EventPlanningSchemaBase
from py_event_planning.shared.models import MixinBookeeping


class GameSession(MixinBookeeping, EventPlanningSchemaBase):
    """SQLAlchemy dnd_event model."""

    # keys
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    # fields
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    organizer: Mapped[str] = mapped_column(nullable=False)
    # constraints
