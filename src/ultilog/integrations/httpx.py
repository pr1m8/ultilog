"""httpx integration helpers for ``ultilog``.

Purpose
-------
Provide an httpx event hook that logs outgoing HTTP requests with ultilog
context.

Design
------
The helper returns a pair of event hooks (request / response) that can be
passed to an ``httpx.Client`` or ``httpx.AsyncClient``.  httpx is imported
lazily.
"""

from __future__ import annotations

import logging
from typing import Any

from ultilog.utils.import_tools import require_module

_log = logging.getLogger("ultilog.integrations.httpx")


def install_httpx_logging(client: Any) -> Any:
    """Install request/response logging hooks on an httpx client.

    Args:
        client: An ``httpx.Client`` or ``httpx.AsyncClient``.

    Returns:
        The same client for fluent usage.

    Raises:
        UltilogOptionalDependencyError: If httpx is not installed.

    Examples:
        >>> install_httpx_logging(client)  # doctest: +SKIP
    """
    require_module("httpx", extra="httpx")

    original_hooks = getattr(client, "event_hooks", {})
    request_hooks = list(original_hooks.get("request", []))
    response_hooks = list(original_hooks.get("response", []))

    def _log_request(request: Any) -> None:
        _log.debug(
            "http.request",
            extra={
                "http.method": str(request.method),
                "http.url": str(request.url),
            },
        )

    def _log_response(response: Any) -> None:
        _log.debug(
            "http.response",
            extra={
                "http.status_code": response.status_code,
                "http.url": str(response.request.url),
            },
        )

    request_hooks.append(_log_request)
    response_hooks.append(_log_response)
    client.event_hooks = {"request": request_hooks, "response": response_hooks}
    return client


__all__ = ["install_httpx_logging"]
