"""Tests for context decorator helpers."""

from __future__ import annotations

from ultilog.context.decorators import with_logging_context
from ultilog.context.vars import get_context


def test_with_logging_context_binds_values_during_call() -> None:
    @with_logging_context(component="worker")
    def task() -> dict:
        return dict(get_context())

    result = task()
    assert result["component"] == "worker"


def test_with_logging_context_restores_after_call() -> None:
    @with_logging_context(component="worker")
    def task() -> None:
        pass

    task()
    assert "component" not in get_context()
