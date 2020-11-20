from starlette.requests import Request


async def serve(req: Request):
    hello = req.query_params.get("hello", "world")
    return {"hello": hello}
