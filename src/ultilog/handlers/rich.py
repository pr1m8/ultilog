"""Rich logging handler factory.

Purpose
-------
Create a configured ``rich.logging.RichHandler`` without configuring global
logging state.

Design
------
Handler construction is separate from bootstrap so it can be tested and reused
independently.

Examples
--------
>>> handler = create_rich_handler()
>>> handler.__class__.__name__
'RichHandler'
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from types import ModuleType

from rich.console import Console
from rich.highlighter import Highlighter, ReprHighlighter
from rich.logging import RichHandler

from ultilog.models.rich import RichSettings


def create_rich_handler(
    *,
    settings: RichSettings | None = None,
    level: int = logging.NOTSET,
    console: Console | None = None,
    highlighter: Highlighter | None = None,
    tracebacks_suppress: Iterable[str | ModuleType] = (),
) -> RichHandler:
    """Create a configured ``RichHandler``.

    Args:
        settings: Rich handler settings. Defaults to ``RichSettings()``.
        level: Handler-level logging threshold.
        console: Optional Rich console instance.
        highlighter: Optional Rich highlighter.
        tracebacks_suppress: Modules, paths, or objects to suppress in tracebacks.

    Returns:
        A configured Rich logging handler.

    Raises:
        None

    Examples:
        >>> handler = create_rich_handler()
        >>> isinstance(handler, RichHandler)
        True
    """
    resolved = settings or RichSettings()
    return RichHandler(
        level=level,
        console=console,
        show_time=resolved.show_time,
        omit_repeated_times=resolved.omit_repeated_times,
        show_level=resolved.show_level,
        show_path=resolved.show_path,
        enable_link_path=resolved.enable_link_path,
        highlighter=highlighter or ReprHighlighter(),
        markup=resolved.markup,
        rich_tracebacks=resolved.rich_tracebacks,
        tracebacks_code_width=resolved.tracebacks_code_width,
        tracebacks_extra_lines=resolved.tracebacks_extra_lines,
        tracebacks_word_wrap=resolved.tracebacks_word_wrap,
        tracebacks_show_locals=resolved.tracebacks_show_locals,
        tracebacks_suppress=tracebacks_suppress,
        tracebacks_max_frames=resolved.tracebacks_max_frames,
        locals_max_length=resolved.locals_max_length,
        locals_max_string=resolved.locals_max_string,
        log_time_format=resolved.log_time_format,
    )


__all__ = ["create_rich_handler"]
