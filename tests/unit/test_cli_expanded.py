"""Tests for expanded CLI subcommands."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from ultilog import project_bootstrap
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


def test_bootstrap_apply_requires_explicit_scope(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["bootstrap", "--apply", "--no-env-check"]) == 2
    output = capsys.readouterr().out
    assert "--group NAME or --all" in output


def test_bootstrap_commands_can_include_environment_repair(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    (tmp_path / "pdm.lock").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
dependencies = []
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(project_bootstrap, "_installed_packages", lambda: set())

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        return subprocess.CompletedProcess(
            args[0],
            1,
            stdout=(
                "opentelemetry-instrumentation-openai-v2 2.4b0 has requirement "
                "opentelemetry-util-genai>=0.4b0.dev, but you have "
                "opentelemetry-util-genai 0.2b0.\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(project_bootstrap.subprocess, "run", fake_run)

    assert main(["bootstrap", str(tmp_path), "--commands", "--check-environment"]) == 0

    output = capsys.readouterr().out
    assert "# Environment issue:" in output
    assert (
        "# Suggested repair: pdm run python -m pip install --upgrade "
        "'opentelemetry-util-genai>=0.4b0.dev'"
    ) in output
