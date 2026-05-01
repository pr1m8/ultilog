"""Tests for OTel trace correlation filter."""

from __future__ import annotations

import logging

from ultilog.otel.correlation import TraceCorrelationFilter


def test_trace_correlation_filter_sets_defaults() -> None:
    f = TraceCorrelationFilter()
    record = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
    result = f.filter(record)
    assert result is True
    assert record.trace_id is None  # type: ignore[attr-defined]
    assert record.span_id is None  # type: ignore[attr-defined]
