"""Tests for structlog renderer helpers."""

from __future__ import annotations

from ultilog.structlog.renderers import get_renderer_name


def test_json_mode_returns_json() -> None:
    assert get_renderer_name(mode="json") == "json"


def test_plain_mode_returns_key_value() -> None:
    assert get_renderer_name(mode="plain") == "key_value"


def test_rich_mode_returns_console() -> None:
    assert get_renderer_name(mode="rich") == "console"


def test_legacy_json_flag_true() -> None:
    assert get_renderer_name(True) == "json"


def test_legacy_json_flag_false() -> None:
    assert get_renderer_name(False) == "console"
