"""Pytest fixtures for ``ultilog``.

Purpose
-------
Keep logging state isolated across tests.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator

import pytest

from ultilog.testing.reset import reset_ultilog


@pytest.fixture(autouse=True)
def clean_logging_state(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Reset logging and environment state for every test.

    Args:
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        Iterator that yields to the test.

    Raises:
        None
    """
    root = logging.getLogger()
    old_handlers = list(root.handlers)
    old_level = root.level
    reset_ultilog()
    for key in list(__import__("os").environ):
        if key.startswith("ULTILOG_"):
            monkeypatch.delenv(key, raising=False)
    root.handlers.clear()
    root.setLevel(logging.NOTSET)
    yield
    root.handlers.clear()
    root.handlers.extend(old_handlers)
    root.setLevel(old_level)
    reset_ultilog()
