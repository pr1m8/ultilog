"""Tests for text formatter factory."""

from __future__ import annotations

import logging

from ultilog.formatters.text import create_text_formatter


def test_create_text_formatter_returns_formatter() -> None:
    fmt = create_text_formatter()
    assert isinstance(fmt, logging.Formatter)


def test_create_text_formatter_uses_custom_format() -> None:
    fmt = create_text_formatter(fmt="%(levelname)s: %(message)s")
    record = logging.LogRecord("test", logging.INFO, "", 0, "hello", (), None)
    assert fmt.format(record) == "INFO: hello"
