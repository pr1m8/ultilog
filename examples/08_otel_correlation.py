"""08 — OpenTelemetry trace/log correlation (auto-attached when available).

When the opentelemetry package is installed, ultilog automatically attaches
the TraceCorrelationFilter so log records carry trace_id and span_id when a
span is active. This works regardless of the logging mode.

Install with:
    pip install "ultilog[otel]"

Run:
    PYTHONPATH=src python examples/08_otel_correlation.py
"""

from __future__ import annotations

from ultilog import get_logger, setup_prod
from ultilog.otel.availability import otel_available

setup_prod(service_name="otel-demo")
log = get_logger("examples.otel")

if not otel_available():
    log.warning("otel.unavailable", extra={"hint": "pip install ultilog[otel]"})
else:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider

    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer("examples.otel")

    log.info("before.span")  # no trace_id yet
    with tracer.start_as_current_span("demo.span"):
        log.info("inside.span")  # trace_id and span_id present in JSON output
    log.info("after.span")
