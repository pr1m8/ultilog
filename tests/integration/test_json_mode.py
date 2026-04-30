"""Integration tests for JSON logging mode."""

from __future__ import annotations

import json

from ultilog import get_logger, setup
from ultilog.context.managers import logging_context


def test_json_mode_outputs_context(capsys) -> None:  # type: ignore[no-untyped-def]
    setup(mode="json", force=True)
    log = get_logger("integration.json")
    with logging_context(request_id="req_json"):
        log.info("json.event")
    output = capsys.readouterr().out.strip()
    payload = json.loads(output)
    assert payload["message"] == "json.event"
    assert payload["context"] == {"request_id": "req_json"}
