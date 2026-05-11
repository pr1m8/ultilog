"""Tests for expanded CLI subcommands."""

from __future__ import annotations

import json

from ultilog.__main__ import main


def test_show_config_returns_zero() -> None:
    assert main(["show-config"]) == 0


def test_validate_returns_int() -> None:
    result = main(["validate"])
    assert isinstance(result, int)


def test_bootstrap_json_outputs_plan(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["bootstrap", "--json"]) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert "detected_dependencies" in payload
    assert "zero_code" in payload


def test_bootstrap_snippet_outputs_setup_code(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["bootstrap", "--snippet", "--service-name", "orders-api"]) == 0
    output = capsys.readouterr().out
    assert 'setup_auto(service_name="orders-api")' in output


def test_bootstrap_human_output_is_grouped(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["bootstrap"]) == 0
    output = capsys.readouterr().out
    assert "ultilog bootstrap" in output
    assert "Install Groups" in output
    assert "OpenTelemetry Zero-Code" in output
