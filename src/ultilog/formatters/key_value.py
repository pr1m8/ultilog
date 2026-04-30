"""Key-value formatter for compact structured text logs.

Purpose
-------
Provide a small formatter that renders a stable ``key=value`` line without
requiring ``structlog``.

Design
------
This formatter is intentionally conservative. It uses ``LogRecord`` fields,
context injected by ``ContextFilter``, and optional extras. It is useful for
local debugging and for systems that prefer logfmt-like text over JSON.

Examples
--------
>>> import logging
>>> record = logging.LogRecord("demo", logging.INFO, __file__, 1, "hello", (), None)
>>> KeyValueFormatter().format(record)
'level=INFO logger=demo message=hello'
"""

from __future__ import annotations

import logging
from typing import Any

_RESERVED = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
    "message",
    "asctime",
}


def _quote(value: Any) -> str:
    """Return a safe key-value representation.

    Args:
        value: Value to represent.

    Returns:
        String representation suitable for a key-value log line.

    Raises:
        None.

    Examples:
        >>> _quote("hello world")
        '"hello world"'
    """
    text = str(value)
    if any(char.isspace() for char in text) or text == "":
        return repr(text).replace("'", '"')
    return text


class KeyValueFormatter(logging.Formatter):
    """Render records as compact key-value text.

    Args:
        include_context: Whether ``ultilog`` context values are included.
        include_extra: Whether non-standard record fields are included.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> isinstance(KeyValueFormatter(), logging.Formatter)
        True
    """

    def __init__(self, *, include_context: bool = True, include_extra: bool = True) -> None:
        """Initialize the formatter.

        Args:
            include_context: Whether to include context values.
            include_extra: Whether to include extra record attributes.

        Returns:
            None.

        Raises:
            None.
        """
        super().__init__()
        self.include_context = include_context
        self.include_extra = include_extra

    def format(self, record: logging.LogRecord) -> str:
        """Format a record.

        Args:
            record: Log record.

        Returns:
            Key-value text line.

        Raises:
            None.
        """
        values: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if self.include_context:
            values.update(getattr(record, "ultilog_context", {}) or {})
        if self.include_extra:
            values.update(self._extra(record))
        return " ".join(f"{key}={_quote(value)}" for key, value in values.items())

    def _extra(self, record: logging.LogRecord) -> dict[str, Any]:
        """Return non-reserved record values.

        Args:
            record: Log record.

        Returns:
            Extra attributes.

        Raises:
            None.
        """
        ignored = _RESERVED | {"ultilog_context", "ultilog_context_text"}
        return {
            key: value
            for key, value in record.__dict__.items()
            if key not in ignored and not key.startswith("_")
        }


__all__ = ["KeyValueFormatter"]
