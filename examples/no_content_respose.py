from stardust.responses import send


async def serve(req):
    return send(status_code=204)
