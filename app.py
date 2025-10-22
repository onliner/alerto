import logging
from aiohttp import web

from src.http.webhook import graylog
from src.http.health import healthz, readyz

logging.basicConfig(level=logging.WARN)


app = web.Application()
app.add_routes([
    web.post("/", graylog),
    web.get("/healthz", healthz),
    web.get("/readyz", readyz),
])

if __name__ == "__main__":
    from src.settings import settings
    web.run_app(app, port=settings.port)
