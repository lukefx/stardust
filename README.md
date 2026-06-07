# Stardust

[![PyPI version](https://badge.fury.io/py/stardust.svg)](https://badge.fury.io/py/stardust)
[![Python Versions](https://img.shields.io/pypi/pyversions/stardust.svg)](https://pypi.org/project/stardust/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Stardust is a minimal ASGI microframework for serving a single Python function as an HTTP endpoint. It is built on top of Starlette and Uvicorn and is designed around a simple contract: load one local function, expose it at `/`, and convert its return value into an HTTP response.

## What It Does

- Loads a Python file or package directory.
- Finds the first local function defined in that module.
- Serves that function on `/` for `GET` and `POST`.
- Passes the incoming `Request` object when the function accepts parameters.
- Wraps non-`Response` return values in `JSONResponse`.
- Enables permissive CORS by default.

## Installation

```bash
pip install stardust
```

Requires Python 3.10 or newer.

## Quick Start

Create `app.py`:

```python
async def serve(req):
    return {"hello": "world"}
```

Run it:

```bash
stardust app.py
```

The app will be available at `http://localhost:8000/`.

## Application Contract

Stardust looks for the first local function in the target module. That function can be:

- `async def serve(req): ...`
- `async def serve(): ...`
- `def serve(req): ...`
- `def serve(): ...`

If the function accepts at least one parameter, Stardust passes the Starlette `Request` object. If it accepts no parameters, it is called without arguments.

### Return Values

- `dict`, `list`, and other JSON-serializable values are returned as JSON.
- Any Starlette `Response` subclass is returned unchanged.
- Status codes and headers should be controlled by returning a `Response` object.

Example:

```python
from starlette.responses import PlainTextResponse


async def serve(req):
    name = req.query_params.get("name", "world")
    return PlainTextResponse(f"hello {name}")
```

## CLI

```bash
stardust [file]
stardust --file path/to/app.py --host 127.0.0.1 --port 9000 --log-level info --debug
```

Options:

- `file`: optional positional target, defaults to `app.py`
- `--file`: explicit target path to a Python file or package directory
- `--host`: bind host, defaults to `0.0.0.0`
- `--port`: bind port, defaults to `8000`
- `--log-level`: one of `critical`, `error`, `warning`, `info`, `debug`
- `--debug`: enables Starlette debug mode and Uvicorn access logs

If no local function is found, the CLI exits with status code `1`.

## Examples

The [`examples/`](/Users/luke/Projects/stardust/examples) directory contains small runnable apps, including:

- JSON responses
- plain text responses
- query parameter handling
- multiple functions in one module
- package-based app loading

## Developer Documentation

Detailed developer documentation lives in [`docs/`](/Users/luke/Projects/stardust/docs):

- [`docs/overview.md`](/Users/luke/Projects/stardust/docs/overview.md)
- [`docs/architecture.md`](/Users/luke/Projects/stardust/docs/architecture.md)
- [`docs/development.md`](/Users/luke/Projects/stardust/docs/development.md)
- [`docs/testing.md`](/Users/luke/Projects/stardust/docs/testing.md)

## Local Development

```bash
uv sync --all-extras --dev
uv run pytest
```

## License

MIT. See [`LICENSE.txt`](/Users/luke/Projects/stardust/LICENSE.txt).
