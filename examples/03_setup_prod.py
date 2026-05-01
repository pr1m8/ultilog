"""03 — Production setup: JSON logs, optional OTel correlation.

setup_prod() emits structured JSON suitable for log aggregators. If the
opentelemetry package is installed, trace_id and span_id are auto-attached
to records when a span is active.

Run:
    PYTHONPATH=src python examples/03_setup_prod.py
"""

from __future__ import annotations

from ultilog import get_logger, logging_context, setup_prod

setup_prod(service_name="my-api")
log = get_logger("api")

with logging_context(request_id="req_abc", user_id="u_42"):
    log.info("request.received")
    log.info("request.processed")
