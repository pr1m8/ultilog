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
import os
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


def setup_dev(*, level: str = "DEBUG", force: bool = True, **overrides: Any) -> None:
    """One-line setup for local development with super-pretty Rich output.

    Uses the ``dev`` preset (Rich console, colored output) at DEBUG level by
    default so you see everything while iterating. Enables Rich tracebacks
    with local variables shown.

    Args:
        level: Logging level (defaults to ``DEBUG``).
        force: Whether to reconfigure if already configured (defaults to True).
        **overrides: Additional flat setting overrides.

    Returns:
        None.

    Examples:
        >>> setup_dev()
    """
    overrides.setdefault("rich_tracebacks", True)
    overrides.setdefault("tracebacks_show_locals", True)
    overrides.setdefault("show_path", True)
    overrides.setdefault("show_time", True)
    setup_logging(force=force, preset="dev", level=level, **overrides)


def setup_prod(
    *,
    level: str = "INFO",
    service_name: str | None = None,
    force: bool = True,
    **overrides: Any,
) -> None:
    """One-line setup for production.

    Uses the ``prod`` preset (JSON output, Rich disabled) at INFO level. When
    ``service_name`` is provided and the ``opentelemetry`` package is available,
    OTel trace/log correlation attaches automatically.

    Args:
        level: Logging level (defaults to ``INFO``).
        service_name: Optional service name for OTel resource attribution.
        force: Whether to reconfigure if already configured (defaults to True).
        **overrides: Additional flat setting overrides.

    Returns:
        None.

    Examples:
        >>> setup_prod(service_name="my-api")
    """
    if service_name is not None:
        overrides.setdefault("service_name", service_name)
    setup_logging(force=force, preset="prod", level=level, **overrides)


def setup_test(*, level: str = "WARNING", force: bool = True, **overrides: Any) -> None:
    """One-line setup for test suites.

    Uses the ``test`` preset (plain output, Rich disabled) at WARNING level so
    test output stays quiet unless something goes wrong.

    Args:
        level: Logging level (defaults to ``WARNING``).
        force: Whether to reconfigure if already configured (defaults to True).
        **overrides: Additional flat setting overrides.

    Returns:
        None.

    Examples:
        >>> setup_test()
    """
    setup_logging(force=force, preset="test", level=level, **overrides)


def setup_auto(
    *,
    service_name: str | None = None,
    env: str | None = None,
    level: str | None = None,
    force: bool = True,
    **overrides: Any,
) -> None:
    """Configure logging from the current application environment.

    Environment resolution checks ``ULTILOG_ENV``, ``APP_ENV``,
    ``ENVIRONMENT``, then ``ENV``. Production-like values use JSON production
    logging, test-like values use quiet plain logging, and everything else uses
    the Rich development setup.

    Args:
        service_name: Optional service name for production OTel attribution.
        env: Explicit environment name. Overrides environment variables.
        level: Optional log level override for the selected setup.
        force: Whether to reconfigure if already configured.
        **overrides: Additional flat setting overrides.

    Returns:
        None.

    Examples:
        >>> setup_auto(env="test")
    """
    resolved = _resolve_auto_environment(env)
    if resolved in {"prod", "production", "live"}:
        setup_prod(
            level=level or "INFO",
            service_name=service_name,
            force=force,
            **overrides,
        )
        return

    if resolved in {"test", "testing", "ci"}:
        setup_test(level=level or "WARNING", force=force, **overrides)
        return

    setup_dev(level=level or "DEBUG", force=force, **overrides)


def _resolve_auto_environment(env: str | None) -> str:
    """Resolve the environment name used by ``setup_auto``."""
    value = (
        env
        or os.getenv("ULTILOG_ENV")
        or os.getenv("APP_ENV")
        or os.getenv("ENVIRONMENT")
        or os.getenv("ENV")
        or "dev"
    )
    return value.strip().lower()


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
    "setup_auto",
    "setup_dev",
    "setup_prod",
    "setup_test",
]
