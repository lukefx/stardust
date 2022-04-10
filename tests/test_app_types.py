import pytest
from starlette.requests import Request
from starlette.testclient import TestClient

from stardust import Stardust
from stardust.responses import send, text, json


def test_json_app():
    async def serve():
        return {"hello": "world"}

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "hello" in response.json()


def test_json_app_with_request():
    async def serve(req):
        return {"hello": "world"}

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "hello" in response.json()


def test_json_app_with_request_and_send():
    async def serve(req):
        return send({"hello": "world"})

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "hello" in response.json()


def test_empty_content():
    async def serve():
        return

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 204


def test_custom_status_code():
    async def serve(req):
        return send({"Hello": "World"}, status_code=400)

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 400


def test_send_json():
    async def serve(req):
        return json({"hello": "world"})

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "world" in response.json()["hello"]


def test_response_plain_text():
    async def serve(req):
        return text("Hello World!")

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello" in response.text


def test_query_params():
    async def serve(req: Request):
        hello = req.query_params.get("hello", "all")
        return {"hello": hello}

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/?hello=world")
    assert response.status_code == 200
    assert "world" in response.json()["hello"]


def test_post_payload():
    async def echo(req: Request):
        body = await req.json()
        return body

    json = {"hello": "world"}

    app = Stardust(fun=echo).build()
    client = TestClient(app)
    response = client.post("/", json=json)
    assert response.status_code == 200
    assert json == response.json()


def test_headers_response():
    async def serve():
        return send(
            {"Hello": "World"},
            status_code=200,
            headers={"x-custom-header": "hello world"},
        )

    app = Stardust(fun=serve).build()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "x-custom-header" in response.headers
    assert "hello" in response.headers["x-custom-header"]


def test_empty_file(capsys):
    captured = capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        app = Stardust().build()
        assert captured.out == "File must contain at least one local function."
