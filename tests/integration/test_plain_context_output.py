"""Integration tests for plain text context output."""

from __future__ import annotations

from ultilog import get_logger, setup
from ultilog.context.managers import logging_context


def test_plain_mode_appends_context(capsys) -> None:  # type: ignore[no-untyped-def]
    setup(mode="plain", force=True)
    log = get_logger("integration.plain")
    with logging_context(job_id="job_1"):
        log.warning("job.started")
    output = capsys.readouterr().out
    assert "job.started" in output
    assert "job_id=job_1" in output
