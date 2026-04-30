"""Tests for public API."""

from __future__ import annotations

import logging

from ultilog import get_logger, setup
from ultilog.state import runtime_state


def test_get_logger_configures_lazily() -> None:
    assert runtime_state.configured is False
    logger = get_logger("demo")
    assert logger.name == "demo"
    assert runtime_state.configured is True


def test_get_logger_without_name_infers_non_ultilog_module() -> None:
    logger = get_logger()
    assert logger.name == __name__


def test_get_logger_with_bind_values_returns_adapter() -> None:
    logger = get_logger("demo", component="test")
    assert isinstance(logger, logging.LoggerAdapter)
    assert logger.extra["component"] == "test"


def test_setup_configures_explicitly() -> None:
    setup(level="DEBUG", force=True)
    assert runtime_state.configured is True
    assert runtime_state.explicit_setup is True
    assert logging.getLogger().level == logging.DEBUG
