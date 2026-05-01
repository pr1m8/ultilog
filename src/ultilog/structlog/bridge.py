"""Structlog bridge for ``ultilog``.

Purpose
-------
Determine whether ``ultilog`` should route logging through structlog or
through the standard library.

Design
------
The bridge is enabled when the ``structlog`` extra is installed **and** the
user has explicitly enabled it in settings.  This keeps the default behaviour
unchanged for applications that do not opt in.
"""

from __future__ import annotations

from importlib.util import find_spec


def bridge_enabled() -> bool:
    """Return whether structlog bridging is available.

    The bridge is considered available when the ``structlog`` package can be
    imported.  Actual activation still requires ``StructlogSettings.enabled``
    to be ``True``.

    Args:
        None.

    Returns:
        ``True`` when structlog is importable.

    Raises:
        None.

    Examples:
        >>> isinstance(bridge_enabled(), bool)
        True
    """
    return find_spec("structlog") is not None


__all__ = ["bridge_enabled"]
