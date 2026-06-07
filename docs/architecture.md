# Architecture

## Module Layout

### `src/stardust/cli.py`

Owns process startup:

- parses arguments
- loads the application target
- constructs `Stardust`
- exits cleanly on invalid application input
- delegates serving to `uvicorn.run()`

This module should stay thin. It is orchestration code, not business logic.

### `src/stardust/file_handler.py`

Owns module loading and function discovery.

Key functions:

- `load_module(module_name, path)`: imports from a file or package path
- `find_local_function(module)`: returns the first local function
- `handle(path)`: convenience wrapper used by the CLI

Important design detail: loaded applications are registered under `sys.modules["stardust.app"]`. Tests explicitly clean that entry between runs.

### `src/stardust/stardust.py`

Owns ASGI app construction.

Key responsibilities:

- validate that a callable handler exists
- build the Starlette application
- route `/` requests
- normalize return values into HTTP responses
- emit startup and shutdown lifecycle logs

## Request Lifecycle

1. Uvicorn receives the HTTP request.
2. Starlette routes `GET /` or `POST /` to `Stardust.__wrap_response`.
3. `__wrap_response` inspects the handler signature.
4. The handler is called either with `Request` or with no args.
5. If the result is not already a `Response`, it is wrapped in `JSONResponse`.
6. Starlette sends the final response.

## Error Model

### Invalid app input

`Stardust` raises `InvalidApplicationError` when initialized without a callable function.

### Path and import failures

`file_handler` raises:

- `ValueError` for invalid paths
- `FileNotFoundError` for directories without `__init__.py`
- `ImportError` if module spec creation fails

The CLI only converts the missing-callable case into a user-facing exit. Other exceptions currently propagate.

## Logging

Logging is intentionally minimal:

- CLI logs an exception when app loading produces `InvalidApplicationError`
- `Stardust.lifespan()` logs startup and shutdown events with the configured port in structured `extra`

There is no custom logger configuration in the package itself; logging behavior is mostly delegated to the hosting process and Uvicorn settings.

## Extension Points

The cleanest places to extend behavior are:

- `find_local_function()` if app discovery rules need to change
- `Stardust.build()` if middleware or routes need to expand
- `Stardust.__wrap_response()` if response coercion rules need to expand
- `cli.main()` if new runtime options are introduced

When changing any of these areas, preserve the library’s main invariant: a minimal app should still be runnable with one small file and no extra configuration.
