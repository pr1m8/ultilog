"""LogRecord context injection for ``ultilog``.

Purpose
-------
Attach current contextvars data to each standard-library ``LogRecord``.

Design
------
The filter copies context values to safe record attributes and adds two stable
fields:

``ultilog_context``
    A dictionary of context values.

``ultilog_context_text``
    A compact text suffix suitable for simple log formats.

Examples
--------
>>> import logging
>>> record = logging.LogRecord("x", 20, __file__, 1, "msg", (), None)
>>> ContextFilter().filter(record)
True
"""

from __future__ import annotations

import logging
from typing import Any

from ultilog.context.vars import get_context

_RESERVED_RECORD_KEYS = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)


def format_context_text(context: dict[str, Any]) -> str:
    """Format context values as a compact suffix.

    Args:
        context: Context values.

    Returns:
        A suffix beginning with a single space, or an empty string when no
        context exists.

    Raises:
        None.

    Examples:
        >>> format_context_text({"request_id": "r1"})
        ' request_id=r1'
    """
    if not context:
        return ""
    parts = [f"{key}={value}" for key, value in sorted(context.items())]
    return " " + " ".join(parts)


class ContextFilter(logging.Filter):
    """Inject current ultilog context into log records.

    Args:
        include_attributes: Whether safe context keys should be copied to record
            attributes in addition to the aggregate context dictionary.
        include_text: Whether ``ultilog_context_text`` should include values.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> ContextFilter().__class__.__name__
        'ContextFilter'
    """

    def __init__(self, *, include_attributes: bool = True, include_text: bool = True) -> None:
        """Initialize the context filter.

        Args:
            include_attributes: Whether to copy safe keys onto records.
            include_text: Whether to render compact context text.

        Returns:
            None.

        Raises:
            None.
        """
        super().__init__()
        self.include_attributes = include_attributes
        self.include_text = include_text

    def filter(self, record: logging.LogRecord) -> bool:
        """Attach context to ``record``.

        Args:
            record: Log record being processed.

        Returns:
            Always ``True`` so the record continues through logging.

        Raises:
            None.
        """
        context = dict(get_context())
        record.ultilog_context = context
        record.ultilog_context_text = format_context_text(context) if self.include_text else ""
        if self.include_attributes:
            for key, value in context.items():
                if key.isidentifier() and key not in _RESERVED_RECORD_KEYS:
                    setattr(record, key, value)
        return True


__all__ = ["ContextFilter", "format_context_text"]
