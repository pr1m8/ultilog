"""FastAPI integration shape example.

This file intentionally does not require FastAPI to run. It demonstrates the
expected app-level call shape using a tiny fake app.
"""

from __future__ import annotations

from ultilog.integrations.fastapi import install_fastapi_logging


class FakeApp:
    def __init__(self) -> None:
        self.middlewares = []

    def middleware(self, kind: str):
        def decorator(func):
            self.middlewares.append((kind, func.__name__))
            return func
        return decorator


app = install_fastapi_logging(FakeApp())
print(app.middlewares)
