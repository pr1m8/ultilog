"""JSON logging mode example."""

from __future__ import annotations

from ultilog import get_logger, setup
from ultilog.context import logging_context

setup(mode="json", force=True)
log = get_logger("examples.json")

with logging_context(request_id="req_json_example"):
    log.info("json_mode.event")
