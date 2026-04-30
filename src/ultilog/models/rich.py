"""Rich handler settings for ``ultilog``.

Purpose
-------
Represent options passed to ``rich.logging.RichHandler``.

Design
------
Defaults favor a polished local-development console while avoiding unsafe Rich
markup parsing and noisy local-variable tracebacks.

Examples
--------
>>> RichSettings().show_time
True
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RichSettings(BaseModel):
    """Settings for Rich console logging.

    Args:
        enabled: Whether Rich console logging is enabled.
        show_time: Whether to show the time column.
        omit_repeated_times: Whether repeated times are visually collapsed.
        show_level: Whether to show the level column.
        show_path: Whether to show the source path column.
        enable_link_path: Whether paths should be clickable when supported.
        markup: Whether Rich markup is enabled in log messages.
        rich_tracebacks: Whether Rich tracebacks are enabled.
        tracebacks_show_locals: Whether tracebacks include local variables.
        log_time_format: Rich time format string.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> RichSettings(show_path=False).show_path
        False
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    show_time: bool = True
    omit_repeated_times: bool = True
    show_level: bool = True
    show_path: bool = True
    enable_link_path: bool = True
    markup: bool = False
    rich_tracebacks: bool = True
    tracebacks_show_locals: bool = False
    tracebacks_word_wrap: bool = True
    tracebacks_extra_lines: int = Field(default=3, ge=0)
    tracebacks_code_width: int = Field(default=100, ge=20)
    tracebacks_max_frames: int = Field(default=100, ge=1)
    locals_max_length: int = Field(default=10, ge=0)
    locals_max_string: int = Field(default=120, ge=0)
    log_time_format: str = "[%Y-%m-%d %H:%M:%S]"


__all__ = ["RichSettings"]
