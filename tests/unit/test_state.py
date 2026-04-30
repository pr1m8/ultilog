"""Tests for runtime state."""

from __future__ import annotations

from ultilog.state import RuntimeState


def test_runtime_state_defaults() -> None:
    state = RuntimeState()
    assert state.configured is False
    assert state.explicit_setup is False
    assert state.active_preset == "dev"


def test_runtime_state_reset() -> None:
    state = RuntimeState(configured=True, explicit_setup=True, active_preset="prod")
    state.reset()
    assert state.configured is False
    assert state.explicit_setup is False
    assert state.active_preset == "dev"
