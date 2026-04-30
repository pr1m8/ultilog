"""ASGI middleware shape example.

Purpose
-------
Demonstrate how ``UltilogASGIMiddleware`` wraps an ASGI app without requiring
FastAPI or Starlette.

Examples
--------
.. code-block:: bash

    PYTHONPATH=src python examples/09_asgi_shape.py
"""

from __future__ import annotations

import asyncio

from ultilog import get_logger, setup
from ultilog.integrations.asgi import UltilogASGIMiddleware

setup(mode="plain", force=True)
log = get_logger("examples.asgi")


async def app(scope, receive, send):
    log.info("inside.asgi.app")
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"ok"})


async def main() -> None:
    sent = []

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
