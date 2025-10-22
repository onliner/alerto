from aiohttp import web


async def healthz(_: web.Request) -> web.Response:
    return web.Response(text="ok")


async def readyz(_: web.Request) -> web.Response:
    return web.Response(text="ok")
