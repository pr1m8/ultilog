"""Standard-library logging helpers."""

from __future__ import annotations

import logging


def get_root_logger() -> logging.Logger:
    """Return the root logger.

    Args:
        None

    Returns:
        The root logger.

    Raises:
        None

    Examples:
        >>> get_root_logger().name
        'root'
    """
    return logging.getLogger()


__all__ = ["get_root_logger"]
