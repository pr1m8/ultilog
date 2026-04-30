"""E2E tests for the demo app example."""

from __future__ import annotations

import subprocess
import sys


def test_demo_app_runs() -> None:
    result = subprocess.run(
        [sys.executable, "examples/10_demo_app.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "order.completed" in result.stdout
