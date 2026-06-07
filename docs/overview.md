# Stardust Developer Overview

## Purpose

Stardust is intentionally narrow in scope. The library is not trying to be a full routing framework. Its core job is to turn one Python module into one HTTP endpoint with as little configuration as possible.

That design goal shapes the whole codebase:

- one entrypoint command
- one app loader
- one framework wrapper
- one route
- minimal implicit behavior

## High-Level Flow

Runtime flow from CLI to response:

1. `stardust.cli:main` parses CLI arguments.
2. `stardust.file_handler.handle()` loads the target file or package.
3. `handle()` returns the first local function found in the module.
4. `stardust.stardust.Stardust` validates the function and builds a Starlette app.
5. Uvicorn serves the app.
6. Requests to `/` are routed to the wrapped function for `GET` and `POST`.
7. Return values are normalized into Starlette responses.

## Public Surface Area

The public API is small:

- `stardust.Stardust`
- `stardust.InvalidApplicationError`
- `stardust` CLI command

There is no decorator system, routing DSL, or plugin interface yet. Most extension work today means changing the loader, the route configuration, or response normalization in core modules.

## Core Behaviors Developers Should Know

### Application Discovery

The loader imports either:

- a single Python file, or
- a package directory containing `__init__.py`

It then selects the first local function discovered by `inspect.getmembers()`. That means:

- selection is based on sorted member order, not source order
- multiple functions are allowed, but only the first discovered one is used
- imported functions are ignored unless they resolve as local to the loaded module namespace

This behavior is important because it is simple but implicit. Any changes here should be paired with explicit tests.

### Request Dispatch

Stardust checks the selected function signature:

- if the function has parameters, it receives the Starlette `Request`
- if it has no parameters, it is called with no arguments
- async and sync functions are both supported

### Response Normalization

If the handler returns a Starlette `Response` subclass, Stardust returns it directly. Otherwise, Stardust wraps the result in `JSONResponse`.

This is the main response contract today. There is no specialized coercion for bytes, iterators, streaming, or custom encoders beyond what Starlette already supports through `JSONResponse`.

### Built-In Middleware

The app currently installs only one middleware:

- `CORSMiddleware` with `allow_origins=["*"]`

This is intentionally permissive. If the project evolves toward production-focused defaults, this area is a likely candidate for configuration work.

## Current Limitations

- Only `/` is routed.
- Only `GET` and `POST` are enabled.
- Only one function is served.
- Function selection is implicit when multiple local functions exist.
- CORS configuration is not user-configurable.
- CLI configuration is limited to host, port, logging, and debug.

These are not necessarily bugs. They are part of the current product definition. Any expansion should keep the project’s minimalism in mind.
