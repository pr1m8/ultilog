"""Rich themes for ``ultilog``.

Purpose
-------
Define a small default Rich theme that can be shared by examples, CLIs, and
future console renderers.

Design
------
Theme names avoid coupling to internal logging implementation details so the
styles can be reused for diagnostics, tables, panels, and command output.

Examples
--------
>>> create_ultilog_theme().__class__.__name__
'Theme'
"""

from __future__ import annotations

from rich.theme import Theme


def create_ultilog_theme() -> Theme:
    """Create the default ultilog Rich theme.

    Args:
        None.

    Returns:
        Rich ``Theme``.

    Raises:
        None.

    Examples:
        >>> theme = create_ultilog_theme()
        >>> "ultilog.info" in theme.styles
        True
    """
    return Theme(
        {
            "ultilog.title": "bold cyan",
            "ultilog.info": "blue",
            "ultilog.success": "green",
            "ultilog.warning": "yellow",
            "ultilog.error": "bold red",
            "ultilog.muted": "dim",
            "ultilog.key": "bold magenta",
            "ultilog.value": "white",
        }
    )


__all__ = ["create_ultilog_theme"]
