from typing import Iterable, TypeVar

T = TypeVar("T")


def get_batch(iterable: Iterable[T], n: int) -> Iterable[list[T]]:
    """
    Yield successive n-sized chunks from iterable.
    """
    # Create an iterator from the iterable
    it = iter(iterable)

    chunk = []

    for element in it:
        chunk.append(element)
        if len(chunk) == n:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
