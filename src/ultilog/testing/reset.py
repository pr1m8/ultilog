"""Reset helpers for ``ultilog`` tests.

Purpose
-------
Expose a public test helper for clearing package runtime state.
"""

from __future__ import annotations

from ultilog.state import runtime_state


def reset_ultilog() -> None:
    """Reset ``ultilog`` runtime state.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Examples:
        >>> reset_ultilog()
    """
    runtime_state.reset()


__all__ = ["reset_ultilog"]
