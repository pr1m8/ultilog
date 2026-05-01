"""Structlog processors for ``ultilog``.

Purpose
-------
Provide pre-built processor chains for common structlog configurations.

Design
------
Processors are returned as lists so ``configure_structlog`` can compose them
with user-supplied additions.  All helpers import structlog lazily.
"""

from __future__ import annotations

from typing import Any


def get_default_processors() -> list[Any]:
    """Return the default structlog processor chain.

    Args:
        None.

    Returns:
        List of structlog processors for a standard dev/console setup.

    Raises:
        RuntimeError: If structlog is not installed.

    Examples:
        >>> len(get_default_processors()) > 0  # doctest: +SKIP
        True
    """
    try:
        import structlog
    except ImportError as exc:
        raise RuntimeError("Install ultilog[structlog] for processor support.") from exc

    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.TimeStamper(fmt="iso"),
    ]


def get_json_processors() -> list[Any]:
    """Return processors suited for JSON / machine-readable output.

    Args:
        None.

    Returns:
        Processor list ending with JSONRenderer.

    Raises:
        RuntimeError: If structlog is not installed.

    Examples:
        >>> get_json_processors()[-1]  # doctest: +SKIP
        JSONRenderer(...)
    """
    try:
        import structlog
    except ImportError as exc:
        raise RuntimeError("Install ultilog[structlog] for processor support.") from exc

    base = get_default_processors()
    base.append(structlog.processors.dict_tracebacks)
    base.append(structlog.processors.JSONRenderer())
    return base


def get_console_processors() -> list[Any]:
    """Return processors suited for human-readable console output.

    Args:
        None.

    Returns:
        Processor list ending with ConsoleRenderer.

    Raises:
        RuntimeError: If structlog is not installed.

    Examples:
        >>> get_console_processors()[-1]  # doctest: +SKIP
        ConsoleRenderer(...)
    """
    try:
        import structlog
    except ImportError as exc:
        raise RuntimeError("Install ultilog[structlog] for processor support.") from exc

    base = get_default_processors()
    base.append(structlog.dev.ConsoleRenderer())
    return base


__all__ = ["get_console_processors", "get_default_processors", "get_json_processors"]
