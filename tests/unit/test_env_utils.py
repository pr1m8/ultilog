"""Tests for environment utilities."""

from __future__ import annotations

from ultilog.utils.env import collect_ultilog_env, describe_env_prefix, is_ultilog_env_key


def test_is_ultilog_env_key() -> None:
    assert is_ultilog_env_key("ULTILOG_PRESET")
    assert not is_ultilog_env_key("PATH")


def test_collect_ultilog_env_filters_keys() -> None:
    assert collect_ultilog_env({"ULTILOG_PRESET": "test", "PATH": "x"}) == {
        "ULTILOG_PRESET": "test"
    }


def test_describe_env_prefix() -> None:
    assert "ULTILOG_" in describe_env_prefix()
