"""Tests for public API."""

from __future__ import annotations

import logging

from ultilog import get_logger, setup, setup_auto
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


def test_setup_auto_uses_dev_by_default() -> None:
    setup_auto()

    assert runtime_state.active_preset == "dev"
    assert logging.getLogger().level == logging.DEBUG


def test_setup_auto_uses_prod_from_env(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("APP_ENV", "production")

    setup_auto(service_name="orders-api")

    assert runtime_state.active_preset == "prod"
    assert logging.getLogger().level == logging.INFO


def test_setup_auto_uses_test_from_explicit_env() -> None:
    setup_auto(env="test")

    assert runtime_state.active_preset == "test"
    assert logging.getLogger().level == logging.WARNING
