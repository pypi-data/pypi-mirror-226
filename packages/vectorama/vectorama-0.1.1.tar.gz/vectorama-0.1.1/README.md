# vectorama-python

## Tests

**Tests will clear out the current database as part of the test flows. Make sure you are only running a test server locally and you are not storing real data.**

Tests are intended to be run with a live vectorama server running on `localhost:50051`. We provide a docker-compose file for this purpose. To run the tests, first start the server:

```bash
docker-compose up
```

Then, in a separate terminal, run the tests:

```bash
poetry run pytest
```
