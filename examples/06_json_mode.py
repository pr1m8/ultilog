"""06 — JSON output mode for structured logs.

Run:
    PYTHONPATH=src python examples/06_json_mode.py
"""

from __future__ import annotations

from ultilog import get_logger, logging_context, setup

setup(mode="json", force=True)
log = get_logger("examples.json")

with logging_context(request_id="req_json_example"):
    log.info("json_mode.event")
    log.warning("json_mode.warning", extra={"latency_ms": 42})
