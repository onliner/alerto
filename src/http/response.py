from typing import Final

from aiohttp import web

STATUSES: Final = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    422: "Validation Failed",
}


def error_response(status: int, detail) -> web.Response:
    error = STATUSES.get(status, "Error")
    data = dict(error=error, detail=detail)
    return web.json_response(data, status=status)
