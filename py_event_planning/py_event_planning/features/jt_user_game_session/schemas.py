"""Join Table User/GameSession schemas."""

import uuid

from pydantic import BaseModel, ConfigDict, Field

from py_event_planning.features.user.schemas import UserSchema
from py_event_planning.shared.schemas import (
    MixinBookeepingCreate,
    MixinBookeepingUpdate,
    QueryBase,
)


class JtUserGameSessionSchemaBase(BaseModel, MixinBookeepingCreate):
    """How the Join Table User/GameSession shows up in the database."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
        str_strip_whitespace=True,
    )
    id: uuid.UUID = Field(title="Join Table User/GameSystem ID")
    user_id: uuid.UUID = Field(title="User ID")
    game_session_id: uuid.UUID = Field(title="Game System ID")


class JtUserGameSessionSchema(JtUserGameSessionSchemaBase):
    """How the Join Table User/GameSession shows up in the database."""

    user: UserSchema | None = Field(default=None)
    # game_session


class JtUserGameSessionCreateInput(BaseModel):
    """Fields used to create a user."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    user_id: uuid.UUID | None = Field(default=None, title="User ID")


class JtUserGameSessionCreate(JtUserGameSessionCreateInput, MixinBookeepingCreate, MixinBookeepingUpdate):
    """Fields used to create a user."""

    game_session_id: uuid.UUID = Field(title="Game System ID")


class JtUserGameSessionUpdate(BaseModel, MixinBookeepingUpdate):
    """Fields you can update for a user."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    # no update


class JtUserGameSessionQuery(QueryBase):
    """Fields you can use to query user(s)."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    user_id: uuid.UUID = Field(title="User ID")
    game_session_id: uuid.UUID = Field(title="Game System ID")
