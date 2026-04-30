"""Tests for key-value formatting."""

from __future__ import annotations

import logging

from ultilog.formatters.key_value import KeyValueFormatter


def test_key_value_formatter_includes_message() -> None:
    record = logging.LogRecord("demo", logging.INFO, __file__, 1, "hello world", (), None)
    text = KeyValueFormatter().format(record)
    assert "level=INFO" in text
    assert "logger=demo" in text
    assert 'message="hello world"' in text
