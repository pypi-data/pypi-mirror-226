from dataclasses import dataclass
from typing import Any, Optional, Type, TypeVar
from uuid import UUID

from vectorama.api.api_pb2 import (
    FieldType,
    MetadataField,
    MetadataValue,
    Record,
    Schema,
)
from vectorama.base import RESERVED_FIELDS, vectoramaBase
from vectorama.fields import (
    EmbeddingFieldBase as vectoramaEmbeddingField,
)
from vectorama.fields import (
    MetadataFieldBase as vectoramaMetadataField,
)

T = TypeVar("T", bound=vectoramaBase)


class MetadataFieldWrapper:
    """
    Provide hashing support for MetadataField, since grpc objects are not hashable by default. This allows
    clients to more easily determine the equality between two metadata definitions.

    """

    def __init__(self, metadata_field: MetadataField):
        self.raw = metadata_field

    def __eq__(self, other):
        if isinstance(other, MetadataFieldWrapper):
            return (
                self.raw.name == other.raw.name
                and self.raw.type == other.raw.type
                and self.raw.isManifold == other.raw.isManifold
            )
        return False

    def __hash__(self):
        return hash((self.raw.name, self.raw.type, self.raw.isManifold))


@dataclass(frozen=True)
class ParsedPydanticModel:
    desired_cluster_count: int
    desired_cluster_size: int
    chunk_size: int
    embedding_length: int
    metadatas: frozenset[MetadataFieldWrapper]


def parse_pydantic_model(model: Type[T]):
    embedding_size: int | None = None
    metadatas: list[MetadataField] = []

    for field_name, field_value in model.model_fields.items():
        if field_name in RESERVED_FIELDS:
            continue

        field_type: FieldType.ValueType | None = None

        if isinstance(field_value, vectoramaEmbeddingField):
            embedding_size = field_value.length
            continue

        if field_value.annotation == str or field_value.annotation == Optional[str]:
            field_type = FieldType.String
        elif field_value.annotation == int or field_value.annotation == Optional[int]:
            field_type = FieldType.Int
        elif field_value.annotation == UUID or field_value.annotation == Optional[UUID]:
            field_type = FieldType.UUID
        else:
            raise ValueError(f"Unsupported field type: {field_value.annotation}")

        metadatas.append(
            MetadataField(
                name=field_name,
                type=field_type,
                isManifold=field_value.is_manifold
                if isinstance(field_value, vectoramaMetadataField)
                else False,
            )
        )

    if embedding_size is None:
        raise ValueError("No embedding field found")

    return ParsedPydanticModel(
        desired_cluster_count=model.model_config["desired_cluster_count"],
        desired_cluster_size=model.model_config["desired_cluster_size"],
        chunk_size=model.model_config.get("chunk_size", 1000),
        embedding_length=embedding_size,
        metadatas=frozenset([MetadataFieldWrapper(metadata) for metadata in metadatas]),
    )


def pydantic_field_to_remote(schema: Schema, field_name: str, field_value):
    field = next(field for field in schema.fields if field.name == field_name)
    match field.type:
        case FieldType.String:
            return MetadataValue(stringValue=field_value)
        case FieldType.Int:
            return MetadataValue(intValue=field_value)
        case FieldType.UUID:
            return MetadataValue(uuidValue=field_value)
        case _:
            raise ValueError(f"Unsupported field type: {field.type}")


def pydantic_model_to_remote(schema: Schema, model: T) -> Record:
    # Format the key/value pairs implicit in our local model to the protobuf packed versions
    # that we'll send to the server
    ordered_metadata: list[MetadataValue] = []
    for field in schema.fields:
        field_value = getattr(model, field.name)
        metadata_value = pydantic_field_to_remote(schema, field.name, field_value)
        ordered_metadata.append(metadata_value)

    embedding_values = [
        getattr(model, field_name)
        for field_name, field in model.model_fields.items()
        if isinstance(field, vectoramaEmbeddingField)
    ]

    if len(embedding_values) != 1:
        raise ValueError(
            f"Expected exactly one embedding field, got: {embedding_values}"
        )

    return Record(
        metadata=ordered_metadata,
        embedding=embedding_values[0],
    )


def remote_to_pydantic_model(schema: Schema, record: Record, model: Type[T]) -> T:
    metadata_values: dict[str, Any] = {}
    for schema_field, record_metadata in zip(schema.fields, record.metadata):
        match schema_field.type:
            case FieldType.String:
                metadata_values[schema_field.name] = record_metadata.stringValue
            case FieldType.Int:
                metadata_values[schema_field.name] = record_metadata.intValue
            case FieldType.UUID:
                metadata_values[schema_field.name] = record_metadata.uuidValue
            case _:
                raise ValueError(f"Unsupported field type: {schema_field.type}")

    embedding_field_name = next(
        field_name
        for field_name, field in model.model_fields.items()
        if isinstance(field, vectoramaEmbeddingField)
    )
    metadata_values[embedding_field_name] = record.embedding
    metadata_values["id"] = record.id

    return model(**metadata_values)
