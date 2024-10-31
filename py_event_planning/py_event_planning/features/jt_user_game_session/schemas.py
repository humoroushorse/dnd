"""Join Table User/GameSession schemas."""

from pydantic import BaseModel, ConfigDict, Field

from py_event_planning.shared.schemas import MixinBookeepingCreate


class JtUserGameSession(BaseModel, MixinBookeepingCreate):
    """How the Join Table User/GameSession shows up in the database."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    # Fields of the model
    id: str = Field(title="Join Table User/GameSystem ID")
