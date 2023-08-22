from typing import Any, Type, TypeVar

from pydantic import BaseModel

from vectorama.base import WrappedComparison

T = TypeVar("T", bound=BaseModel)


class Query:
    def __init__(self, model: Type[T]):
        self.model = model

        self.raw_filters: list[WrappedComparison] = []
        self.raw_limit: int | None = None
        self.raw_embedding: list[float] | None = None

    def filter(self, comparison: Any):
        # At runtime, `comparison` will be WrappedComparison, but because the class-based instance variables
        # are inherited from Pydantic, these comparisons (like MyModel.element == X) will look like a bool to mypy
        # We typehint this function as Any to avoid errors
        self.raw_filters.append(comparison)
        return self

    def limit(self, limit: int):
        self.raw_limit = limit
        return self

    def closest(self, embedding: list[float]):
        self.raw_embedding = embedding
        return self
