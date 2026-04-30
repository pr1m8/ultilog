"""Pytest fixture helpers for downstream users.

Purpose
-------
Document and expose fixture-style helpers that downstream projects can wrap in
their own ``conftest.py`` files.

Design
------
This module intentionally avoids importing pytest so the runtime package does
not require pytest outside development environments.

Examples
--------
>>> callable(reset_logging_state)
True
"""

from __future__ import annotations

from ultilog.testing.reset import reset_ultilog


def reset_logging_state() -> None:
    """Reset logging state for a test.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> reset_logging_state()
    """
    reset_ultilog()


__all__ = ["reset_logging_state"]
