"""Shared models for API responses."""
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T", int, str)


class GenericListResponse(GenericModel, Generic[T]):
    """Wrapper model for returning list objects with other metadata."""

    total_count: int
    limit: int
    offset: int
    data_count: int
    data: List[T]


class BulkLoadResponse(BaseModel):
    """Response type for bulk loading resources."""

    class BulkLoadResponseTotals(BaseModel):
        """Summary report for bulk loading."""

        created: Optional[int] = 0
        errored: Optional[int] = 0
        warning: Optional[int] = 0

    filename: str
    totals: BulkLoadResponseTotals = BulkLoadResponseTotals()
    created: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    def update_totals(self) -> None:
        """Updates totals based on current array lengths."""
        self.totals.created = len(self.created if self.created else [])
        self.totals.errored = len(self.errors if self.errors else [])
        self.totals.warning = len(self.warnings if self.warnings else [])


class MessageResponse(BaseModel):
    """Response message."""

    message: str
