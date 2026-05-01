"""Tests for OTel availability check."""

from __future__ import annotations

from ultilog.otel.availability import otel_available


def test_otel_available_returns_bool() -> None:
    assert isinstance(otel_available(), bool)
