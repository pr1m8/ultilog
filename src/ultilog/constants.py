"""Constants used by ``ultilog``.

Purpose
-------
Centralize small stable constants used throughout the package.

Design
------
Constants are intentionally plain values so importing this module has no side
effects.

Attributes
----------
DEFAULT_LOGGER_NAME:
    Fallback logger name when caller inference fails.
DEFAULT_PRESET:
    Default runtime preset.

Examples
--------
>>> DEFAULT_LOGGER_NAME
'ultilog'
"""

from __future__ import annotations

DEFAULT_LOGGER_NAME = "ultilog"
DEFAULT_PRESET = "dev"
ENV_PREFIX = "ULTILOG_"

__all__ = ["DEFAULT_LOGGER_NAME", "DEFAULT_PRESET", "ENV_PREFIX"]
