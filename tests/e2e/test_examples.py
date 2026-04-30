"""End-to-end tests for example scripts."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_example(name: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, str(ROOT / "examples" / name)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_zero_config_example_runs() -> None:
    result = run_example("01_zero_config.py")
    assert result.returncode == 0, result.stderr
    assert "zero_config.started" in result.stdout


def test_json_mode_example_runs_and_outputs_json() -> None:
    result = run_example("04_json_mode.py")
    assert result.returncode == 0, result.stderr
    assert '"message": "json_mode.event"' in result.stdout


def test_context_example_runs() -> None:
    result = run_example("05_context_scope.py")
    assert result.returncode == 0, result.stderr
    assert "request_id=req_example" in result.stdout
