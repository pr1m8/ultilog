"""Tests for expanded diagnostics helpers."""

from __future__ import annotations

from ultilog.diagnostics import get_diagnostics, validate_config


def test_diagnostics_includes_formatters() -> None:
    info = get_diagnostics()
    assert "formatters" in info


def test_diagnostics_includes_env_overrides() -> None:
    info = get_diagnostics()
    assert "env_overrides" in info
    assert isinstance(info["env_overrides"], dict)


def test_diagnostics_includes_python_version() -> None:
    info = get_diagnostics()
    assert "python_version" in info


def test_diagnostics_optional_deps_have_version_info() -> None:
    info = get_diagnostics()
    for _dep_name, dep_info in info["optional_dependencies"].items():
        assert "available" in dep_info
        assert "version" in dep_info


def test_validate_config_unconfigured() -> None:
    warnings = validate_config()
    assert any("not been configured" in w for w in warnings)


def test_validate_config_after_setup() -> None:
    from ultilog import setup

    setup(force=True, preset="test")
    warnings = validate_config()
    assert not any("not been configured" in w for w in warnings)
