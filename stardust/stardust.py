import sys
from inspect import signature, iscoroutinefunction
from typing import Callable

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from stardust.responses import send


class Stardust:
    def __init__(self, fun: Callable = None, port=8000, debug=False):
        self.debug: bool = debug
        self.app = None
        self.port = port
        self.method = fun

        if not self.method:
            sys.stderr.write("File must contain at least one local function.")
            exit(1)

    async def __wrap_response(self, request: Request):
        call_if_params = (
            lambda method, req: method(req)
            if len(signature(method).parameters) > 0
            else method()
        )

        result = (
            await call_if_params(self.method, request)
            if iscoroutinefunction(self.method)
            else call_if_params(self.method, request)
        )

        # The app already returned a Response object
        if issubclass(result.__class__, Response):
            return result
        else:
            return send(result)

    def startup(self):
        sys.stdout.write(f"Stardust listening on {self.port} 🎉")

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
