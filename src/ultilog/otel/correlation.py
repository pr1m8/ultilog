"""OpenTelemetry trace/log correlation helpers.

Purpose
-------
Provide optional helpers that can add trace identifiers to log records when
OpenTelemetry is installed and a span is active.

Design
------
The filter imports OpenTelemetry lazily and never fails logging if OTel is not
installed or no current span exists.
"""

from __future__ import annotations

import logging


class TraceCorrelationFilter(logging.Filter):
    """Attach trace and span IDs to records when available.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> TraceCorrelationFilter().__class__.__name__
        'TraceCorrelationFilter'
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Inject trace fields if an active OpenTelemetry span exists.

        Args:
            record: Log record.

        Returns:
            Always ``True``.

        Raises:
            None.
        """
        record.trace_id = None
        record.span_id = None
        try:
            from opentelemetry import trace
        except Exception:
            return True

        span = trace.get_current_span()
        context = span.get_span_context()
        if getattr(context, "is_valid", False):
            record.trace_id = f"{context.trace_id:032x}"
            record.span_id = f"{context.span_id:016x}"
        return True


__all__ = ["TraceCorrelationFilter"]
