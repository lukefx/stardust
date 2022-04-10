import asyncio
from asyncio import Future
from json import dumps
from unittest.mock import MagicMock

from stardust.responses import json, text, stream, html, redirect, file


def test_json_response():
    body = {"Hello": "World"}
    response = json(body)
    assert response
    assert response.media_type == "application/json"
    assert (
        response.body
        == dumps(
            body,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode()
    )


def test_text_response():
    body = "Hello World"
    response = text(body)
    assert response
    assert response.media_type == "text/plain"
    assert response.body == body.encode()


def test_stream_response(monkeypatch):
    def content_generator():
        for i in ["Hello", "World"]:
            yield i

    send = MagicMock(return_value=Future())
    send.return_value.set_result(123)

    response = stream(content_generator())
    asyncio.run(response.stream_response(send))

    assert send.called
    assert send.call_count == 4


def test_html_response():
    content = "<html><body>hello world</body></html>"
    response = html(content)
    assert response
    assert response.media_type == "text/html"
    assert response.body == content.encode()


def test_redirect_response():
    response = redirect("http://google.com")
    assert response
    assert response.status_code == 307
    assert "location" in response.headers
    assert response.headers.get("location") == "http://google.com"


def test_file_response(tmp_path):
    p = tmp_path / "greetings.mp3"
    p.write_text("Hello world")
    response = file(p.as_posix())
    assert response.status_code == 200
