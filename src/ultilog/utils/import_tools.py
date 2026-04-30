"""Optional import helpers for ``ultilog``.

Purpose
-------
Centralize optional dependency checks so integrations can fail gracefully with a
clear message instead of raising surprising import errors.

Design
------
The functions return booleans or modules. They do not install dependencies or
perform network operations.

Examples
--------
>>> is_module_available("logging")
True
"""

from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from types import ModuleType

from ultilog.exceptions import UltilogOptionalDependencyError


def is_module_available(name: str) -> bool:
    """Return whether a module can be imported.

    Args:
        name: Module name.

    Returns:
        ``True`` if import machinery can find the module.

    Raises:
        None.

    Examples:
        >>> is_module_available("not_a_real_ultilog_dependency")
        False
    """
    return find_spec(name) is not None


def require_module(name: str, *, extra: str | None = None) -> ModuleType:
    """Import an optional dependency or raise a helpful package error.

    Args:
        name: Module name.
        extra: Optional package extra that provides the module.

    Returns:
        Imported module.

    Raises:
        UltilogOptionalDependencyError: If the module is unavailable.

    Examples:
        >>> require_module("logging").__name__
        'logging'
    """
    if not is_module_available(name):
        suffix = f" Install ultilog[{extra}]." if extra else ""
        raise UltilogOptionalDependencyError(f"Optional dependency {name!r} is not installed.{suffix}")
    return import_module(name)


__all__ = ["is_module_available", "require_module"]
