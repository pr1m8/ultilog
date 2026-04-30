"""Testing factories for ``ultilog``.

Purpose
-------
Create deterministic settings and records for tests without copying setup code.

Design
------
Factories stay dependency-light and return normal package objects.

Examples
--------
>>> make_test_settings().preset
'test'
"""

from __future__ import annotations

import logging

from ultilog.settings import UltilogSettings


def make_test_settings(**overrides: object) -> UltilogSettings:
    """Create test-friendly settings.

    Args:
        **overrides: Flat settings overrides.

    Returns:
        ``UltilogSettings`` instance.

    Raises:
        ValueError: If overrides are invalid.

    Examples:
        >>> make_test_settings(level="DEBUG").logging.level
        'DEBUG'
    """
    return UltilogSettings.from_overrides(preset="test", **overrides)


def make_log_record(
    *,
    name: str = "ultilog.test",
    level: int = logging.INFO,
    message: str = "event",
) -> logging.LogRecord:
    """Create a simple log record.

    Args:
        name: Logger name.
        level: Numeric log level.
        message: Log message.

    Returns:
        ``logging.LogRecord`` instance.

    Raises:
        None.

    Examples:
        >>> make_log_record(message="hello").getMessage()
        'hello'
    """
    return logging.LogRecord(name, level, __file__, 1, message, (), None)


__all__ = ["make_log_record", "make_test_settings"]
