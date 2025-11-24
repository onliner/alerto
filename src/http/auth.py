import functools

from aiohttp import web

from src.http.response import error_response
from src.settings import settings


def require_auth(handler):
    @functools.wraps(handler)
    async def wrapper(request: web.Request):
        if not settings.auth_token:
            return await handler(request)

        header = request.headers.get("Authorization", "")
        if not header.lower().startswith("bearer "):
            return error_response(401, "Missing auth token")

        token = header.split(" ", 1)[1].strip()
        if token != settings.auth_token:
            return error_response(403, "Access denied")

        return await handler(request)

    return wrapper
