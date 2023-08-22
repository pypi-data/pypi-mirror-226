from contextlib import asynccontextmanager
from logging import info
from time import time
from typing import TYPE_CHECKING, Generic, Iterable, Type, TypeVar

import grpc

from vectorama.api.api_pb2 import (
    DeleteVectorsRequest,
    GetSchemasRequest,
    InsertVectorsRequest,
    RegisterSchemaRequest,
    Schema,
    SearchVectorsRequest,
)
from vectorama.api.api_pb2_grpc import vectoramaStub
from vectorama.base import VectoramaBase
from vectorama.fields import (
    EmbeddingFieldBase as VectoramaEmbeddingField,
)
from vectorama.parsers import (
    MetadataFieldWrapper,
    ParsedPydanticModel,
    parse_pydantic_model,
    pydantic_field_to_remote,
    pydantic_model_to_remote,
    remote_to_pydantic_model,
)
from vectorama.query import Query
from vectorama.utils import get_batch

if TYPE_CHECKING:
    from vectorama.api.api_pb2_grpc import vectoramaAsyncStub

T = TypeVar("T", bound=VectoramaBase)


class SearchResponse(Generic[T]):
    def __init__(self, result: T, distance: float):
        self.result = result
        self.distance = distance


class VectoramaClient(Generic[T]):
    """
    Constructor class for a vectorama client.
    """

    def __init__(
        self,
        model: Type[T],
        host: str,
        port: int,
        max_insert_batch_size: int = 1000,
        max_delete_batch_size: int = 10000,
    ):
        self.validate_model(model)

        self.model = model
        self.host = host
        self.port = port
        self.max_insert_batch_size = max_insert_batch_size
        self.max_delete_batch_size = max_delete_batch_size

    def validate_model(self, model: Type[T]):
        """
        Validates that a local python model is compatible with vectorama schema definitions.
        """
        embedding_aliases = [
            field_name
            for field_name, field in model.model_fields.items()
            if isinstance(field, VectoramaEmbeddingField)
        ]
        # Ensure that only one field has an embedding alias
        if len(embedding_aliases) > 1:
            raise ValueError(
                f"Only one field should be an EmbeddingField, got: {embedding_aliases}"
            )
        elif len(embedding_aliases) == 0:
            raise ValueError(f"No EmbeddingField found in model: {model}")

        desired_cluster_count = model.model_config.get("desired_cluster_count")
        if not desired_cluster_count:
            raise ValueError(
                f"Model `{model.__name__}` must specify an model_config.desired_cluster_count attribute"
            )

        desired_cluster_size = model.model_config.get("desired_cluster_size")
        if not desired_cluster_size:
            raise ValueError(
                f"Model `{model.__name__}` must specify an model_config.desired_cluster_size attribute"
            )

    @asynccontextmanager
    async def connect(self):
        async with grpc.aio.insecure_channel(f"{self.host}:{self.port}") as channel:
            yield VectoramaConnection(
                self.model,
                channel,
                self.max_insert_batch_size,
                self.max_delete_batch_size,
            )


