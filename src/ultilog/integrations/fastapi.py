"""FastAPI integration helpers for ``ultilog``.

Purpose
-------
Provide an optional helper that installs the ASGI middleware on FastAPI or any
compatible Starlette-style application.

Design
------
This module avoids importing FastAPI at import time. The helper operates by
calling ``app.add_middleware`` if present, so tests can use a small fake app.

Examples
--------
.. code-block:: python

    install_fastapi_logging(app)
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast

from ultilog.context.managers import logging_context
from ultilog.context.request import request_context_values
from ultilog.integrations.asgi import UltilogASGIMiddleware

type HTTPMiddleware = Callable[..., Awaitable[Any]]
type MiddlewareRegistrar = Callable[[str], Callable[[HTTPMiddleware], HTTPMiddleware]]


def install_fastapi_logging(app: Any, *, request_id_header: bytes = b"x-request-id") -> Any:
    """Install ultilog request logging middleware on an app.

    Args:
        app: FastAPI or Starlette-style application with ``add_middleware``.
        request_id_header: Header used for request IDs.

    Returns:
        The same app object for fluent usage.

    Raises:
        AttributeError: If the app does not expose ``add_middleware``.

    Examples:
        >>> class App:
        ...     def __init__(self): self.items = []
        ...     def add_middleware(self, cls, **kwargs): self.items.append((cls, kwargs))
        >>> app = install_fastapi_logging(App())
        >>> len(app.items)
        1
    """
    add_middleware = getattr(app, "add_middleware", None)
    if callable(add_middleware):
        add_middleware(UltilogASGIMiddleware, request_id_header=request_id_header)
        return app

    middleware = getattr(app, "middleware", None)
    if callable(middleware):
        async def _ultilog_http_middleware(request: Any, call_next: Any) -> Any:
            scope = getattr(request, "scope", None)
            if isinstance(scope, dict):
                headers = {key.lower(): value for key, value in scope.get("headers", [])}
                request_id = headers.get(request_id_header.lower())
                context = request_context_values(
                    method=scope.get("method"),
                    path=scope.get("path"),
                    request_id=request_id.decode() if isinstance(request_id, bytes) else request_id,
                )
            else:
                context = request_context_values()

            with logging_context(**context):
                return await call_next(request)

        register = cast(MiddlewareRegistrar, middleware)
        register("http")(_ultilog_http_middleware)
        return app

    msg = "app must provide add_middleware(...) or middleware(...)"
    raise AttributeError(msg)


__all__ = ["install_fastapi_logging"]
