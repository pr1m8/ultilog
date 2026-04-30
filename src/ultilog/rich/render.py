"""Rich rendering helpers for diagnostics.

Purpose
-------
Render small diagnostic dictionaries with Rich without making Rich mandatory for
all callers that only want structured data.

Design
------
The helper accepts a console object for tests and callers that need deterministic
output. It is intentionally separate from logging handler creation.

Examples
--------
.. code-block:: python

    render_mapping({"configured": True})
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from rich.console import Console
from rich.table import Table


def build_mapping_table(data: Mapping[str, Any], *, title: str = "ultilog") -> Table:
    """Build a Rich table for mapping data.

    Args:
        data: Mapping to render.
        title: Table title.

    Returns:
        Rich ``Table`` instance.

    Raises:
        None.

    Examples:
        >>> table = build_mapping_table({"configured": True})
        >>> table.title
        'ultilog'
    """
    table = Table(title=title)
    table.add_column("Key", style="ultilog.key")
    table.add_column("Value", style="ultilog.value")
    for key, value in data.items():
        table.add_row(str(key), repr(value))
    return table


def render_mapping(
    data: Mapping[str, Any],
    *,
    console: Console | None = None,
    title: str = "ultilog",
) -> None:
    """Render mapping data to a Rich console.

    Args:
        data: Mapping to render.
        console: Optional console. A default console is created when omitted.
        title: Table title.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> render_mapping({"ok": True})
    """
    target = console or Console()
    target.print(build_mapping_table(data, title=title))


__all__ = ["build_mapping_table", "render_mapping"]
