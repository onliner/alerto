import json

from aiohttp import web
from pydantic import ValidationError

from src.http.auth import require_auth
from src.http.response import error_response
from src.models.graylog import WebhookPayload
from src.services.limiter import RateLimiter
from src.utils.alert import send_alert, send_report

limiter = RateLimiter()


@require_auth
async def graylog(request: web.Request) -> web.Response:
    try:
        data = await request.json()

        payload = WebhookPayload.model_validate(data)
    except json.JSONDecodeError:
        return error_response(400, "Invalid JSON")
    except ValidationError as e:
        return error_response(422, json.loads(e.json()))

    if not limiter.try_acquire():
        limiter.schedule_flush(send_report)
        return web.json_response({"status": "dropped"})

    await send_alert(payload)
    return web.json_response({"status": "ok"})
