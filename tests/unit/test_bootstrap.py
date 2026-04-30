"""Tests for bootstrap behavior."""

from __future__ import annotations

import logging

from ultilog.bootstrap import ensure_configured, setup_logging
from ultilog.state import runtime_state


def test_ensure_configured_is_idempotent() -> None:
    ensure_configured()
    first_handlers = list(logging.getLogger().handlers)
    ensure_configured()
    second_handlers = list(logging.getLogger().handlers)
    assert first_handlers == second_handlers


def test_setup_without_force_after_config_is_noop() -> None:
    ensure_configured()
    setup_logging(level="DEBUG", force=False)
    assert runtime_state.explicit_setup is False
