"""Log capture utilities for users and internal tests.

Purpose
-------
Provide lightweight capture helpers that work with standard-library logging and
do not require pytest.

Design
------
The context manager temporarily attaches an in-memory handler to a logger and
restores prior state on exit.

Examples
--------
>>> import logging
>>> with capture_logs("demo") as records:
...     logging.getLogger("demo").warning("hello")
>>> records[0].getMessage()
'hello'
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager


class ListHandler(logging.Handler):
    """Logging handler that stores records in a list.

    Args:
        level: Handler level.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> handler = ListHandler()
        >>> handler.records
        []
    """

    def __init__(self, level: int = logging.NOTSET) -> None:
        """Initialize the list handler.

        Args:
            level: Handler level.

        Returns:
            None.

        Raises:
            None.
        """
        super().__init__(level=level)
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        """Store a record.

        Args:
            record: Log record.

        Returns:
            None.

        Raises:
            None.
        """
        self.records.append(record)


@contextmanager
def capture_logs(
    name: str | None = None, *, level: int = logging.DEBUG
) -> Iterator[list[logging.LogRecord]]:
    """Capture records emitted by a logger.

    Args:
        name: Logger name. ``None`` means the root logger.
        level: Temporary logger level.

    Returns:
        Iterator yielding captured records.

    Raises:
        None.

    Examples:
        >>> with capture_logs("x") as records:
        ...     logging.getLogger("x").error("boom")
        >>> records[0].levelname
        'ERROR'
    """
    logger = logging.getLogger(name)
    old_level = logger.level
    handler = ListHandler(level=level)
    logger.addHandler(handler)
    logger.setLevel(level)
    try:
        yield handler.records
    finally:
        logger.removeHandler(handler)
        logger.setLevel(old_level)


__all__ = ["ListHandler", "capture_logs"]
