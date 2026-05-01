"""Tests for dictConfig builder."""

from __future__ import annotations

from ultilog.config.dictconfig import build_dict_config
from ultilog.settings import UltilogSettings


def test_dict_config_has_version() -> None:
    payload = build_dict_config(UltilogSettings(preset="test"))
    assert payload["version"] == 1


def test_dict_config_json_mode_uses_json_formatter() -> None:
    payload = build_dict_config(UltilogSettings(preset="prod"))
    assert payload["handlers"]["console"]["formatter"] == "json"


def test_dict_config_plain_mode_uses_plain_formatter() -> None:
    payload = build_dict_config(UltilogSettings(preset="test"))
    assert payload["handlers"]["console"]["formatter"] == "plain"
