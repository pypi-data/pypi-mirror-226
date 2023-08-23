import math
from typing import Any, Callable, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel, field_validator
from pydantic_core import core_schema

from vectorama.api.api_pb2 import (
    FieldType,
    MetadataField,
    MetadataValue,
    Record,
    Schema,
)
from vectorama.base import RESERVED_FIELDS, VectoramaBase
from vectorama.fields import (
    EmbeddingFieldBase as VectoramaEmbeddingField,
)
from vectorama.fields import (
    MetadataFieldBase as vectoramaMetadataField,
)

T = TypeVar("T", bound=VectoramaBase)


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

    @classmethod
    def validate(
        cls, __input_value: Any, _: core_schema.ValidationInfo
    ) -> "MetadataFieldWrapper":
        if not isinstance(__input_value, MetadataFieldWrapper):
            raise ValueError(
                f"Expected MetadataFieldWrapper, received: {type(__input_value)}"
            )
        return __input_value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.general_plain_validator_function(cls.validate)


class ParsedPydanticModel(BaseModel):
    desired_cluster_count: int
    desired_cluster_size: int
    require_reindex_skew_threshold: float
    require_reindex_change_log_size: int
    chunk_size: int
    embedding_length: int
    metadatas: set[MetadataFieldWrapper]

    @field_validator("require_reindex_skew_threshold")
    def parse_float_to_three_significant_figures(cls, v):
        return parse_float_to_three_significant_figures_raw(v)


def parse_pydantic_model(model: Type[T]):
    embedding_size: int | None = None
    metadatas: list[MetadataField] = []

    for field_name, field_value in model.model_fields.items():
        if field_name in RESERVED_FIELDS:
            continue

        field_type: FieldType.ValueType | None = None

        if isinstance(field_value, VectoramaEmbeddingField):
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
        # Specify default values for the model configuration
        desired_cluster_count=model.model_config["desired_cluster_count"],
        desired_cluster_size=model.model_config["desired_cluster_size"],
        require_reindex_skew_threshold=model.model_config.get(
            "require_reindex_skew_threshold", 0.1
        ),
        require_reindex_change_log_size=model.model_config.get(
            "require_reindex_change_log_size", 1000
        ),
        chunk_size=model.model_config.get("chunk_size", 1000),
        embedding_length=embedding_size,
        metadatas={MetadataFieldWrapper(metadata) for metadata in metadatas},
    )


def pydantic_field_to_remote(schema: Schema, field_name: str, field_value: Any):
    field = next(field for field in schema.fields if field.name == field_name)
    match field.type:
        case FieldType.String:
            if not isinstance(field_value, str):
                raise ValueError(
                    f"Incorrect input argument type for string-metadata: {field_value} ({type(field_value)})"
                )
            return MetadataValue(stringValue=field_value)
        case FieldType.Int:
            if not isinstance(field_value, int):
                raise ValueError(
                    f"Incorrect input argument type for int-metadata: {field_value} ({type(field_value)})"
                )
            return MetadataValue(intValue=field_value)
        case FieldType.UUID:
            if not isinstance(field_value, UUID):
                raise ValueError(
                    f"Incorrect input argument type for uuid-metadata: {field_value} ({type(field_value)})"
                )
            return MetadataValue(uuidValue=str(field_value))
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
        if isinstance(field, VectoramaEmbeddingField)
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
                metadata_values[schema_field.name] = UUID(record_metadata.uuidValue)
            case _:
                raise ValueError(f"Unsupported field type: {schema_field.type}")

    embedding_field_name = next(
        field_name
        for field_name, field in model.model_fields.items()
        if isinstance(field, VectoramaEmbeddingField)
    )
    metadata_values[embedding_field_name] = record.embedding
    metadata_values["id"] = record.id

    return model(**metadata_values)


def parse_float_to_three_significant_figures_raw(v: float) -> float:
    return round(v, 3 - int(math.floor(math.log10(abs(v)))) - 1)
