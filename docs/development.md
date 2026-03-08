# Development Guide

## Environment Setup

Stardust uses a standard Python package layout under `src/`.

Recommended setup:

```bash
uv sync --all-extras --dev
```

If you prefer plain `pip`, install the package in editable mode with the dev dependencies declared in `pyproject.toml`.

## Repository Structure

```text
src/stardust/          package source
tests/                 automated tests
examples/              runnable example apps
README.md              project overview
pyproject.toml         package metadata and dependencies
```

## Working on the Loader

Most subtle behavior lives in [`src/stardust/file_handler.py`](/Users/luke/Projects/stardust/src/stardust/file_handler.py).

Be careful with:

- module naming collisions in `sys.modules`
- package directory support
- imported versus local function detection
- deterministic function selection

If you change app discovery behavior, update tests in [`tests/test_handle_file.py`](/Users/luke/Projects/stardust/tests/test_handle_file.py).

## Working on the Framework Wrapper

Most HTTP behavior lives in [`src/stardust/stardust.py`](/Users/luke/Projects/stardust/src/stardust/stardust.py).

Common change categories:

- adding methods or routes
- changing middleware defaults
- extending response coercion
- changing handler invocation rules

Keep sync and async handlers working unless there is a deliberate breaking change.

## Working on the CLI

CLI behavior lives in [`src/stardust/cli.py`](/Users/luke/Projects/stardust/src/stardust/cli.py).

When adding flags:

- keep positional `file` behavior intact unless there is a strong reason not to
- update CLI tests
- document default values in `README.md`

## Backward Compatibility

The framework is small, so even minor edits can be user-visible. Treat these behaviors as compatibility-sensitive:

- default target path of `app.py`
- serving on `/`
- support for `GET` and `POST`
- first-function discovery
- JSON wrapping of non-`Response` return values
- permissive CORS

If a change intentionally breaks one of these assumptions, note it clearly in docs and tests.

## Documentation Expectations

When changing runtime behavior:

1. Update `README.md` if it affects users.
2. Update the relevant file in `docs/` if it affects developers.
3. Update or add tests that capture the new behavior.

This project is simple enough that documentation drift is avoidable. Keep the docs close to the code.
