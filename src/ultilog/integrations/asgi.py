"""ASGI integration for ``ultilog``.

Purpose
-------
Provide a framework-neutral ASGI middleware that binds request context around an
application call.

Design
------
The middleware does not import FastAPI or Starlette. It uses the ASGI scope and
``ultilog`` context managers directly, making it useful as a low-level adapter
and a testable integration boundary.

Examples
--------
.. code-block:: python

    app = UltilogASGIMiddleware(app)
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from ultilog.context.managers import logging_context
from ultilog.context.request import request_context_values

type Scope = dict[str, Any]
type Receive = Callable[[], Awaitable[dict[str, Any]]]
type Send = Callable[[dict[str, Any]], Awaitable[None]]
type ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]


class UltilogASGIMiddleware:
    """Bind request context around an ASGI application.

    Args:
        app: ASGI application.
        request_id_header: Header name used to read request IDs.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> async def app(scope, receive, send):
        ...     return None
        >>> middleware = UltilogASGIMiddleware(app)
        >>> middleware.app is app
        True
    """

    def __init__(self, app: ASGIApp, *, request_id_header: bytes = b"x-request-id") -> None:
        """Initialize the middleware.

        Args:
            app: Wrapped ASGI application.
            request_id_header: Lowercase header name used for request IDs.

        Returns:
            None.

        Raises:
            None.
        """
        self.app = app
        self.request_id_header = request_id_header.lower()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Run the ASGI application inside a logging context.

        Args:
            scope: ASGI scope.
            receive: ASGI receive callable.
            send: ASGI send callable.

        Returns:
            None.

        Raises:
            Exception: Propagates errors from the wrapped app.
        """
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return
        headers = {key.lower(): value for key, value in scope.get("headers", [])}
        request_id = headers.get(self.request_id_header)
        context = request_context_values(
            method=scope.get("method"),
            path=scope.get("path"),
            request_id=request_id.decode() if isinstance(request_id, bytes) else request_id,
        )
        with logging_context(**context):
            await self.app(scope, receive, send)


def install_asgi_logging(
    app: ASGIApp, *, request_id_header: bytes = b"x-request-id"
) -> UltilogASGIMiddleware:
    """Wrap an ASGI app with ultilog request-context middleware.

    Args:
        app: ASGI application callable.
        request_id_header: Header name used to read request IDs.

    Returns:
        A middleware instance wrapping ``app``.
    """
    return UltilogASGIMiddleware(app, request_id_header=request_id_header)


__all__ = ["ASGIApp", "Receive", "Scope", "Send", "UltilogASGIMiddleware", "install_asgi_logging"]
