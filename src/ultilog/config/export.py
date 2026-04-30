"""Export helpers for effective logging configuration.

Purpose
-------
Provide serializable snapshots of active or proposed logging settings so users
can debug what ``ultilog`` is doing without reading bootstrap internals.

Design
------
Exports intentionally use plain dictionaries so they can be printed, serialized,
asserted in tests, or attached to support reports.

Examples
--------
>>> from ultilog.config.export import export_settings
>>> from ultilog.settings import UltilogSettings
>>> export_settings(UltilogSettings(preset="test"))["preset"]
'test'
"""

from __future__ import annotations

from typing import Any

from ultilog.settings import UltilogSettings


def export_settings(settings: UltilogSettings) -> dict[str, Any]:
    """Export settings to a plain dictionary.

    Args:
        settings: Settings to export.

    Returns:
        JSON-compatible dictionary.

    Raises:
        None.

    Examples:
        >>> data = export_settings(UltilogSettings(preset="prod"))
        >>> data["logging"]["mode"]
        'json'
    """
    return settings.model_dump(mode="json")


def summarize_settings(settings: UltilogSettings) -> dict[str, Any]:
    """Return a compact settings summary.

    Args:
        settings: Settings to summarize.

    Returns:
        Compact dictionary with the most important runtime choices.

    Raises:
        None.

    Examples:
        >>> summarize_settings(UltilogSettings())["mode"]
        'rich'
    """
    return {
        "preset": settings.preset,
        "mode": settings.logging.mode,
        "level": settings.logging.level,
        "rich_enabled": settings.rich.enabled,
        "context_enabled": settings.context.enabled,
        "structlog_enabled": settings.structlog.enabled,
        "otel_enabled": settings.otel.enabled,
    }


__all__ = ["export_settings", "summarize_settings"]
