"""Tests for expanded CLI subcommands."""

from __future__ import annotations

from ultilog.__main__ import main


def test_show_config_returns_zero() -> None:
    assert main(["show-config"]) == 0


def test_validate_returns_int() -> None:
    result = main(["validate"])
    assert isinstance(result, int)
