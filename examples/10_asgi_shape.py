"""10 — ASGI middleware demo (no FastAPI/Starlette required).

Run:
    PYTHONPATH=src python examples/10_asgi_shape.py
"""

from __future__ import annotations

import asyncio

from ultilog import get_logger, setup_dev
from ultilog.integrations.asgi import UltilogASGIMiddleware

setup_dev(level="INFO")
log = get_logger("examples.asgi")


async def app(scope, receive, send):
    log.info("inside.asgi.app")  # context includes request_id, http.method, http.path
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"ok"})


async def main() -> None:
    sent: list[dict] = []

    async def receive():
        return {"type": "http.request", "body": b""}

    async def send(message):
        sent.append(message)

    wrapped = UltilogASGIMiddleware(app)
    await wrapped(
        {"type": "http", "method": "GET", "path": "/demo", "headers": []},
        receive,
        send,
    )
    print(sent)


if __name__ == "__main__":
    asyncio.run(main())
