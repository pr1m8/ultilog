"""Tests for caller inference."""

from __future__ import annotations

from ultilog.utils.caller import infer_caller_logger_name


def test_caller_inference_returns_current_test_module() -> None:
    assert infer_caller_logger_name() == __name__
