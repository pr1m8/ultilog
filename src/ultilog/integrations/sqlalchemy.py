"""SQLAlchemy integration helpers for ``ultilog``.

Purpose
-------
Configure SQLAlchemy engine logging to flow through ultilog with context.

Design
------
The helper configures SQLAlchemy's ``sqlalchemy.engine`` logger to use
ultilog-managed logging levels without replacing the handler chain.
"""

from __future__ import annotations

import logging
from typing import Any

from ultilog.utils.import_tools import require_module


def install_sqlalchemy_logging(
    engine: Any,
    *,
    level: int = logging.WARNING,
    echo: bool = False,
) -> Any:
    """Configure SQLAlchemy engine logging through ultilog.

    Sets the ``sqlalchemy.engine`` logger level and optionally enables
    SQLAlchemy's built-in ``echo`` mode for query logging.

    Args:
        engine: A SQLAlchemy ``Engine`` instance.
        level: Logging level for ``sqlalchemy.engine``.
        echo: Whether to enable SQLAlchemy query echo (sets engine.echo).

    Returns:
        The same engine for fluent usage.

    Raises:
        UltilogOptionalDependencyError: If sqlalchemy is not installed.

    Examples:
        >>> install_sqlalchemy_logging(engine, level=logging.DEBUG)  # doctest: +SKIP
    """
    require_module("sqlalchemy", extra="sqlalchemy")

    sa_logger = logging.getLogger("sqlalchemy.engine")
    sa_logger.setLevel(level)

    if echo:
        engine.echo = True

    return engine


__all__ = ["install_sqlalchemy_logging"]
