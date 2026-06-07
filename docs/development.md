# Development Guide

This guide is for people changing Stardust itself. If you only want to run a
Stardust application, start with the project `README.md`.

Stardust is intentionally small: it loads one Python function, wraps it in a
Starlette app, and serves it with Uvicorn. Most changes should preserve that
shape unless they are explicitly meant to expand the public contract.

## Quick Start

Prerequisites:

- Python 3.10 or newer
- `uv`

Set up the development environment:

```bash
uv sync --all-extras --dev
```

Run the test suite:

```bash
uv run pytest
```

Build the package locally:

```bash
uv build
```

Run one of the examples:

```bash
uv run stardust examples/app.py
```

Then open `http://localhost:8000/`.

## Repository Map

```text
src/stardust/          Package source
tests/                 Automated tests
examples/              Small runnable Stardust apps
docs/                  Developer and architecture notes
README.md              User-facing overview and quick start
pyproject.toml         Package metadata, dependencies, and script entry point
uv.lock                Locked dependency graph for reproducible local installs
```

Important source files:

- `src/stardust/cli.py`: command-line parsing and process startup
- `src/stardust/file_handler.py`: app module loading and function discovery
- `src/stardust/stardust.py`: Starlette app construction and response handling
- `src/stardust/py.typed`: marker file declaring the package as typed

## Daily Workflow

Use a small edit-test loop:

```bash
uv run pytest tests/test_handle_file.py
uv run pytest tests/test_simple_app.py
uv run pytest
```

For runtime checks, prefer the examples over ad hoc scratch files. They document
the intended behavior and make it easier to spot regressions:

```bash
uv run stardust examples/plain_text_response.py
uv run stardust examples/query_params.py
uv run stardust examples/example_module
```

When changing public behavior, update docs in the same change. This project has
a small enough surface area that code, tests, examples, and docs should stay in
sync.

## Design Principles

Keep the core contract simple:

- A user points Stardust at a Python file or package directory.
- Stardust finds one local function.
- Stardust serves that function at `/`.
- The function may be synchronous or asynchronous.
- If the function accepts parameters, it receives the Starlette `Request`.
- Starlette `Response` objects pass through unchanged.
- Other return values are wrapped in `JSONResponse`.

Prefer explicit behavior over clever inference. Stardust should be easy to
explain from a short example, and failures should point users toward a concrete
fix.

## Working on App Loading

App loading lives in `src/stardust/file_handler.py`.

The loader accepts either:

- a Python file
- a package directory containing `__init__.py`

The loaded module is registered as `stardust.app` in `sys.modules`. Tests that
load temporary modules should clean that entry before running so state from one
test cannot leak into another.

Be careful when changing:

- how paths are classified as files or directories
- how package directories are resolved
- how imported functions are excluded
- how the first local function is selected
- how module names are registered in `sys.modules`

If discovery behavior changes, update `tests/test_handle_file.py` and add or
adjust examples when the new behavior is user-visible.

## Working on HTTP Behavior

HTTP behavior lives in `src/stardust/stardust.py`.

The most important path is `Stardust.__wrap_response()`:

1. Inspect the handler signature.
2. Call the handler with `Request` if it accepts at least one parameter.
3. Await the result if the handler is asynchronous.
4. Return existing Starlette `Response` objects unchanged.
5. Wrap every other result in `JSONResponse`.

Keep both synchronous and asynchronous handlers working. If you change response
normalization, add tests for both ordinary JSON values and explicit Starlette
responses.

`Stardust.build()` owns middleware and route construction. Changes here are
usually public behavior changes because they affect every served app.

## Working on the CLI

CLI behavior lives in `src/stardust/cli.py`.

The CLI should stay thin:

- parse arguments
- load the user function
- construct `Stardust`
- delegate serving to `uvicorn.run()`

When adding or changing flags:

- preserve `stardust app.py`
- preserve the default target of `app.py`
- update `tests/test_cli.py`
- document the flag in `README.md`
- include the default value in the documentation

The CLI currently converts missing application functions into a clean exit.
Other path, import, and runtime errors are allowed to propagate.

## Backward Compatibility

Treat these behaviors as compatibility-sensitive:

- default target path is `app.py`
- root route is `/`
- supported HTTP methods are `GET` and `POST`
- discovery uses the first local function
- handlers may accept zero parameters or at least one request parameter
- sync and async handlers are both supported
- non-`Response` values are converted to JSON
- CORS is permissive by default

If a change intentionally breaks one of these assumptions, make that explicit in
the tests, `README.md`, and the relevant file in `docs/`.

## Dependency Changes

Runtime dependencies belong in `[project.dependencies]` in `pyproject.toml`.
Test and development-only dependencies belong in the `dev` dependency group.

After changing dependencies, run:

```bash
uv sync --all-extras --dev
uv run pytest
```

Commit both `pyproject.toml` and `uv.lock` when dependency resolution changes.

## Release-Sensitive Changes

Before preparing a release, verify:

- `uv run pytest` passes
- `uv build` produces a wheel and source distribution
- the package version in `pyproject.toml` is correct
- `README.md` still describes the current CLI and app contract
- new user-facing behavior has at least one test

Publishing is handled by the GitHub workflows in `.github/workflows/`.

## Documentation Expectations

Use this rule of thumb:

- User-facing behavior changes require `README.md` updates.
- Contributor workflow changes require `docs/development.md` updates.
- Architecture or ownership changes require `docs/architecture.md` updates.
- Test strategy changes require `docs/testing.md` updates.

Examples should stay small and runnable. Prefer one clear example per behavior
over a large example that tries to demonstrate everything.
