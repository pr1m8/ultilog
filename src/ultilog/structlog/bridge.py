"""Structlog bridge for ``ultilog``.

Purpose
-------
Scaffold future structlog bridge.
"""

from __future__ import annotations

def bridge_enabled() -> bool:
    """Return whether the future structlog bridge is enabled.

    Args:
        None

    Returns:
        ``False`` in Phase 1.

    Raises:
        None

    Examples:
        >>> bridge_enabled()
        False
    """
    return False


__all__ = ["bridge_enabled"]
