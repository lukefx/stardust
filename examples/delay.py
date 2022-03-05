from asyncio import sleep


async def serve(req):
    await sleep(10)
    return {"hello": "world"}
