"""Request context helpers for ``ultilog``.

Purpose
-------
Normalize common HTTP request metadata into logging context values.

Design
------
Framework integrations can call ``request_context_values`` with lightweight
attributes rather than depending on a concrete web framework.

Examples
--------
>>> request_context_values(method="GET", path="/health")["http.method"]
'GET'
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4


def request_context_values(
    *,
    method: str | None = None,
    path: str | None = None,
    request_id: str | None = None,
    client: str | None = None,
    user_agent: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Build normalized request context values.

    Args:
        method: HTTP method.
        path: Request path.
        request_id: Existing request ID. A new value is generated when omitted.
        client: Optional client identifier.
        user_agent: Optional user agent.
        **extra: Additional context values.

    Returns:
        Context dictionary.

    Raises:
        None.

    Examples:
        >>> data = request_context_values(method="POST", path="/items")
        >>> data["http.method"]
        'POST'
    """
    data: dict[str, Any] = {"request_id": request_id or str(uuid4())}
    if method is not None:
        data["http.method"] = method
    if path is not None:
        data["http.path"] = path
    if client is not None:
        data["client"] = client
    if user_agent is not None:
        data["user_agent"] = user_agent
    data.update(extra)
    return data


__all__ = ["request_context_values"]
