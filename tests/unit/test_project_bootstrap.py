"""Tests for project bootstrap planning."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ultilog import project_bootstrap
from ultilog.project_bootstrap import (
    apply_project_bootstrap_plan,
    build_project_bootstrap_plan,
    setup_snippet,
)


def test_bootstrap_plan_detects_otel_instrumentation_from_pyproject(
    tmp_path: Path,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
dependencies = ["fastapi>=0.115", "requests>=2"]

[project.optional-dependencies]
web = ["starlette>=0.45"]

[dependency-groups]
dev = ["pytest>=9"]
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        project_bootstrap,
        "_installed_packages",
        lambda: {"fastapi", "requests", "starlette", "opentelemetry-instrumentation"},
    )

    plan = build_project_bootstrap_plan(tmp_path)

    packages = {status.package for status in plan.otel_instrumentation_packages}
    assert "opentelemetry-instrumentation-asgi" in packages
    assert "opentelemetry-instrumentation-fastapi" in packages
    assert "opentelemetry-instrumentation-requests" in packages
    assert "opentelemetry-instrumentation-starlette" in packages
    assert plan.zero_code.requirements_command == "opentelemetry-bootstrap -a requirements"


def test_bootstrap_plan_uses_pdm_commands_when_pdm_lock_exists(
    tmp_path: Path,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    (tmp_path / "pdm.lock").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
dependencies = ["httpx>=0.28"]
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(project_bootstrap, "_installed_packages", lambda: {"httpx"})

    plan = build_project_bootstrap_plan(tmp_path)

    assert plan.package_manager == "pdm"
    assert plan.zero_code.install_command == "pdm run opentelemetry-bootstrap -a install"
    assert plan.commands["add_observability_core"].startswith(
        "pdm add --no-sync -G observability-core "
    )


def test_bootstrap_plan_recommends_type_stubs_for_detected_dependencies(
    tmp_path: Path,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
dependencies = ["requests>=2"]
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(project_bootstrap, "_installed_packages", lambda: {"requests"})

    plan = build_project_bootstrap_plan(tmp_path)

    assert any(status.package == "types-requests" for status in plan.type_stub_packages)
    assert "types-requests" in plan.commands["add_typing"]


def test_bootstrap_plan_groups_dev_tools_by_dependency_group(
    tmp_path: Path,
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

    plan = build_project_bootstrap_plan(tmp_path)

    assert plan.commands["add_formatting"] == "pdm add --no-sync -d -G formatting ruff"
    assert "pdm add --no-sync -d -G test-core" in plan.commands["add_test_core"]
    assert plan.commands["add_coverage"] == "pdm add --no-sync -d -G coverage coverage"


def test_setup_snippet_uses_auto_setup() -> None:
    snippet = setup_snippet(service_name="orders-api")

    assert 'setup_auto(service_name="orders-api")' in snippet
    assert "get_logger(__name__)" in snippet


def test_apply_project_bootstrap_plan_runs_selected_group(
    tmp_path: Path,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    (tmp_path / "pdm.lock").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
dependencies = ["requests>=2"]
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(project_bootstrap, "_installed_packages", lambda: {"requests"})
    calls: list[list[str]] = []

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        calls.append(args[0])
        return subprocess.CompletedProcess(args[0], 0, stdout="ok\n", stderr="")

    monkeypatch.setattr(project_bootstrap.subprocess, "run", fake_run)
    plan = build_project_bootstrap_plan(tmp_path)

    results = apply_project_bootstrap_plan(plan, groups={"typing"})

    assert len(results) == 1
    assert results[0].group == "typing"
    assert calls[0][:5] == ["pdm", "add", "--no-sync", "-d", "-G"]


def test_bootstrap_plan_reports_environment_conflicts(
    tmp_path: Path,
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

    plan = build_project_bootstrap_plan(tmp_path, check_environment=True)

    assert plan.environment_check is not None
    assert plan.environment_check.issues
    assert plan.environment_check.repair_commands == (
        "pdm run python -m pip install --upgrade 'opentelemetry-util-genai>=0.4b0.dev'",
    )
