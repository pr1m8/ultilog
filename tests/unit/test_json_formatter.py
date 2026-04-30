"""Tests for JSON formatter."""

from __future__ import annotations

import json
import logging

from ultilog.formatters.json import JsonFormatter


def test_json_formatter_includes_message_level_logger() -> None:
    record = logging.LogRecord("demo", logging.INFO, __file__, 1, "hello", (), None)
    rendered = JsonFormatter().format(record)
    payload = json.loads(rendered)
    assert payload["logger"] == "demo"
    assert payload["level"] == "INFO"
    assert payload["message"] == "hello"
