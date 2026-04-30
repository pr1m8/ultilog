"""Basic standard-library logging configuration.

Purpose
-------
Configure Python's root logger for the active ``ultilog`` runtime.

Design
------
The function delegates handler construction to handler factories and keeps all
global logging mutation in one place. Rich, plain text, and JSON modes all flow
through standard-library logging so future OpenTelemetry log bridges can attach
to the same pipeline.

Examples
--------
>>> from ultilog.settings import UltilogSettings
>>> configure_basic_logging(UltilogSettings(preset="test"), force=True)
"""

from __future__ import annotations

import logging

from ultilog.formatters.json import JsonFormatter
from ultilog.handlers.rich import create_rich_handler
from ultilog.handlers.stream import create_stream_handler, resolve_stream
from ultilog.records.context_filter import ContextFilter
from ultilog.settings import UltilogSettings


def configure_basic_logging(settings: UltilogSettings, *, force: bool | None = None) -> None:
    """Configure Python's standard logging system.

    Args:
        settings: Resolved package settings.
        force: Optional override for root logging reconfiguration.

    Returns:
        None.

    Raises:
        ValueError: If settings are invalid.

    Examples:
        >>> configure_basic_logging(UltilogSettings(preset="test"), force=True)
    """
    handler = _create_handler(settings)
    if settings.context.enabled:
        handler.addFilter(
            ContextFilter(
                include_attributes=settings.context.include_in_records,
                include_text=settings.context.include_in_text and settings.logging.include_context,
            )
        )

    logging.basicConfig(
        level=settings.logging.level_value,
        format=settings.logging.effective_format,
        handlers=[handler],
        force=settings.logging.force if force is None else force,
    )


def _create_handler(settings: UltilogSettings) -> logging.Handler:
    """Create the active root handler.

    Args:
        settings: Resolved package settings.

    Returns:
        Configured logging handler.

    Raises:
        ValueError: If the configured mode is unsupported.
    """
    level = logging.NOTSET
    if settings.logging.mode == "rich" and settings.rich.enabled:
        return create_rich_handler(settings=settings.rich, level=level)

    handler = create_stream_handler(resolve_stream(settings.logging.stream), level=level)
    if settings.logging.mode == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter(settings.logging.effective_format))
    return handler


__all__ = ["configure_basic_logging"]
