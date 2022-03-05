import inspect
import os
from importlib.machinery import SourceFileLoader
from inspect import getmembers
from typing import Any, Callable

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route


class Stardust:
    def __init__(self, file_path: str, port=5000, debug=False):
        self.debug: bool = debug
        self.app = None
        self.port = port
        self.module = None

        try:
            with open(file_path) as f:
                # exec(f.read(), {}, self.module)
                # self.load_module(file_path)
                # module_name = pathlib.Path(file_path)
                # self.module = importlib.import_module(module_name)
                # file_dir = os.path.dirname(file_path)
                # sys.path.append(file_dir)
                # exec(f.read(), globals(), self.module)

                # spec = importlib.util.spec_from_file_location("app", file_path)
                # self.module = importlib.util.module_from_spec(spec)
                # spec.loader.exec_module(self.module)

                self.module = SourceFileLoader("app", file_path).load_module()

        except FileNotFoundError:
            print("No such file or directory.")
            exit(1)

        self.method = self._find_async_function(self.module, file_path)
        if not self.method:
            print("File must contain at least one async function.")
            exit(1)

    @staticmethod
    def _find_async_function(module, file_path) -> Callable:
        method = None
        # getmembers returns a list of tuples
        for member in getmembers(module):
            name, item = member
            if (
                inspect.isfunction(item)
                and not inspect.isbuiltin(item)
                # we want to catch only local functions, not imported ones
                and os.path.samefile(item.__code__.co_filename, file_path)
            ):
                # if item.__module__ == module.__name__ and inspect.isfunction(item):
                method = item
        return method

    async def __wrap_response(self, request: Request) -> Any:

        # check if first params is type Request
        if len(inspect.signature(self.method).parameters) > 0:
            response = (
                await self.method(request)
                if inspect.iscoroutinefunction(self.method)
                else self.method(request)
            )
        else:
            response = (
                await self.method()
                if inspect.iscoroutinefunction(self.method)
                else self.method()
            )

        if not issubclass(response.__class__, Response):
            # by default, we reply with json...
            response = JSONResponse(response)
        return response

    def startup(self):
        print(f"Stardust listening on {self.port} 🎉")

    def build(self):

        middlewares = [
            Middleware(CORSMiddleware, allow_origins=["*"]),
        ]

        routes = [
            Route("/", self.__wrap_response, methods=["GET", "POST"]),
        ]

        self.app = Starlette(
            debug=self.debug,
            middleware=middlewares,
            routes=routes,
            on_startup=[self.startup],
        )

        return self.app
