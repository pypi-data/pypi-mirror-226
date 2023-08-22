from typing import Any

from pydantic.fields import FieldInfo


class EmbeddingFieldBase(FieldInfo):
    def __init__(self, *, length: int, **kwargs):
        super().__init__(
            **kwargs,
        )
        self.length = length


class MetadataFieldBase(FieldInfo):
    def __init__(self, *, is_manifold: bool, **kwargs):
        super().__init__(
            **kwargs,
        )
        self.is_manifold = is_manifold


def EmbeddingField(length: int, **kwargs) -> Any:
    return EmbeddingFieldBase(length=length, **kwargs)


def MetadataField(is_manifold: bool = False, **kwargs) -> Any:
    return MetadataFieldBase(is_manifold=is_manifold, **kwargs)
