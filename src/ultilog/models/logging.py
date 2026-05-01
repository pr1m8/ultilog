"""Standard logging settings for ``ultilog``.

Purpose
-------
Represent configuration that applies to Python's standard ``logging`` system.

Design
------
The model accepts string or integer log levels and exposes computed helpers for
runtime configuration. It intentionally keeps logging transport concerns close
to the standard library so later Rich, JSON, structlog, and OpenTelemetry layers
can compose around the same root logger.

Examples
--------
>>> settings = LoggingSettings(level="DEBUG")
>>> settings.level_value
10
"""

from __future__ import annotations

import logging
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

LogLevel = Annotated[str | int, Field(description="Logging level name or integer.")]
LogMode = Literal["rich", "plain", "json"]


class LoggingSettings(BaseModel):
    """Settings for standard library logging.

    Args:
        level: Logging threshold as a name or integer.
        force: Whether root logging configuration should replace existing handlers.
        format: Standard logging format string.
        mode: Output mode. ``"rich"`` uses RichHandler, ``"plain"`` uses a stream
            handler, and ``"json"`` uses the package JSON formatter.
        stream: Stream target name for stream-like handlers. Supported values are
            ``"stdout"`` and ``"stderr"``.
        include_context: Whether context values should be appended to rendered
            text logs when supported.

    Returns:
        None.

    Raises:
        ValueError: If the level, mode, or stream cannot be resolved.

    Examples:
        >>> LoggingSettings(level="INFO").level_value
        20
        >>> LoggingSettings(mode="json").mode
        'json'
    """

    model_config = ConfigDict(extra="forbid")

    level: LogLevel = "INFO"
    force: bool = False
    format: str = "%(message)s"
    mode: LogMode = "rich"
    stream: Literal["stdout", "stderr"] = "stdout"
    include_context: bool = True

    @field_validator("level")
    @classmethod
    def validate_level(cls, value: LogLevel) -> LogLevel:
        """Validate a logging level.

        Args:
            value: Candidate logging level.

        Returns:
            The original level value if valid. String values are normalized to
            uppercase names.

        Raises:
            ValueError: If the level cannot be resolved.

        Examples:
            >>> LoggingSettings(level="warning").level
            'WARNING'
        """
        if isinstance(value, int):
            if value < 0:
                raise ValueError("Logging level must be non-negative.")
            return value
        if value.upper() not in logging._nameToLevel:
            raise ValueError(f"Unknown logging level: {value!r}")
        return value.upper()

    @computed_field
    @property
    def level_value(self) -> int:
        """Return the numeric logging level.

        Returns:
            Numeric logging level.

        Raises:
            None.

        Examples:
            >>> LoggingSettings(level="ERROR").level_value
            40
        """
        if isinstance(self.level, int):
            return self.level
        return logging._nameToLevel[self.level.upper()]

    @computed_field
    @property
    def effective_format(self) -> str:
        """Return the active standard logging format string.

        Returns:
            Format string used by text-oriented handlers.

        Raises:
            None.

        Examples:
            >>> LoggingSettings(include_context=False).effective_format
            '%(message)s'
        """
        if self.mode == "json" or not self.include_context:
            return self.format
        if "%(ultilog_context_text)s" in self.format:
            return self.format
        return f"{self.format}%(ultilog_context_text)s"


__all__ = ["LogLevel", "LogMode", "LoggingSettings"]
