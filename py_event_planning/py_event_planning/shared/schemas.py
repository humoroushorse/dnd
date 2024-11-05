"""Shared schemas."""

import datetime
from typing import Annotated, Any, Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

T = TypeVar("T", bound=BaseModel)


class MixinBookeepingCreate:
    """Entity Creation Bookeeping Mixin."""

    created_at: Annotated[datetime.datetime, Field()]
    created_by: Annotated[str, Field()]

    # @field_serializer('created_at')
    # def serialize_created_at(self, dt: datetime.datetime):
    #     return dt.isoformat()


class MixinBookeepingUpdate:
    """Entity Update Bookeeping Mixin."""

    updated_at: Annotated[datetime.datetime, Field()]
    updated_by: Annotated[str, Field()]

    # @field_serializer('updated_at')
    # def serialize_created_by(self, dt: datetime.datetime):
    #     return dt.isoformat()


class MixinImageUrl:
    """Schema Mixin for adding image information."""

    image_url: str | None = Field(default=None, title="Image URL")
    image_url_description: str | None = Field(default=None, title="Image URL description (for accessability)")

    @model_validator(mode="before")
    @classmethod
    def image_must_also_have_description(cls, data: Any) -> Any:
        """Validator for forcing images to have descriptions for accessability reasons."""
        if isinstance(data, dict):
            if data.get("image_url") and not data.get("image_url_description"):
                raise ValueError("Image must also have a description for accessability reasons")
        return data


class QueryBase(BaseModel):
    """Query options for pagination."""

    limit: int | None = Field(
        default=100,
        title="Limit",
    )
    offset: int | None = Field(default=0, title="Offset")


class GenericListResponse(BaseModel, Generic[T]):
    """Wrapper model for returning list objects with other metadata."""

    total_entities_count: int | None = Field(
        default=0,
        title="Total Count",
        description="How many entities exist in the database for filters (excluding limit/offset).",
    )
    limit: int | None = Field(
        default=0,
        title="Limit",
    )
    offset: int | None = Field(default=0, title="Offset")
    filters: dict | None = Field(
        default=None, title="Filters", description="Filters used when querying, includes default filter values."
    )
    entities_count: int | None = Field(
        default=0,
        title="Data Count",
        description="How many entities are returned in this response for given filters (including limit/offset).",
    )
    entities: list[T] | None = Field(
        default_factory=list, title="Entities", description="Entites returned based on given filters."
    )

    @model_validator(mode="after")
    @classmethod
    def validate_model_generic(cls, data: Any) -> Any:
        """General checks for deterniming GenericListResponse field values.

        Args:
            data (Any): _description_

        Returns:
            Any: _description_
        """
        if not data.entities_count:
            data.entities_count = len(data.entities)
        # If not provided, assume we're returning everything
        if not data.total_entities_count:
            data.total_entities_count = len(data.entities)
        return data


class BulkLoadResponse(BaseModel):
    """Response type for bulk loading resources."""

    class BulkLoadResponseTotals(BaseModel):
        """Summary report for bulk loading."""

        created: int | None = 0
        errored: int | None = 0
        warning: int | None = 0

    filename: str
    totals: BulkLoadResponseTotals = BulkLoadResponseTotals()
    created: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def update_totals(self) -> None:
        """Updates totals based on current array lengths."""
        self.totals.created = len(self.created if self.created else [])
        self.totals.errored = len(self.errors if self.errors else [])
        self.totals.warning = len(self.warnings if self.warnings else [])
