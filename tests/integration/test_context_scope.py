"""Integration tests for context helpers."""

from __future__ import annotations

from ultilog.context.managers import logging_context
from ultilog.context.vars import get_context


def test_logging_context_restores_previous_values() -> None:
    assert dict(get_context()) == {}
    with logging_context(request_id="req_1"):
        assert dict(get_context()) == {"request_id": "req_1"}
    assert dict(get_context()) == {}
