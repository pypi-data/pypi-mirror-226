from logging import info
from random import random

import pytest

from vectorama.api.api_pb2 import GetSchemasResponse
from vectorama.base import VectoramaBase, VectoramaConfig
from vectorama.client import VectoramaClient
from vectorama.fields import EmbeddingField
from vectorama.query import Query
from vectorama.tests.fixtures import MyPizza, MyPizzaOptional


def get_member_sum(schema_stats: GetSchemasResponse.SchemaDefinition):
    return sum(
        [
            cluster.countMembers
            for collection in schema_stats.collectionDefinitions
            for cluster in collection.clusters
        ]
    )


@pytest.mark.asyncio
async def test_register_invalid_schema(host: str, port: int):
    class MyPizzaNoVector(VectoramaBase):
        # No embeddings specified
        model_config = VectoramaConfig(
            desired_cluster_count=10,
            desired_cluster_size=100,
        )
        vec: list[float]

    with pytest.raises(ValueError, match="No EmbeddingField found in model"):
        VectoramaClient[MyPizzaNoVector](MyPizzaNoVector, host, port)

    class MyPizzaNoClusters(VectoramaBase):
        # No clusters specified
        vec: list[float] = EmbeddingField(length=100)

    with pytest.raises(ValueError, match="must specify an model_config"):
        VectoramaClient[MyPizzaNoClusters](MyPizzaNoClusters, host, port)


@pytest.mark.asyncio
async def test_register_new_schema(wipe_database, host: str, port: int):
    client = VectoramaClient[MyPizza](MyPizza, host, port)
    async with client.connect() as connection:
        schema = await connection.register_schema()
        assert schema.name == "mypizza"


@pytest.mark.asyncio
async def test_register_existing_schema(wipe_database, host: str, port: int):
    client = VectoramaClient[MyPizza](MyPizza, host, port)
    async with client.connect() as connection:
        schema = await connection.register_schema()
        original_id = schema.id

        schema2 = await connection.register_schema()
        assert schema2.id == original_id


@pytest.mark.asyncio
async def test_register_different_schema(wipe_database, host: str, port: int):
    client = VectoramaClient[MyPizza](MyPizza, host, port)
    async with client.connect() as connection:
        await connection.register_schema()

    # We don't want to affect the global pizza model, so we create a subset of the fields here
    # We then mirror the original name because we want to encounter a collision
    class MyPizzaFake(VectoramaBase):
        model_config = MyPizza.model_config
        vec: list[float] = EmbeddingField(length=100)
        topping: str

    MyPizzaFake.__name__ = MyPizza.__name__

    client2 = VectoramaClient[MyPizzaFake](MyPizzaFake, host, port)
    async with client2.connect() as connection:
        with pytest.raises(ValueError):
            await connection.register_schema()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "vector_count",
    [
        1,
        10,
        10_000,
    ],
)
async def test_insert_vectors(wipe_database, host: str, port: int, vector_count: int):
    info("Generating random vectors")
    random_pizzas = [
        MyPizza(
            vec=[random() for _ in range(100)],
            topping=f"Topping Type {i}",
            cost=i * 10,
        )
        for i in range(vector_count)
    ]
    info(f"Generated {len(random_pizzas)} random vectors")

    client = VectoramaClient[MyPizza](MyPizza, host, port)
    async with client.connect() as connection:
        await connection.register_schema()
        inserted_ids = await connection.insert(random_pizzas)

        # Ensure that we can map the vectors to their IDs 1:1 in case clients have to take
        # secondary actions on them
        assert len(inserted_ids) == vector_count
        assert len(set(inserted_ids)) == vector_count

        schema_stats = await connection.get_stats()
        assert get_member_sum(schema_stats) == vector_count


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "vector_count",
    [
        1,
        10,
        10_000,
    ],
)
async def test_delete_vectors(wipe_database, host: str, port: int, vector_count: int):
    info("Generating random vectors")
    random_pizzas = [
        MyPizza(
            vec=[random() for _ in range(100)],
            topping=f"Topping Type {i}",
            cost=i * 10,
        )
        for i in range(vector_count)
    ]
    info(f"Generated {len(random_pizzas)} random vectors")

    client = VectoramaClient[MyPizza](MyPizza, host, port)
    async with client.connect() as connection:
        await connection.register_schema()

        # Ensure that the collection stats are zero to start
        schema_stats = await connection.get_stats()
        assert get_member_sum(schema_stats) == 0

        inserted_ids = await connection.insert(random_pizzas)

        # Ensure that we can map the vectors to their IDs 1:1 in case clients have to take
        # secondary actions on them
        assert len(inserted_ids) == vector_count
        assert len(set(inserted_ids)) == vector_count

        schema_stats = await connection.get_stats()
        assert get_member_sum(schema_stats) == vector_count

        # Try deleting these vectors
        await connection.delete(inserted_ids)

        # Get the collection stats and ensure they are zero
        schema_stats = await connection.get_stats()
        assert get_member_sum(schema_stats) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model,return_embeddings,return_metadata",
    [
        # Metadata has to be returned for the MyPizza model because the pydantic schema requires values
        (MyPizza, True, True),
        (MyPizza, False, True),
        # We create a new model here to allow nulls
        (MyPizzaOptional, True, True),
        (MyPizzaOptional, False, True),
        (MyPizzaOptional, True, False),
        (MyPizzaOptional, False, False),
    ],
)
async def test_simple_search(
    wipe_database,
    host: str,
    port: int,
    return_embeddings: bool,
    return_metadata: bool,
    model: VectoramaBase,
):
    pizzas = [
        MyPizza(
            vec=[random() for _ in range(100)],
            topping="pepperoni",
            cost=12,
        ),
        MyPizza(
            vec=[random() for _ in range(100)],
            topping="cheese",
            cost=10,
        ),
    ]

    client = VectoramaClient[model](model, host, port)  # type: ignore
    async with client.connect() as connection:
        await connection.register_schema()
        inserted_ids = await connection.insert(pizzas)

        # Ensure that we can map the vectors to their IDs 1:1 in case clients have to take
        # secondary actions on them
        assert len(inserted_ids) == len(pizzas)
        assert len(set(inserted_ids)) == len(pizzas)

        query = (
            Query(MyPizza)
            .filter(MyPizza.topping == "pepperoni")
            .closest([random() for _ in range(100)])
            .limit(1)
        )
        results = await connection.search(
            query, return_embeddings=return_embeddings, return_metadata=return_metadata
        )
        assert len(results) == 1
        assert results[0].result.id == inserted_ids[0]

        if return_metadata:
            assert results[0].result.topping == "pepperoni"
        if return_embeddings:
            assert results[0].result.vec is not None
