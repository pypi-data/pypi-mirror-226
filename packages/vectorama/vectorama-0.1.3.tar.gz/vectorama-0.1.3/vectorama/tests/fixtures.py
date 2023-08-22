from vectorama.base import VectoramaBase, VectoramaConfig
from vectorama.fields import EmbeddingField


class MyPizza(VectoramaBase):
    model_config = VectoramaConfig(
        desired_cluster_count=10,
        desired_cluster_size=100,
    )

    vec: list[float] = EmbeddingField(length=100)
    topping: str
    cost: int


class MyPizzaOptional(VectoramaBase):
    model_config = VectoramaConfig(
        desired_cluster_count=10,
        desired_cluster_size=100,
    )

    vec: list[float] = EmbeddingField(length=100)
    topping: str | None = None
    cost: int | None = None
