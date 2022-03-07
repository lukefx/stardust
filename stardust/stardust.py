import os
from importlib.machinery import SourceFileLoader
from inspect import getmembers
from inspect import signature, isfunction, isbuiltin, iscoroutinefunction
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
                self.module = SourceFileLoader("app", file_path).load_module()

        except FileNotFoundError:
            print("No such file or directory.")
            exit(1)

        self.method = self._find_local_function(self.module, file_path)
        if not self.method:
            print("File must contain at least one local function.")
            exit(1)

    @staticmethod
    def _find_local_function(module, file_path) -> Callable:
        method = None
        # getmembers returns a list of tuples
        for member in getmembers(module):
            name, item = member
            if (
                isfunction(item)
                and not isbuiltin(item)
                # we want to catch only local functions, not imported ones
                and os.path.samefile(item.__code__.co_filename, file_path)
            ):
                method = item

        return method

    async def __wrap_response(self, request: Request) -> Any:
        call_if_params = (
            lambda method, req: method(req)
            if len(signature(method).parameters) > 0
            else method()
        )

        response = (
            await call_if_params(self.method, request)
            if iscoroutinefunction(self.method)
            else call_if_params(self.method, request)
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
