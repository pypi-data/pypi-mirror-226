from vectorama.base import vectoramaBase, vectoramaConfig
from vectorama.fields import EmbeddingField


class MyPizza(vectoramaBase):
    model_config = vectoramaConfig(
        desired_cluster_count=10,
        desired_cluster_size=100,
    )

    vec: list[float] = EmbeddingField(length=100)
    topping: str
    cost: int


class MyPizzaOptional(vectoramaBase):
    model_config = vectoramaConfig(
        desired_cluster_count=10,
        desired_cluster_size=100,
    )

    vec: list[float] = EmbeddingField(length=100)
    topping: str | None = None
    cost: int | None = None
