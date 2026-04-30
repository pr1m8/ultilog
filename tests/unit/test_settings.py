"""Tests for settings models."""

from __future__ import annotations

from ultilog.models.logging import LoggingSettings
from ultilog.settings import UltilogSettings


def test_logging_level_string_normalizes() -> None:
    assert LoggingSettings(level="debug").level == "DEBUG"
    assert LoggingSettings(level="debug").level_value == 10


def test_test_preset_changes_defaults() -> None:
    settings = UltilogSettings(preset="test")
    assert settings.logging.level == "WARNING"
    assert settings.rich.show_path is False


def test_flat_overrides_map_to_nested_settings() -> None:
    settings = UltilogSettings.from_overrides(level="DEBUG", show_path=False)
    assert settings.logging.level == "DEBUG"
    assert settings.rich.show_path is False
