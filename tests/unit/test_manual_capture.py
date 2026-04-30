"""Tests for manual log capture utilities."""

from __future__ import annotations

import logging

from ultilog.testing.capture import capture_logs


def test_capture_logs_records_message() -> None:
    with capture_logs("capture.demo") as records:
        logging.getLogger("capture.demo").warning("captured")
    assert records[0].getMessage() == "captured"
