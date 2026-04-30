"""Stream handler helpers for ``ultilog``.

Purpose
-------
Create standard stream handlers with consistent defaults.

Design
------
The helper avoids global logging changes and returns a configured handler that
bootstrap can attach to the root logger.

Examples
--------
>>> create_stream_handler().__class__.__name__
'StreamHandler'
"""

from __future__ import annotations

import logging
import sys
from typing import TextIO


def resolve_stream(name: str) -> TextIO:
    """Resolve a stream name.

    Args:
        name: ``"stdout"`` or ``"stderr"``.

    Returns:
        Matching text stream.

    Raises:
        ValueError: If the stream name is unknown.

    Examples:
        >>> resolve_stream("stdout") is sys.stdout
        True
    """
    if name == "stdout":
        return sys.stdout
    if name == "stderr":
        return sys.stderr
    raise ValueError(f"Unknown stream: {name!r}")


def create_stream_handler(
    stream: TextIO | None = None,
    *,
    level: int = logging.NOTSET,
) -> logging.StreamHandler[TextIO]:
    """Create a stream handler.

    Args:
        stream: Stream to write to. Defaults to ``sys.stdout``.
        level: Handler log level.

    Returns:
        A standard stream handler.

    Raises:
        None.

    Examples:
        >>> create_stream_handler().__class__.__name__
        'StreamHandler'
    """
    handler: logging.StreamHandler[TextIO] = logging.StreamHandler(stream or sys.stdout)
    handler.setLevel(level)
    return handler


__all__ = ["create_stream_handler", "resolve_stream"]
