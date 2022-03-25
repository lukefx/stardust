import typing

from starlette.responses import (
    JSONResponse,
    PlainTextResponse,
    Response,
    StreamingResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse,
)


def send(
    content: typing.Any = None,
    status_code: int = 200,
    headers: dict = None,
    media_type: str = None,
) -> Response:

    # Empty content
    if content is None:
        return Response(status_code=204)

    if isinstance(content, dict):
        # by default, we reply with json...
        return json(content, status_code, headers, media_type)

    elif isinstance(content, typing.AsyncIterable):
        return stream(content, status_code, headers, media_type)

    else:
        return Response(content, status_code, headers, media_type)


def json(
    content: typing.Any = None,
    status_code: int = 200,
    headers: dict = None,
    media_type: str = None,
):
    return JSONResponse(content, status_code, headers, media_type)


def text(
    content: typing.Any = None,
    status_code: int = 200,
    headers: dict = None,
    media_type: str = None,
):
    return PlainTextResponse(content, status_code, headers, media_type)


def stream(
    content: typing.Any = None,
    status_code: int = 200,
    headers: dict = None,
    media_type: str = None,
):
    return StreamingResponse(content, status_code, headers, media_type)


def html(
    content: str = None,
    status_code: int = 200,
    headers: dict = None,
    media_type: str = None,
):
    return HTMLResponse(content, status_code, headers, media_type)


def redirect(url: str):
    return RedirectResponse(url)


def file(path: str):
    return FileResponse(path)
