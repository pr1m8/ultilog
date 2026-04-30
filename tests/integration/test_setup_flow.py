"""Integration tests for setup flow."""

from __future__ import annotations

import logging

from ultilog import get_logger, setup


def test_setup_then_get_logger_uses_configured_level() -> None:
    setup(level="ERROR", force=True)
    log = get_logger("integration.demo")
    assert log.name == "integration.demo"
    assert logging.getLogger().level == logging.ERROR
