from typing import Any, Type
from uuid import UUID

import pytest

import vectorama.fields as fields
from vectorama.api.api_pb2 import FieldType, MetadataField, MetadataValue, Schema
from vectorama.base import VectoramaBase
from vectorama.parsers import (
    MetadataFieldWrapper,
    parse_float_to_three_significant_figures_raw,
    parse_pydantic_model,
    pydantic_field_to_remote,
)


class MockModelWithEmbedding(VectoramaBase):
    model_config = {
        "desired_cluster_count": 5,
        "desired_cluster_size": 5,
        "require_reindex_skew_threshold": 0.5,
        "require_reindex_change_log_size": 500,
        "chunk_size": 2000,
    }
    test_embedding: list[float] = fields.EmbeddingField(length=50)
    test_field: str
    optional_field: int | None
    manifold_field: str = fields.MetadataField(is_manifold=True)
    uuid_field: UUID | None


class MockModelWithoutEmbedding(VectoramaBase):
    test_field: str


@pytest.mark.parametrize(
    "field1, field2, expected",
    [
        (
            MetadataField(name="name1", type=FieldType.String, isManifold=False),
            MetadataField(name="name1", type=FieldType.String, isManifold=False),
            True,
        ),
        (
            MetadataField(name="name1", type=FieldType.String, isManifold=False),
            MetadataField(name="name2", type=FieldType.String, isManifold=False),
            False,
        ),
    ],
)
def test_metadata_field_wrapper_equality(
    field1: MetadataField, field2: MetadataField, expected: bool
):
    wrapper1 = MetadataFieldWrapper(field1)
    wrapper2 = MetadataFieldWrapper(field2)
    assert (wrapper1 == wrapper2) == expected


@pytest.mark.parametrize(
    "field1, field2, expected",
    [
        (
            MetadataField(name="name1", type=FieldType.String, isManifold=False),
            MetadataField(name="name1", type=FieldType.String, isManifold=False),
            True,
        ),
        (
            MetadataField(name="name1", type=FieldType.String, isManifold=False),
            MetadataField(name="name2", type=FieldType.String, isManifold=False),
            False,
        ),
    ],
)
def test_metadata_field_wrapper_hash(
    field1: MetadataField, field2: MetadataField, expected: bool
):
    wrapper1 = MetadataFieldWrapper(field1)
    wrapper2 = MetadataFieldWrapper(field2)
    assert (hash(wrapper1) == hash(wrapper2)) == expected


def test_metadata_field_wrapper_validate_success():
    wrapper = MetadataFieldWrapper(
        MetadataField(name="test", type=FieldType.String, isManifold=False)
    )
    validated = MetadataFieldWrapper.validate(wrapper, None)
    assert validated == wrapper


def test_metadata_field_wrapper_validate_failure():
    with pytest.raises(ValueError):
        MetadataFieldWrapper.validate("invalid_value", None)


@pytest.mark.parametrize(
    "input_val, expected", [(0.12345, 0.123), (1234.56, 1230.0), (0.00012345, 0.000123)]
)
def test_parse_float_to_three_significant_figures(input_val: float, expected: float):
    assert parse_float_to_three_significant_figures_raw(input_val) == expected


@pytest.mark.parametrize(
    "model, expected_embedding_length, expected_metadatas",
    [
        (
            MockModelWithEmbedding,
            50,
            {
                MetadataFieldWrapper(
                    MetadataField(
                        name="test_field", type=FieldType.String, isManifold=False
                    )
                ),
                MetadataFieldWrapper(
                    MetadataField(
                        name="optional_field", type=FieldType.Int, isManifold=False
                    )
                ),
                MetadataFieldWrapper(
                    MetadataField(
                        name="manifold_field", type=FieldType.String, isManifold=True
                    )
                ),
                MetadataFieldWrapper(
                    MetadataField(
                        name="uuid_field", type=FieldType.UUID, isManifold=False
                    )
                ),
            },
        ),
    ],
)
def test_successful_parse_pydantic_model(
    model: Type[VectoramaBase],
    expected_embedding_length: int,
    expected_metadatas: set[MetadataFieldWrapper],
):
    parsed = parse_pydantic_model(model)
    assert parsed.embedding_length == expected_embedding_length
    assert parsed.metadatas == expected_metadatas


def test_failure_on_missing_embedding():
    with pytest.raises(ValueError, match="No embedding field found"):
        parse_pydantic_model(MockModelWithoutEmbedding)


@pytest.mark.parametrize(
    "schema, field_name, field_value, expected",
    [
        (
            Schema(fields=[MetadataField(name="test", type=FieldType.String)]),
            "test",
            "sample_string",
            MetadataValue(stringValue="sample_string"),
        ),
        (
            Schema(fields=[MetadataField(name="test", type=FieldType.Int)]),
            "test",
            1234,
            MetadataValue(intValue=1234),
        ),
        (
            Schema(fields=[MetadataField(name="test", type=FieldType.UUID)]),
            "test",
            UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
            MetadataValue(uuidValue="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
        ),
    ],
)
def test_pydantic_field_to_remote(
    schema: Schema, field_name: str, field_value: Any, expected: MetadataValue
):
    assert pydantic_field_to_remote(schema, field_name, field_value) == expected


def test_pydantic_field_to_remote_unsupported_field():
    with pytest.raises(ValueError, match="Unsupported field type"):
        pydantic_field_to_remote(
            Schema(fields=[MetadataField(name="test", type=9999)]),
            "test",
            "sample_string",
        )


@pytest.mark.parametrize(
    "schema, field_name, field_value",
    [
        (
            Schema(fields=[MetadataField(name="test", type=FieldType.String)]),
            "test",
            1234,
        ),
        (
            Schema(fields=[MetadataField(name="test", type=FieldType.Int)]),
            "test",
            "1234",
        ),
        (
            Schema(fields=[MetadataField(name="test", type=FieldType.UUID)]),
            "test",
            # We need a full UUID here, not a string
            "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        ),
    ],
)
def test_pydantic_field_to_remote_incorrect_type(
    schema: Schema, field_name: str, field_value: Any
):
    with pytest.raises(ValueError):
        pydantic_field_to_remote(schema, field_name, field_value)
