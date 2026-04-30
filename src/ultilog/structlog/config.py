"""Optional structlog configuration helpers.

Purpose
-------
Provide a real integration point that degrades gracefully when ``structlog`` is
not installed.

Design
------
The function imports structlog lazily so core ``ultilog`` remains lightweight.
When available, it configures a small processor chain compatible with stdlib
logging.

Examples
--------
.. code-block:: python

    configure_structlog()
"""

from __future__ import annotations

from typing import Any

from ultilog.models.structlog import StructlogSettings


def configure_structlog(settings: StructlogSettings | None = None) -> None:
    """Configure structlog if the optional dependency is installed.

    Args:
        settings: Optional structlog settings.

    Returns:
        None.

    Raises:
        RuntimeError: If structlog is not installed.

    Examples:
        .. code-block:: python

            configure_structlog(StructlogSettings(enabled=True))
    """
    resolved = settings or StructlogSettings(enabled=True)
    try:
        import structlog as structlog_pkg
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError("Install ultilog[structlog] to enable structlog support.") from exc

    processors: list[Any] = [
        structlog_pkg.contextvars.merge_contextvars,
        structlog_pkg.stdlib.add_logger_name,
        structlog_pkg.stdlib.add_log_level,
        structlog_pkg.processors.TimeStamper(fmt="iso"),
    ]
    if resolved.renderer == "json":
        processors.append(structlog_pkg.processors.dict_tracebacks)
        processors.append(structlog_pkg.processors.JSONRenderer())
    elif resolved.renderer == "key_value":
        processors.append(structlog_pkg.processors.KeyValueRenderer())
    else:
        processors.append(structlog_pkg.dev.ConsoleRenderer())

    structlog_pkg.configure(
        processors=processors,
        wrapper_class=structlog_pkg.stdlib.BoundLogger,
        logger_factory=structlog_pkg.stdlib.LoggerFactory(),
        cache_logger_on_first_use=resolved.cache_logger_on_first_use,
    )


__all__ = ["configure_structlog"]
