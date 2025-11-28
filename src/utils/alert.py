from pathlib import Path
from html import escape as html_escape

from jinja2 import Environment, FileSystemLoader

from src.models.graylog import WebhookPayload
from src.services.telegram import TelegramClient
from src.settings import settings
from src.utils import random
from src.utils.string import strip_whitespaces

telegram = TelegramClient(settings.telegram_token, settings.chat_id)


def render(template: str, params: dict) -> str:
    path = Path(__file__).parents[1]
    env = Environment(loader=FileSystemLoader(path / "templates"))

    return env.get_template(template).render(params)


async def send_alert(payload: WebhookPayload) -> None:
    fields = payload.event.fields

    limit = settings.message_max_len
    message = strip_whitespaces(fields.get("message", ""))

    if len(message) > limit:
        message = message[:limit] + " (truncated...)"

    await telegram.send(render("alert.j2", dict(
        fields=fields,
        message=html_escape(message),
        event=payload.event,
        backlog=payload.backlog,
        graylog_url=settings.graylog_url,
    )))


async def send_report(failed: int):
    await telegram.send(render("dropped.j2", dict(
        count=failed,
        quip=random.get_dropped_quip(),
    )))
