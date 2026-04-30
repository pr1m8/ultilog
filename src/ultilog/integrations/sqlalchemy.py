"""sqlalchemy integration helpers for ultilog.

Purpose
-------
Reserve a stable integration function for sqlalchemy while the full adapter matures.

Design
------
The current helper is a no-op pass-through so applications can safely wire it in
and upgrade behavior in a later package version.
"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def install_sqlalchemy_logging(target: T) -> T:
    """Return target unchanged.

    Args:
        target: Framework/client object.

    Returns:
        The same object.

    Raises:
        None.

    Examples:
        >>> obj = object()
        >>> install_sqlalchemy_logging(obj) is obj
        True
    """
    return target


__all__ = ["install_sqlalchemy_logging"]
