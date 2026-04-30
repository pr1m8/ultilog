"""Scoped logging context example."""

from __future__ import annotations

from ultilog import get_logger, setup
from ultilog.context import logging_context

setup(mode="plain", force=True)
log = get_logger("examples.context")

log.info("outside_context")
with logging_context(request_id="req_example", user_id="u1"):
    log.info("inside_context")
log.info("after_context")
