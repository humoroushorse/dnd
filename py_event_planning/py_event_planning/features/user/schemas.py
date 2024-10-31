"""User schemas."""

from pydantic import BaseModel, ConfigDict, Field

from py_event_planning.shared.schemas import MixinBookeepingCreate, QueryBase


class UserSchema(BaseModel, MixinBookeepingCreate):
    """How the User shows up in the database."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    # Fields of the model
    id: str = Field(title="User ID")


class UserCreate(BaseModel):
    """Fields used to create a user."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
    )

    # Fields of the model


class UserUpdate(BaseModel):
    """Fields you can update for a user."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
    )

    # Fields of the model


class UserQuery(QueryBase):
    """Fields you can use to query user(s)."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    # Fields of the model
