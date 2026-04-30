"""Dictionary configuration builders for ``ultilog``.

Purpose
-------
Build standard-library ``logging.config.dictConfig`` payloads from typed
``ultilog`` settings.

Design
------
The initial package configures logging directly because that is easiest to
understand. This module exists for applications that prefer declarative logging
configuration, and it gives the project a clean bridge toward more advanced
handler graphs without changing the public API.

Attributes
----------
DEFAULT_SCHEMA_VERSION:
    The standard ``dictConfig`` schema version.

Examples
--------
.. code-block:: python

    from logging.config import dictConfig
    from ultilog.config.dictconfig import build_dict_config
    from ultilog.settings import UltilogSettings

    dictConfig(build_dict_config(UltilogSettings(preset="prod")))
"""

from __future__ import annotations

from typing import Any, Final

from ultilog.settings import UltilogSettings

DEFAULT_SCHEMA_VERSION: Final[int] = 1


def build_dict_config(settings: UltilogSettings) -> dict[str, Any]:
    """Build a standard ``dictConfig`` payload.

    Args:
        settings: Resolved ``ultilog`` settings.

    Returns:
        Dictionary suitable for ``logging.config.dictConfig``.

    Raises:
        None.

    Examples:
        >>> payload = build_dict_config(UltilogSettings(preset="test"))
        >>> payload["version"]
        1
    """
    formatter_name = "json" if settings.logging.mode == "json" else "plain"
    handler_class = "logging.StreamHandler"
    stream = "ext://sys.stdout" if settings.logging.stream == "stdout" else "ext://sys.stderr"

    payload: dict[str, Any] = {
        "version": DEFAULT_SCHEMA_VERSION,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {"format": settings.logging.effective_format},
            "json": {"()": "ultilog.formatters.json.JsonFormatter"},
        },
        "handlers": {
            "console": {
                "class": handler_class,
                "stream": stream,
                "level": "NOTSET",
                "formatter": formatter_name,
            }
        },
        "root": {
            "level": settings.logging.level_value,
            "handlers": ["console"],
        },
    }
    return payload


__all__ = ["DEFAULT_SCHEMA_VERSION", "build_dict_config"]
