"""Context settings for ``ultilog``.

Purpose
-------
Configure request/job/task context injection.

Design
------
Context values are stored in ``contextvars`` and copied onto log records by a
logging filter. This keeps context scoped to execution boundaries rather than
logger construction.

Examples
--------
>>> ContextSettings().enabled
True
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ContextSettings(BaseModel):
    """Settings for context propagation helpers.

    Args:
        enabled: Whether context helpers are enabled.
        include_in_records: Whether context values are attached to LogRecord
            instances.
        include_in_text: Whether text handlers append a compact context suffix.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> ContextSettings(include_in_text=False).include_in_text
        False
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    include_in_records: bool = True
    include_in_text: bool = True


__all__ = ["ContextSettings"]
