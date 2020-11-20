from starlette.responses import PlainTextResponse


async def serve(req):
    return PlainTextResponse("Hello World!")
