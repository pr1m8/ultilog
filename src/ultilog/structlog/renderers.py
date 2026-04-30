"""Structlog renderers for ``ultilog``.

Purpose
-------
Scaffold future structlog renderers.
"""

from __future__ import annotations

def get_renderer_name(json_logs: bool) -> str:
    """Return the intended renderer name.

    Args:
        json_logs: Whether JSON output is requested.

    Returns:
        Renderer name.

    Raises:
        None

    Examples:
        >>> get_renderer_name(True)
        'json'
    """
    return "json" if json_logs else "console"


__all__ = ["get_renderer_name"]
