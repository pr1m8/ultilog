"""End-to-end tests for ``python -m ultilog``."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_python_m_ultilog_doctor_json() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run(
        [sys.executable, "-m", "ultilog", "doctor", "--json"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert "configured" in payload


def test_python_m_ultilog_bootstrap_downstream_project(tmp_path: Path) -> None:
    (tmp_path / "pdm.lock").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "downstream-demo"
version = "0.1.0"
dependencies = [
  "fastapi>=0.115",
  "requests>=2",
  "sqlalchemy>=2",
]

[dependency-groups]
test-core = ["pytest>=9"]
""",
        encoding="utf-8",
    )
    package_dir = tmp_path / "src" / "downstream_demo"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text("", encoding="utf-8")
    (package_dir / "app.py").write_text(
        """
import fastapi
import requests
import sqlalchemy

from ultilog import get_logger, setup_dev

setup_dev()
log = get_logger(__name__)
""",
        encoding="utf-8",
    )

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run(
        [sys.executable, "-m", "ultilog", "bootstrap", str(tmp_path), "--json"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["package_manager"] == "pdm"
    assert "fastapi" in payload["detected_dependencies"]
    assert "requests" in payload["detected_dependencies"]
    assert "sqlalchemy" in payload["detected_dependencies"]
    assert "add_observability_core" in payload["commands"]
    assert "opentelemetry-instrumentation-fastapi" in payload["commands"]["add_observability_core"]
    assert (
        "opentelemetry-instrumentation-requests"
        in payload["commands"]["add_observability_extra"]
    )
    assert (
        payload["zero_code"]["requirements_command"]
        == "pdm run opentelemetry-bootstrap -a requirements"
    )


def test_python_m_ultilog_bootstrap_commands_and_snippet(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "downstream-demo"
version = "0.1.0"
dependencies = ["requests>=2"]
""",
        encoding="utf-8",
    )

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    commands = subprocess.run(
        [sys.executable, "-m", "ultilog", "bootstrap", str(tmp_path), "--commands"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    snippet = subprocess.run(
        [
            sys.executable,
            "-m",
            "ultilog",
            "bootstrap",
            str(tmp_path),
            "--snippet",
            "--service-name",
            "orders-api",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert commands.returncode == 0, commands.stderr
    assert "opentelemetry-bootstrap -a requirements" in commands.stdout
    assert "opentelemetry-instrument python -m your_app" in commands.stdout
    assert snippet.returncode == 0, snippet.stderr
    assert 'setup_auto(service_name="orders-api")' in snippet.stdout
