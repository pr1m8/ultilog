"""Rich console factories for ``ultilog``.

Purpose
-------
Centralize Rich ``Console`` construction so handler factories, examples, and
future CLIs can share consistent defaults.

Design
------
The function accepts a small set of commonly useful options but does not hide
Rich's own ``Console`` type from advanced users.

Examples
--------
>>> create_console().__class__.__name__
'Console'
"""

from __future__ import annotations

from rich.console import Console


def create_console(
    *,
    stderr: bool = False,
    force_terminal: bool | None = None,
    soft_wrap: bool = False,
    width: int | None = None,
) -> Console:
    """Create a Rich console.

    Args:
        stderr: Whether the console writes to stderr.
        force_terminal: Optional terminal-forcing flag.
        soft_wrap: Whether Rich should soft-wrap long lines.
        width: Optional fixed console width.

    Returns:
        Rich ``Console``.

    Raises:
        None.

    Examples:
        >>> console = create_console(width=100)
        >>> console.width == 100
        True
    """
    return Console(
        stderr=stderr,
        force_terminal=force_terminal,
        soft_wrap=soft_wrap,
        width=width,
    )


__all__ = ["create_console"]
