"""Runtime state for ``ultilog``.

Purpose
-------
Define the small mutable runtime state used to coordinate package bootstrap.

Design
------
The state object tracks whether logging has already been configured and whether
that configuration came from explicit setup. A re-entrant lock guards lazy
bootstrap so repeated ``get_logger()`` calls do not install duplicate handlers.

Attributes
----------
runtime_state:
    Singleton runtime state used by the package.

Examples
--------
>>> state = RuntimeState()
>>> state.configured
False
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock

from ultilog.constants import DEFAULT_PRESET


@dataclass(slots=True)
class RuntimeState:
    """Mutable runtime state for ``ultilog``.

    Args:
        configured: Whether logging has already been configured.
        explicit_setup: Whether configuration came from an explicit setup call.
        active_preset: Name of the active preset.
        lock: Re-entrant lock used to guard bootstrap.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> state = RuntimeState(configured=True)
        >>> state.reset()
        >>> state.configured
        False
    """

    configured: bool = False
    explicit_setup: bool = False
    active_preset: str = DEFAULT_PRESET
    lock: RLock = field(default_factory=RLock)

    def reset(self) -> None:
        """Reset runtime state to its initial values.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Examples:
            >>> state = RuntimeState(configured=True, explicit_setup=True)
            >>> state.reset()
            >>> state.explicit_setup
            False
        """
        self.configured = False
        self.explicit_setup = False
        self.active_preset = DEFAULT_PRESET


runtime_state = RuntimeState()

__all__ = ["RuntimeState", "runtime_state"]
