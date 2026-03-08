# Testing Guide

## Test Suite

Run the full test suite with:

```bash
uv run pytest
```

The test suite currently covers:

- CLI argument wiring
- invalid application handling
- function discovery from files and packages
- invalid path behavior
- request and response behavior through Starlette `TestClient`
- lifespan logging

## Test Files

### [`tests/test_cli.py`](/Users/luke/Projects/stardust/tests/test_cli.py)

Verifies:

- parsed CLI arguments are forwarded correctly
- invalid application discovery exits before `uvicorn.run()`

### [`tests/test_handle_file.py`](/Users/luke/Projects/stardust/tests/test_handle_file.py)

Verifies:

- loading app code from a file
- handling imports inside app files
- multi-function file behavior
- package directory loading
- empty module behavior
- invalid path and invalid package layout behavior

### [`tests/test_simple_app.py`](/Users/luke/Projects/stardust/tests/test_simple_app.py)

Verifies:

- JSON responses
- request-aware handlers
- custom `Response` objects
- plain text responses
- query params
- JSON POST payload echoing
- response headers
- lifecycle logging

## Writing New Tests

Guidelines:

- prefer focused unit tests for loader behavior
- prefer `TestClient` for request/response behavior
- test both successful paths and explicit failure modes
- add a regression test before changing behavior that could affect app discovery or response normalization

## Gaps Worth Watching

Current gaps include:

- non-JSON-serializable return values
- import execution side effects in loaded modules
- behavior for handlers with more than one parameter
- methods other than `GET` and `POST`
- richer CORS configuration

These are good candidates for new tests if those areas change.
