"""Tests for settings combination validation."""

from __future__ import annotations

import warnings

from ultilog.models.logging import LoggingSettings
from ultilog.models.rich import RichSettings
from ultilog.settings import UltilogSettings


def test_rich_mode_with_disabled_rich_falls_back_to_plain() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        settings = UltilogSettings(
            logging=LoggingSettings(mode="rich"),
            rich=RichSettings(enabled=False),
        )
    assert settings.logging.mode == "plain"
    assert len(w) == 1
    assert "mode='rich'" in str(w[0].message)


def test_valid_rich_mode_with_enabled_rich_no_warning() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        settings = UltilogSettings(
            logging=LoggingSettings(mode="rich"),
            rich=RichSettings(enabled=True),
        )
    assert settings.logging.mode == "rich"
    assert len(w) == 0


def test_prod_preset_sets_json_mode() -> None:
    settings = UltilogSettings(preset="prod")
    assert settings.logging.mode == "json"
    assert settings.rich.enabled is False


def test_test_preset_sets_plain_mode() -> None:
    settings = UltilogSettings(preset="test")
    assert settings.logging.mode == "plain"
    assert settings.rich.enabled is False
    assert settings.logging.level == "WARNING"


def test_dev_preset_keeps_rich_mode() -> None:
    settings = UltilogSettings(preset="dev")
    assert settings.logging.mode == "rich"
    assert settings.rich.enabled is True
