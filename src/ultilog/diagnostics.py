"""Diagnostics helpers for ``ultilog``.

Purpose
-------
Expose lightweight runtime diagnostics for examples, CLI smoke tests, and user
support.

Design
------
Diagnostics avoid importing optional integrations eagerly. They report package
runtime state and root logger configuration using only the standard library.

Examples
--------
>>> info = get_diagnostics()
>>> "configured" in info
True
"""

from __future__ import annotations

import logging
import os
import sys
from importlib.util import find_spec
from typing import Any

from ultilog.constants import ENV_PREFIX
from ultilog.state import runtime_state


def get_diagnostics() -> dict[str, Any]:
    """Return current ultilog diagnostics.

    Args:
        None.

    Returns:
        Dictionary with runtime and dependency information.

    Raises:
        None.

    Examples:
        >>> isinstance(get_diagnostics()["handlers"], list)
        True
    """
    root = logging.getLogger()
    handlers_info = []
    formatters_info = []
    for handler in root.handlers:
        handlers_info.append(type(handler).__name__)
        fmt = handler.formatter
        if fmt is not None:
            formatters_info.append(type(fmt).__name__)

    env_overrides = {
        key: value
        for key, value in os.environ.items()
        if key.startswith(ENV_PREFIX)
    }

    return {
        "active_preset": runtime_state.active_preset,
        "configured": runtime_state.configured,
        "explicit_setup": runtime_state.explicit_setup,
        "handlers": handlers_info,
        "formatters": formatters_info,
        "level": logging.getLevelName(root.level),
        "python_version": sys.version,
        "env_overrides": env_overrides,
        "optional_dependencies": _optional_dependency_info(),
    }


def _optional_dependency_info() -> dict[str, dict[str, Any]]:
    """Collect availability and version info for optional dependencies.

    Args:
        None.

    Returns:
        Dictionary mapping dependency names to status dictionaries.

    Raises:
        None.
    """
    deps: dict[str, dict[str, Any]] = {}
    for name in ("opentelemetry", "structlog", "httpx", "celery", "rq", "sqlalchemy"):
        available = find_spec(name) is not None
        version: str | None = None
        if available:
            try:
                from importlib.metadata import version as get_version

                version = get_version(name)
            except Exception:
                version = "unknown"
        deps[name] = {"available": available, "version": version}
    return deps


def validate_config() -> list[str]:
    """Validate current ultilog configuration and return any warnings.

    Args:
        None.

    Returns:
        List of warning messages.  Empty if configuration is valid.

    Raises:
        None.

    Examples:
        >>> isinstance(validate_config(), list)
        True
    """
    warnings: list[str] = []
    if not runtime_state.configured:
        warnings.append("ultilog has not been configured yet.")

    env_keys = [k for k in os.environ if k.startswith(ENV_PREFIX)]
    for key in env_keys:
        if key == ENV_PREFIX.rstrip("_"):
            warnings.append(f"Environment variable {key!r} has no setting name suffix.")

    return warnings


__all__ = ["get_diagnostics", "validate_config"]
