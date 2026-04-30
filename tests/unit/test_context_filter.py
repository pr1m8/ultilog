"""Tests for context record injection."""

from __future__ import annotations

import logging

from ultilog.context.vars import bind_context, clear_context
from ultilog.records.context_filter import ContextFilter


def test_context_filter_adds_context_to_record() -> None:
    clear_context()
    bind_context(request_id="req_1")
    record = logging.LogRecord("demo", logging.INFO, __file__, 1, "hello", (), None)
    assert ContextFilter().filter(record) is True
    assert record.ultilog_context == {"request_id": "req_1"}
    assert record.request_id == "req_1"
    assert "request_id=req_1" in record.ultilog_context_text
