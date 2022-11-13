"""Shared models for API responses."""
from typing import Generic, List, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T", int, str)


class GenericListResponse(GenericModel, Generic[T]):
    """Wrapper model for returning list objects with other metadata."""

    total_count: int
    limit: int
    offset: int
    data_count: int
    data: List[T]
