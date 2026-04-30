"""File handler factories for ``ultilog``.

Purpose
-------
Create standard file handlers without coupling file output to package bootstrap.

Design
------
The helpers return configured handler objects only. Higher-level modules decide
when and where those handlers are attached.

Examples
--------
.. code-block:: python

    handler = create_file_handler("app.log")
"""

from __future__ import annotations

import logging
from pathlib import Path


def create_file_handler(
    path: str | Path,
    *,
    level: int = logging.NOTSET,
    encoding: str = "utf-8",
    delay: bool = False,
) -> logging.FileHandler:
    """Create a file handler.

    Args:
        path: Destination log file path.
        level: Handler-level threshold.
        encoding: File encoding.
        delay: Whether to delay opening the file until first emit.

    Returns:
        Configured ``logging.FileHandler``.

    Raises:
        OSError: If the file cannot be opened when ``delay`` is false.

    Examples:
        >>> handler = create_file_handler("/tmp/ultilog-example.log", delay=True)
        >>> handler.level == logging.NOTSET
        True
    """
    handler = logging.FileHandler(Path(path), encoding=encoding, delay=delay)
    handler.setLevel(level)
    return handler


__all__ = ["create_file_handler"]
