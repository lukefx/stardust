import inspect
import os
import sys
import tempfile

import pytest

from stardust.file_handler import handle


@pytest.fixture
def clean_module():
    if "stardust.app" in sys.modules:
        del sys.modules["stardust.app"]
    yield


def __write_app(tmp_path, app: str):
    p = tmp_path / tempfile.NamedTemporaryFile(suffix=".py").name
    p.write_text(app)
    return p.as_posix()


def test_simple_file(tmp_path, clean_module):
    app = """
    async def serve(req):
        return {"hello": "world"}
    """.strip()
    path = __write_app(tmp_path, app)

    fun = handle(path)
    assert inspect.isfunction(fun)
    assert fun.__name__ == "serve"


def test_import_lib(tmp_path, clean_module):
    app = """
from asyncio import sleep

async def serve(req):
    await sleep(1)
    return {"hello": "world1"}
    """.strip()
    path = __write_app(tmp_path, app)

    fun = handle(path)
    assert inspect.isfunction(fun)
    assert fun.__name__ == "serve"


def test_multiple_app(tmp_path, clean_module):
    app = """
async def serve1(req):
    return {"hello": "world1"}

async def serve2(req):
    return {"hello": "world2"}
    """.strip()
    path = __write_app(tmp_path, app)

    fun = handle(path)
    assert inspect.isfunction(fun)
    assert fun.__name__ == "serve1"


def test_module(tmp_path, clean_module):
    app_path = os.path.join(os.getcwd(), "tests", "test_file_handler")
    fun = handle(app_path)
    assert fun is not None
    assert inspect.isfunction(fun)
    assert fun.__name__ == "serve_1"


def test_no_local_function(tmp_path, clean_module):
    app = """
    # No function defined
    """.strip()
    path = __write_app(tmp_path, app)

    fun = handle(path)
    assert fun is None


def test_invalid_path(tmp_path, clean_module):
    # Create a path that is neither a file nor a directory
    path = tmp_path / "non_existent_path"

    with pytest.raises(ValueError, match="neither a file nor directory"):
        handle(path)


def test_directory_without_init(tmp_path, clean_module):
    # Create a directory without an __init__.py file
    path = tmp_path / "empty_dir"
    path.mkdir()

    with pytest.raises(FileNotFoundError, match="does not exist"):
        handle(path)
