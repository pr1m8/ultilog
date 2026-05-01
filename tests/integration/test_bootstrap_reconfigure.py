"""Tests for bootstrap reconfiguration behavior."""

from __future__ import annotations

import logging

from ultilog import get_logger, setup
from ultilog.state import runtime_state


def test_setup_with_force_reconfigures() -> None:
    setup(force=True, level="WARNING")
    assert runtime_state.configured is True

    setup(force=True, level="DEBUG")
    assert runtime_state.configured is True
    root = logging.getLogger()
    assert root.level == logging.DEBUG


def test_setup_without_force_after_config_is_noop() -> None:
    setup(force=True, level="WARNING")
    root = logging.getLogger()
    original_level = root.level

    setup(level="DEBUG")  # no force — should be noop
    assert root.level == original_level


def test_get_logger_after_setup_uses_configured_settings() -> None:
    setup(force=True, mode="plain", level="ERROR")
    log = get_logger("test.reconfigure")
    assert log.name == "test.reconfigure"
    assert logging.getLogger().level == logging.ERROR


def test_lazy_config_then_explicit_setup_with_force() -> None:
    get_logger("lazy.first")
    assert runtime_state.configured is True
    assert runtime_state.explicit_setup is False

    setup(force=True, level="CRITICAL")
    assert runtime_state.explicit_setup is True
    assert logging.getLogger().level == logging.CRITICAL
