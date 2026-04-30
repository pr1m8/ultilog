"""Public API for ``ultilog``.

Purpose
-------
Expose the small ergonomic API used by normal application code.

Design
------
``get_logger()`` lazily bootstraps logging and can infer the caller's module
name when no explicit logger name is provided. Context helpers are exposed for
request/job/task boundaries, but context is not bound at logger construction
time.

Examples
--------
>>> log = get_logger("demo")
>>> log.name
'demo'
"""

from __future__ import annotations

import logging
from typing import Any

from ultilog.bootstrap import configure_with_settings, ensure_configured, setup_logging
from ultilog.context.managers import logging_context
from ultilog.context.vars import bind_context, clear_context, get_context
from ultilog.settings import UltilogSettings
from ultilog.testing.reset import reset_ultilog
from ultilog.utils.caller import infer_caller_logger_name


def get_logger(
    name: str | None = None,
    **bind_values: object,
) -> logging.LoggerAdapter[Any] | logging.Logger:
    """Return a configured logger.

    Args:
        name: Optional logger name. If omitted, the caller module is inferred.
        **bind_values: Static context to attach using ``LoggerAdapter``.

    Returns:
        A standard logger or logger adapter.

    Raises:
        UltilogConfigurationError: If lazy bootstrap fails.

    Examples:
        >>> get_logger("my.module").name
        'my.module'
    """
    ensure_configured()
    logger = logging.getLogger(name or infer_caller_logger_name())
    if bind_values:
        return logging.LoggerAdapter(logger, bind_values)
    return logger


def setup(*, preset: str | None = None, force: bool = False, **overrides: Any) -> None:
    """Optionally configure ``ultilog`` before first logger use.

    Args:
        preset: Optional preset name.
        force: Whether to reconfigure if logging is already configured.
        **overrides: Flat settings overrides such as ``level`` or ``show_path``.

    Returns:
        None.

    Raises:
        UltilogConfigurationError: If configuration fails.

    Examples:
        >>> setup(force=True, level="DEBUG")
    """
    if preset is not None:
        overrides["preset"] = preset
    setup_logging(force=force, **overrides)


def configure(settings: UltilogSettings, *, force: bool = False) -> None:
    """Configure logging using an explicit settings object.

    This is the advanced path. Normal callers should use ``get_logger()`` or
    lightweight ``setup(...)``.

    Args:
        settings: Resolved settings object.
        force: Whether to reconfigure even if already configured.

    Returns:
        None.

    Raises:
        UltilogConfigurationError: If configuration fails.

    Examples:
        >>> configure(UltilogSettings(preset="test"), force=True)
    """
    configure_with_settings(settings, force=force)


def reset_logging() -> None:
    """Reset package and root logging state.

    This helper is intended for tests, notebooks, demos, and local experiments.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> reset_logging()
    """
    reset_ultilog()


__all__ = [
    "UltilogSettings",
    "bind_context",
    "clear_context",
    "configure",
    "get_context",
    "get_logger",
    "logging_context",
    "reset_logging",
    "setup",
]
