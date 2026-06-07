# Testing Guide

Stardust's tests should protect the public contract without making the small
codebase hard to change. Prefer focused tests that describe one behavior at a
time.

## Running Tests

Run the full suite:

```bash
uv run pytest
```

Run one area while developing:

```bash
uv run pytest tests/test_cli.py
uv run pytest tests/test_handle_file.py
uv run pytest tests/test_simple_app.py
```

Run with verbose test names when diagnosing a failure:

```bash
uv run pytest -vv
```

## Test Layout

`tests/test_cli.py` covers command-line orchestration:

- parsed arguments are forwarded into the loader, `Stardust`, and Uvicorn
- invalid application discovery exits before `uvicorn.run()`

`tests/test_handle_file.py` covers module loading and app discovery:

- loading a function from a file
- imports inside app files
- deterministic selection when multiple local functions exist
- package directory loading
- empty module behavior
- invalid paths
- directories without `__init__.py`

`tests/test_simple_app.py` covers request and response behavior through
Starlette `TestClient`:

- JSON responses
- request-aware handlers
- custom `Response` objects
- plain text responses
- query parameters
- JSON POST payloads
- response headers
- lifespan logging

## Choosing the Right Test Style

Use loader tests for behavior in `src/stardust/file_handler.py`. Temporary files
and directories are usually the clearest way to describe loader behavior.

Use `TestClient` tests for behavior in `src/stardust/stardust.py`. These tests
should make requests against a built Stardust app and assert on HTTP responses.

Use mocks sparingly for `src/stardust/cli.py`. CLI tests should prove wiring
without starting a real Uvicorn server.

## Regression Tests

Add a regression test before changing behavior in any of these areas:

- app discovery
- handler invocation
- response normalization
- supported HTTP methods
- default route or default file path
- CLI argument forwarding
- error handling visible to users

Regression tests should fail against the old behavior and pass with the new
implementation.

## Temporary Module Hygiene

The loader registers app modules under `sys.modules["stardust.app"]`. Tests that
load dynamic files should remove that entry before running. This prevents one
test's loaded module from affecting another test.

The existing `clean_module` fixture in `tests/test_handle_file.py` is the model
to follow when adding loader tests.

## Coverage Gaps

Areas worth strengthening:

- non-JSON-serializable return values
- import execution side effects in loaded modules
- handlers with more than one parameter
- unsupported HTTP methods
- richer CORS configuration
- CLI behavior for invalid paths and import failures
- package loading when app code uses relative imports

These gaps do not all need to be filled at once. Add coverage when touching the
related behavior.
