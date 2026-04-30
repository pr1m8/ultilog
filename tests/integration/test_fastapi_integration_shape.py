"""Tests for FastAPI middleware installer shape without importing FastAPI."""

from __future__ import annotations

from ultilog.integrations.fastapi import install_fastapi_logging


class FakeApp:
    def __init__(self) -> None:
        self.middlewares: list[tuple[str, object]] = []

    def middleware(self, kind: str):  # type: ignore[no-untyped-def]
        def decorator(func):  # type: ignore[no-untyped-def]
            self.middlewares.append((kind, func))
            return func
        return decorator


def test_fastapi_installer_registers_http_middleware() -> None:
    app = FakeApp()
    returned = install_fastapi_logging(app)
    assert returned is app
    assert app.middlewares[0][0] == "http"
