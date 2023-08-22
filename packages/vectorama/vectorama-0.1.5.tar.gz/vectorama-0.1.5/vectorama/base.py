from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel, ConfigDict
from pydantic._internal._model_construction import ModelMetaclass

from vectorama.api.api_pb2 import (
    OperationType,
)

RESERVED_FIELDS = ["id"]


@dataclass
class WrappedComparison:
    field: str
    operator: OperationType.ValueType
    value: Any


class ComparisonField:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other: Any):
        return WrappedComparison(
            field=self.name, operator=OperationType.Equal, value=other
        )

    def __ne__(self, other: Any):
        return WrappedComparison(
            field=self.name, operator=OperationType.NotEqual, value=other
        )

    def __gt__(self, other: Any):
        return WrappedComparison(
            field=self.name, operator=OperationType.GreaterThan, value=other
        )

    def __ge__(self, other: Any):
        return WrappedComparison(
            field=self.name, operator=OperationType.GreaterThanOrEqual, value=other
        )

    def __lt__(self, other: Any):
        return WrappedComparison(
            field=self.name, operator=OperationType.LessThan, value=other
        )

    def __le__(self, other: Any):
        return WrappedComparison(
            field=self.name, operator=OperationType.LessThanOrEqual, value=other
        )


class VectoramaMetaClass(ModelMetaclass):
    def __getattr__(cls, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            # We only want to allow Model.attribute access once we have parsed the model
            # definition into its component fields
            # Before this point, the model constructors use the __getattr__ class to determine
            # different parent properties, so returning prematurely here would break the model
            # configuration behavior
            model_fields = getattr(cls, "model_fields")
            if name in RESERVED_FIELDS:
                raise
            if model_fields:
                requested_field = model_fields.get(name)
                if requested_field:
                    return ComparisonField(name)
            raise


class VectoramaConfig(ConfigDict, total=False):
    """
    Desired total number of clusters. This is used as an absolute figure; we will
    always initialize at least |desired_cluster_count| clusters.
    """

    desired_cluster_count: int

    """
    The desired size of each cluster. This is used in expectation, so we attempt
    to balance clusters out to roughly size |desired_cluster_size|.
    """
    desired_cluster_size: int

    """
    The amount of records that are stored in one text-file. This is expected to be able to quickly
    load the data into memory. If your record sizes are large, you likely want to decrease this value.
    Defaults to 1000.
    """
    chunk_size: int

    """
    The threshold for the skew of the cluster sizes. This is defined as the relative difference between the
    euclidean norms of the fixed centroid and the new datapoint average. If the skew is larger than this
    value, we will reindex the cluster. Defaults to 0.1.

    """
    require_reindex_skew_threshold: float

    """
    The threshold for the change in the size of the change log. If each cluster has more than this quantity of objects
    inserted, we will perform a reindex. Defaults to 1000.

    """
    require_reindex_change_log_size: int


class VectoramaBase(BaseModel, metaclass=VectoramaMetaClass):
    if TYPE_CHECKING:
        model_config: ClassVar[VectoramaConfig]

    # Set by the server, client values are ignored
    id: int | None = None
