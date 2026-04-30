"""Configuration models for ``ultilog``.

Purpose
-------
Group typed configuration models used by settings and bootstrap layers.

Design
------
Models are split by domain so the root settings object remains small and future
integrations can grow independently.
"""

from ultilog.models.context import ContextSettings
from ultilog.models.logging import LoggingSettings
from ultilog.models.otel import OTelSettings
from ultilog.models.presets import PresetName
from ultilog.models.rich import RichSettings
from ultilog.models.structlog import StructlogSettings

__all__ = [
    "ContextSettings",
    "LoggingSettings",
    "OTelSettings",
    "PresetName",
    "RichSettings",
    "StructlogSettings",
]
