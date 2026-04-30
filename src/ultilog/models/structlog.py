"""Structured logging settings for ``ultilog``.

Purpose
-------
Represent optional ``structlog`` integration settings without requiring the
optional dependency for core package imports.

Design
------
The model stays dependency-light. Runtime integration modules import structlog
lazily and degrade with actionable errors when the extra is not installed.

Examples
--------
>>> StructlogSettings().enabled
False
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

StructlogRenderer = Literal["console", "json", "key_value"]


class StructlogSettings(BaseModel):
    """Settings for optional structlog integration.

    Args:
        enabled: Whether structlog integration is enabled.
        renderer: Renderer used by structlog when enabled.
        cache_logger_on_first_use: Whether structlog should cache loggers.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> StructlogSettings(enabled=True).enabled
        True
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = False
    renderer: StructlogRenderer = "console"
    cache_logger_on_first_use: bool = True


__all__ = ["StructlogRenderer", "StructlogSettings"]
