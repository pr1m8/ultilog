"""Structlog processors for ``ultilog``.

Purpose
-------
Scaffold future structlog processors.
"""

from __future__ import annotations

def get_default_processors() -> list[object]:
    """Return default future structlog processors.

    Args:
        None

    Returns:
        Empty list in Phase 1.

    Raises:
        None

    Examples:
        >>> get_default_processors()
        []
    """
    return []


__all__ = ["get_default_processors"]
