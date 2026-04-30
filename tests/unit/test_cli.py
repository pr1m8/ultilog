"""Tests for command-line entry point."""

from __future__ import annotations

import json

from ultilog.__main__ import main


def test_doctor_json_outputs_diagnostics(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["doctor", "--json"]) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert "configured" in payload


def test_demo_command_runs() -> None:
    assert main(["demo", "--mode", "plain"]) == 0
