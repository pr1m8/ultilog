"""JSON formatter helpers for production-oriented logging.

Purpose
-------
Format standard-library ``LogRecord`` instances as stable JSON payloads.

Design
------
The formatter includes a compact core schema and then folds in ultilog context
values that were injected by ``ContextFilter``.

Examples
--------
>>> JsonFormatter().__class__.__name__
'JsonFormatter'
"""

from __future__ import annotations

import json
import logging
from typing import Any

_RESERVED = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
    "message",
    "asctime",
}


class JsonFormatter(logging.Formatter):
    """Format log records as JSON.

    Args:
        include_extra: Whether non-standard LogRecord attributes should be
            included under the ``extra`` key.
        sort_keys: Whether JSON object keys should be sorted.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> isinstance(JsonFormatter(), logging.Formatter)
        True
    """

    def __init__(self, *, include_extra: bool = True, sort_keys: bool = True) -> None:
        """Initialize the formatter.

        Args:
            include_extra: Whether non-standard record fields are included.
            sort_keys: Whether JSON keys are sorted.

        Returns:
            None.

        Raises:
            None.
        """
        super().__init__()
        self.include_extra = include_extra
        self.sort_keys = sort_keys

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as JSON.

        Args:
            record: Log record to format.

        Returns:
            JSON string.

        Raises:
            TypeError: If record data cannot be serialized and ``default=str``
                cannot recover it.
        """
        context = getattr(record, "ultilog_context", {}) or {}
        payload: dict[str, Any] = {
            "context": dict(context),
            "extra": self._extra(record) if self.include_extra else {},
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, sort_keys=self.sort_keys)

    def _extra(self, record: logging.LogRecord) -> dict[str, Any]:
        """Return custom record fields.

        Args:
            record: Log record.

        Returns:
            Custom fields that are not part of standard ``LogRecord`` state.

        Raises:
            None.
        """
        ignored = _RESERVED | {"ultilog_context", "ultilog_context_text"}
        return {
            key: value
            for key, value in record.__dict__.items()
            if key not in ignored and not key.startswith("_")
        }


__all__ = ["JsonFormatter"]
