"""Shared schemas."""

import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

T = TypeVar("T", bound=BaseModel)


class MixinBookeeping:
    """Bookeeping Mixin."""

    created_at: datetime.datetime | None = Field(default=None)
    created_by: str
    updated_at: datetime.datetime | None = Field(default=None)
    updated_by: str


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
