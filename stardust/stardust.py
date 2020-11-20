import inspect
from typing import Any, Callable

import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route


class Stardust:
    def __init__(self, file_path: str, port=5000):
        self.app = None
        self.port = port
        self.module = {}

        try:
            with open(file_path) as f:
                exec(f.read(), {}, self.module)
        except FileNotFoundError:
            print("No such file or directory.")
            exit(1)

        self.method = self._find_async_function(self.module)
        if not self.method:
            print("File must contain at least one async function.")
            exit(1)

    def _find_async_function(self, module) -> Callable:
        method = None
        for _property in self.module.keys():
            member = module[_property]
            if inspect.iscoroutinefunction(member) and not inspect.isbuiltin(member):
                method = module[_property]
        return method

    async def __wrap_response(self, request: Request) -> Any:
        response = await self.method(request)
        if not issubclass(response.__class__, Response):
            # by default we reply with json...
            response = JSONResponse(response)
        return response

    async def __status(request) -> Any:
        return JSONResponse({"status": "UP"})

    def startup(self):
        print(f"Stardust listening on {self.port} 🎉")

    def serve(self):

        middlewares = [
            Middleware(CORSMiddleware, allow_origins=["*"]),
        ]

        routes = [
            Route("/", self.__wrap_response, methods=["GET", "POST"]),
            Route("/status", self.__status),
        ]

        self.app = Starlette(
            debug=False,
            middleware=middlewares,
            routes=routes,
            on_startup=[self.startup],
        )

        uvicorn.run(self.app, port=self.port, access_log=False, log_level="error")
