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
from importlib.util import find_spec
from typing import Any

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
    return {
        "active_preset": runtime_state.active_preset,
        "configured": runtime_state.configured,
        "explicit_setup": runtime_state.explicit_setup,
        "handlers": [type(handler).__name__ for handler in root.handlers],
        "level": logging.getLevelName(root.level),
        "optional_dependencies": {
            "opentelemetry": find_spec("opentelemetry") is not None,
            "structlog": find_spec("structlog") is not None,
        },
    }


__all__ = ["get_diagnostics"]
