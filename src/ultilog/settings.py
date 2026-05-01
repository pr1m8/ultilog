"""Root settings for ``ultilog``.

Purpose
-------
Provide the root settings object used by bootstrap while keeping direct settings
construction optional for normal users.

Design
------
``UltilogSettings`` uses ``pydantic-settings`` for environment-driven overrides.
Nested settings use ``ULTILOG_`` as the prefix and ``__`` as the nested delimiter.
The public API can stay as simple as ``get_logger()`` while internals still use
strong typed configuration.

Attributes
----------
UltilogSettings:
    Root settings object for the package.

Examples
--------
>>> settings = UltilogSettings()
>>> settings.preset
'dev'
"""

from __future__ import annotations

import warnings
from importlib.util import find_spec
from typing import Any, Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ultilog.constants import DEFAULT_PRESET, ENV_PREFIX
from ultilog.models import (
    ContextSettings,
    LoggingSettings,
    OTelSettings,
    RichSettings,
    StructlogSettings,
)
from ultilog.models.presets import PresetName


class UltilogSettings(BaseSettings):
    """Root settings for ``ultilog``.

    Args:
        preset: Runtime preset name.
        logging: Standard library logging settings.
        rich: Rich handler settings.
        context: Runtime context settings.
        structlog: Optional structlog settings.
        otel: Optional OpenTelemetry settings.

    Returns:
        None.

    Raises:
        ValueError: If nested settings are invalid.

    Examples:
        >>> UltilogSettings(preset="test").logging.level
        'WARNING'
    """

    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX,
        env_nested_delimiter="__",
        extra="ignore",
    )

    preset: PresetName = DEFAULT_PRESET
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    rich: RichSettings = Field(default_factory=RichSettings)
    context: ContextSettings = Field(default_factory=ContextSettings)
    structlog: StructlogSettings = Field(default_factory=StructlogSettings)
    otel: OTelSettings = Field(default_factory=OTelSettings)

    @model_validator(mode="after")
    def apply_preset_defaults(self) -> Self:
        """Apply lightweight preset defaults.

        Args:
            None.

        Returns:
            The updated settings object.

        Raises:
            None.

        Examples:
            >>> UltilogSettings(preset="prod").logging.mode
            'json'
        """
        if self.preset == "test":
            if self.logging.level == "INFO":
                self.logging.level = "WARNING"
            self.logging.mode = "plain"
            self.rich.enabled = False
            self.rich.show_path = False
            self.context.include_in_text = False
        elif self.preset == "prod":
            self.logging.mode = "json"
            self.rich.enabled = False
            self.rich.show_path = False
            self.rich.rich_tracebacks = False
        elif self.preset == "dev":
            # Dev preset only enhances prettiness; defaults already produce
            # rich mode + enabled, so don't override them (so users can still
            # set mode="json" or rich.enabled=False at the dev preset).
            self.rich.rich_tracebacks = True
            self.rich.tracebacks_show_locals = True
        return self

    @model_validator(mode="after")
    def validate_combinations(self) -> Self:
        """Validate settings combinations and fix incompatible values.

        Args:
            None.

        Returns:
            The validated settings object.

        Raises:
            ValueError: If an optional dependency is enabled but not installed.

        Examples:
            >>> ls = LoggingSettings(mode="rich")
            >>> s = UltilogSettings(logging=ls, rich=RichSettings(enabled=False))
            >>> s.logging.mode
            'plain'
        """
        if self.logging.mode == "rich" and not self.rich.enabled:
            warnings.warn(
                "mode='rich' but rich.enabled=False; auto-setting mode to 'plain'",
                UserWarning,
                stacklevel=2,
            )
            self.logging.mode = "plain"

        if self.structlog.enabled and find_spec("structlog") is None:
            msg = "structlog.enabled=True but structlog is not installed"
            raise ValueError(msg)

        if self.otel.enabled and find_spec("opentelemetry") is None:
            msg = "otel.enabled=True but opentelemetry is not installed"
            raise ValueError(msg)

        return self

    @classmethod
    def from_overrides(cls, **overrides: Any) -> Self:
        """Create settings from ergonomic setup overrides.

        Args:
            **overrides: Flat user-facing setup overrides.

        Returns:
            A settings instance.

        Raises:
            ValueError: If overrides contain invalid values.

        Examples:
            >>> UltilogSettings.from_overrides(level="DEBUG").logging.level
            'DEBUG'
            >>> UltilogSettings.from_overrides(mode="json").logging.mode
            'json'
        """
        data: dict[str, Any] = {}
        overrides = dict(overrides)
        if "preset" in overrides and overrides["preset"] is not None:
            data["preset"] = overrides.pop("preset")

        logging_data: dict[str, Any] = {}
        rich_data: dict[str, Any] = {}
        context_data: dict[str, Any] = {}
        structlog_data: dict[str, Any] = {}
        otel_data: dict[str, Any] = {}

        logging_aliases = {"mode", "level", "force", "format", "stream", "include_context"}
        for key in list(overrides):
            value = overrides.pop(key)
            if key in logging_aliases:
                logging_data[key] = value
            elif key in RichSettings.model_fields:
                rich_data[key] = value
            elif key in ContextSettings.model_fields:
                context_data[key] = value
            elif key in StructlogSettings.model_fields:
                structlog_data[key] = value
            elif key in OTelSettings.model_fields:
                otel_data[key] = value
            else:
                data[key] = value

        if logging_data:
            data["logging"] = LoggingSettings(**logging_data)
        if rich_data:
            data["rich"] = RichSettings(**rich_data)
        if context_data:
            data["context"] = ContextSettings(**context_data)
        if structlog_data:
            data["structlog"] = StructlogSettings(**structlog_data)
        if otel_data:
            data["otel"] = OTelSettings(**otel_data)
        return cls(**data)


__all__ = ["UltilogSettings"]
