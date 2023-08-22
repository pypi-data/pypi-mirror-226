from vectorama.api.api_pb2 import (
    OperationType,
)
from vectorama.query import Query
from vectorama.tests.fixtures import MyPizza


def test_query_simple_filter():
    query = Query(MyPizza).filter(MyPizza.topping == "pepperoni")
    assert len(query.raw_filters) == 1
    assert query.raw_filters[0].field == "topping"
    assert query.raw_filters[0].value == "pepperoni"
    assert query.raw_filters[0].operator == OperationType.Equal
