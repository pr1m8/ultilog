"""Tests for diagnostics helpers."""

from __future__ import annotations

from ultilog.diagnostics import get_diagnostics


def test_diagnostics_shape() -> None:
    info = get_diagnostics()
    assert "configured" in info
    assert "handlers" in info
    assert "optional_dependencies" in info