class VectoramaConnection(Generic[T]):
    """
    An open GRPC stream, used to send and receive messages.
    """

    def __init__(
        self,
        model: Type[T],
        channel: grpc.aio.Channel,
        max_insert_batch_size: int,
        max_delete_batch_size: int,
    ):
        self.model = model
        self.stub: vectoramaAsyncStub = vectoramaStub(channel)  # type: ignore
        self.max_insert_batch_size = max_insert_batch_size
        self.max_delete_batch_size = max_delete_batch_size
        self.server_schema: Schema | None = None

    async def register_schema(self) -> Schema:
        """
        Determines if schema is already in database, and if so, whether the fields are compatible
        with the current python definitions. If the fields are incompatible, an exception is raised.
        If the schema is not found, it is registered.

        """
        existing_response = await self.stub.GetSchemas(
            GetSchemasRequest(names=[self.model.__name__], returnClusters=False)
        )
        self.check_response_success(existing_response)

        if len(existing_response.schemas) > 1:
            raise ValueError(
                f"Expected to find at most one schema with name {self.model.__name__}, "
                f"but found {len(existing_response.schemas)}"
            )

        pydantic_parsed = parse_pydantic_model(self.model)
        if existing_response.schemas:
            # Determine if the fields have exact equality to the existing schema
            server_parsed = ParsedPydanticModel(
                desired_cluster_count=existing_response.schemas[
                    0
                ].schema.desiredClusterCount,
                desired_cluster_size=existing_response.schemas[
                    0
                ].schema.desiredClusterSize,
                require_reindex_skew_threshold=existing_response.schemas[
                    0
                ].schema.requireReindexSkewThreshold,
                require_reindex_change_log_size=existing_response.schemas[
                    0
                ].schema.requireReindexChangeLogSize,
                chunk_size=existing_response.schemas[0].schema.chunkSize,
                embedding_length=existing_response.schemas[0].schema.embeddingDimension,
                metadatas={
                    MetadataFieldWrapper(raw)
                    for raw in existing_response.schemas[0].schema.fields
                },
            )

            if pydantic_parsed != server_parsed:
                raise ValueError(
                    f"Existing schema `{existing_response.schemas[0].schema.name}` has fields {server_parsed}, "
                    f"but new schema has fields `{pydantic_parsed}`"
                )

            self.server_schema = existing_response.schemas[0].schema
        else:
            # Register the schema
            registration_respose = await self.stub.RegisterSchema(
                RegisterSchemaRequest(
                    schema=Schema(
                        name=self.model.__name__,
                        fields=[
                            metadata_wrapper.raw
                            for metadata_wrapper in pydantic_parsed.metadatas
                        ],
                        embeddingDimension=pydantic_parsed.embedding_length,
                        desiredClusterCount=pydantic_parsed.desired_cluster_count,
                        desiredClusterSize=pydantic_parsed.desired_cluster_size,
                        chunkSize=pydantic_parsed.chunk_size,
                        requireReindexChangeLogSize=pydantic_parsed.require_reindex_change_log_size,
                        requireReindexSkewThreshold=pydantic_parsed.require_reindex_skew_threshold,
                    )
                )
            )
            self.check_response_success(registration_respose)
            self.server_schema = registration_respose.schema

        if not self.server_schema:
            raise ValueError("Schema was not returned from the server")

        return self.server_schema

    async def insert(self, elements: Iterable[T]):
        """
        Inserts a batch of document into the database. If the given iterable is larger than our allowed batch size,
        we will chunk in the background and send over the wire.

        """
        if self.server_schema is None:
            raise ValueError("Schema must be registered before inserting elements")

        inserted_ids: list[int] = []

        for batch in get_batch(elements, self.max_insert_batch_size):
            start = time()
            info(f"Inserting a batch of {len(batch)} elements")
            server_records = [
                pydantic_model_to_remote(self.server_schema, element)
                for element in batch
            ]
            inserted_response = await self.stub.InsertVectors(
                InsertVectorsRequest(
                    schemaId=self.server_schema.id, records=server_records
                )
            )
            self.check_response_success(inserted_response)
            inserted_ids += inserted_response.ids
            info(
                f"Inserting a batch of {len(batch)} elements, took {time() - start} seconds"
            )

        return inserted_ids

    async def delete(self, element_ids: Iterable[int]):
        """
        Deletes the given documents
        """
        if self.server_schema is None:
            raise ValueError("Schema must be registered before deleting elements")

        # These payloads are much smaller than the insertion payloads, so batching *probably* isn't necessary
        # here for most requests. But we do it anyway, just in case the user has sent a very large payload of
        # elements to delete.
        for batch in get_batch(element_ids, self.max_delete_batch_size):
            deletion_response = await self.stub.DeleteVectors(
                DeleteVectorsRequest(
                    schemaId=self.server_schema.id,
                    ids=batch,
                )
            )
            self.check_response_success(deletion_response)

    async def search(
        self,
        query: Query,
        return_embeddings: bool = False,
        return_metadata: bool = True,
    ):
        """
        Searches for the given query, returning the top N results.
        """
        if self.server_schema is None:
            raise ValueError("Schema must be registered before searching elements")

        if query.raw_embedding is None:
            raise ValueError("Embedding must be set")
        if query.raw_limit is None:
            raise ValueError("Limit must be set")

        response = await self.stub.SearchVectors(
            SearchVectorsRequest(
                schemaId=self.server_schema.id,
                queryVector=query.raw_embedding,
                filters=[
                    SearchVectorsRequest.FilterDefinition(
                        name=query_filter.field,
                        value=pydantic_field_to_remote(
                            self.server_schema, query_filter.field, query_filter.value
                        ),
                        operation=query_filter.operator,
                    )
                    for query_filter in query.raw_filters
                ],
                returnEmbeddings=return_embeddings,
                returnMetadata=return_metadata,
                limit=query.raw_limit,
            )
        )
        self.check_response_success(response)

        # Now we can cast the response data to our object schema
        return [
            SearchResponse(
                result=remote_to_pydantic_model(
                    self.server_schema, result.vector, self.model
                ),
                distance=result.distance,
            )
            for result in response.results
        ]

    async def get_stats(self):
        """
        Returns the current statistics for the collection.
        """
        schemas_response = await self.stub.GetSchemas(
            GetSchemasRequest(
                names=[self.model.__name__], returnCollections=True, returnClusters=True
            )
        )
        # print(schemas_response)
        self.check_response_success(schemas_response)
        return schemas_response.schemas[0]

    def check_response_success(self, response):
        if not response.success:
            raise ValueError(f"Request failed: {response.errorMessage}")
