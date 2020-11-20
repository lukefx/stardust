from starlette.requests import Request


async def echo(req: Request):
    body = await req.json()
    return body
