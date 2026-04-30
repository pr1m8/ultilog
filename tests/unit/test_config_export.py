"""Tests for settings export helpers."""

from __future__ import annotations

from ultilog.config.export import export_settings, summarize_settings
from ultilog.settings import UltilogSettings


def test_export_settings_contains_nested_data() -> None:
    settings = UltilogSettings(preset="prod")
    data = export_settings(settings)
    assert data["preset"] == "prod"
    assert data["logging"]["mode"] == "json"


def test_summarize_settings_is_compact() -> None:
    summary = summarize_settings(UltilogSettings(preset="test"))
    assert summary["preset"] == "test"
    assert summary["mode"] == "plain"
