"""Text formatter helpers for ``ultilog``.

Purpose
-------
Provide small reusable helpers around standard text formatting.

Design
------
The package mostly relies on the standard library formatter. This module exists
for consistency and to provide a named factory for users who want to compose
handlers manually.

Examples
--------
>>> create_text_formatter()._style._fmt
'%(message)s'
"""

from __future__ import annotations

import logging


def create_text_formatter(
    fmt: str = "%(message)s", *, datefmt: str | None = None
) -> logging.Formatter:
    """Create a standard text formatter.

    Args:
        fmt: Standard logging format string.
        datefmt: Optional date format string.

    Returns:
        ``logging.Formatter`` instance.

    Raises:
        ValueError: If the format string is invalid during later formatting.

    Examples:
        >>> isinstance(create_text_formatter(), logging.Formatter)
        True
    """
    return logging.Formatter(fmt=fmt, datefmt=datefmt)


__all__ = ["create_text_formatter"]
