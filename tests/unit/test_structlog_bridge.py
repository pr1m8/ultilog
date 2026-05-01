"""Tests for structlog bridge availability check."""

from __future__ import annotations

from ultilog.structlog.bridge import bridge_enabled


def test_bridge_enabled_returns_bool() -> None:
    result = bridge_enabled()
    assert isinstance(result, bool)
