import logging
from os import getenv
from typing import TYPE_CHECKING

import grpc
import pytest
import pytest_asyncio

from vectorama.api.api_pb2 import DestroyAllRequest
from vectorama.api.api_pb2_grpc import vectoramaStub

if TYPE_CHECKING:
    from vectorama.api.api_pb2_grpc import vectoramaAsyncStub


@pytest.fixture(autouse=True)
def enable_logging():
    logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def host():
    if getenv("vectorama_HOST"):
        return getenv("vectorama_HOST")
    return "localhost"


@pytest.fixture
def port():
    if getenv("vectorama_PORT"):
        return int(getenv("vectorama_PORT"))
    return 50051


@pytest_asyncio.fixture
async def wipe_database(host: str, port: int):
    async with grpc.aio.insecure_channel(f"{host}:{port}") as channel:
        stub: vectoramaAsyncStub = vectoramaStub(channel)  # type: ignore
        await stub.DestroyAll(DestroyAllRequest())
        logging.info("Wiped database")
