"""11 — FastAPI integration shape (no FastAPI required).

Demonstrates install_fastapi_logging using a tiny fake app so this example
runs without installing FastAPI. In a real app, just call:

    from fastapi import FastAPI
    from ultilog.integrations import install_fastapi_logging

    app = FastAPI()
    install_fastapi_logging(app)

Run:
    PYTHONPATH=src python examples/11_fastapi_shape.py
"""

from __future__ import annotations

from ultilog.integrations.fastapi import install_fastapi_logging


class FakeApp:
    def __init__(self) -> None:
        self.middlewares: list[tuple[str, str]] = []

    def middleware(self, kind: str):
        def decorator(func):
            self.middlewares.append((kind, func.__name__))
            return func

        return decorator


app = install_fastapi_logging(FakeApp())
print(app.middlewares)
