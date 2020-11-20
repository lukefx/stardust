from starlette.responses import Response


async def serve(req):
    return Response(status_code=204)
