"""Integration tests for ASGI middleware."""

from __future__ import annotations

import pytest

from ultilog.context.vars import get_context
from ultilog.integrations.asgi import UltilogASGIMiddleware


@pytest.mark.anyio
async def test_asgi_middleware_binds_request_context() -> None:
    observed = {}

    async def app(scope, receive, send):
        observed.update(get_context())

    async def receive():
        return {"type": "http.request"}

    async def send(message):
        return None

    middleware = UltilogASGIMiddleware(app)
    await middleware(
        {"type": "http", "method": "GET", "path": "/x", "headers": [(b"x-request-id", b"abc")]},
        receive,
        send,
    )
    assert observed["request_id"] == "abc"
    assert observed["http.method"] == "GET"
