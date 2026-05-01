"""05 — Bind context at request/job boundaries.

logging_context attaches values to every record inside the scope and
restores the previous state on exit. Nesting is supported.

Run:
    PYTHONPATH=src python examples/05_context_scope.py
"""

from __future__ import annotations

from ultilog import get_logger, logging_context, setup

setup(mode="plain", force=True)
log = get_logger("examples.context")

log.info("outside_context")

with logging_context(request_id="req_example", user_id="u1"):
    log.info("inside_context")
    with logging_context(stage="validating"):
        log.info("nested_context")
    log.info("after_nested")

log.info("after_context")
