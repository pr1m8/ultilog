"""Bootstrap orchestration for ``ultilog``.

Purpose
-------
Coordinate lazy and explicit logging configuration.

Design
------
Bootstrap is protected by runtime state so logging configuration is installed at
most once unless explicit force reconfiguration is requested.

Examples
--------
>>> ensure_configured()
"""

from __future__ import annotations

from typing import Any

from ultilog.config.basic import configure_basic_logging
from ultilog.exceptions import UltilogConfigurationError
from ultilog.settings import UltilogSettings
from ultilog.state import runtime_state


def ensure_configured() -> None:
    """Configure logging lazily if it has not already been configured.

    Args:
        None

    Returns:
        None

    Raises:
        UltilogConfigurationError: If configuration fails.

    Examples:
        >>> ensure_configured()
    """
    if runtime_state.configured:
        return
    with runtime_state.lock:
        if runtime_state.configured:
            return
        _configure(UltilogSettings(), explicit=False, force=None)


def setup_logging(*, force: bool = False, **overrides: Any) -> None:
    """Explicitly configure logging with ergonomic overrides.

    Args:
        force: Whether to reconfigure even if logging is already configured.
        **overrides: Flat settings overrides such as ``level`` or ``show_path``.

    Returns:
        None

    Raises:
        UltilogConfigurationError: If configuration fails.

    Examples:
        >>> setup_logging(force=True, level="DEBUG")
    """
    with runtime_state.lock:
        if runtime_state.configured and not force:
            return
        settings = UltilogSettings.from_overrides(force=force, **overrides)
        _configure(settings, explicit=True, force=force)


def configure_with_settings(settings: UltilogSettings, *, force: bool = False) -> None:
    """Configure logging with an explicit settings object.

    Args:
        settings: Settings to apply.
        force: Whether to replace existing root handlers.

    Returns:
        None

    Raises:
        UltilogConfigurationError: If configuration fails.

    Examples:
        >>> configure_with_settings(UltilogSettings(), force=True)
    """
    with runtime_state.lock:
        if runtime_state.configured and not force:
            return
        _configure(settings, explicit=True, force=force)


def _configure(settings: UltilogSettings, *, explicit: bool, force: bool | None) -> None:
    """Apply resolved settings to the runtime.

    Args:
        settings: Resolved package settings.
        explicit: Whether setup was explicit.
        force: Optional root logging force override.

    Returns:
        None

    Raises:
        UltilogConfigurationError: If configuration fails.

    Examples:
        >>> _configure(UltilogSettings(), explicit=True, force=True)
    """
    try:
        configure_basic_logging(settings, force=force)
    except Exception as exc:  # pragma: no cover
        raise UltilogConfigurationError("Failed to configure ultilog.") from exc
    runtime_state.configured = True
    runtime_state.explicit_setup = explicit
    runtime_state.active_preset = settings.preset


__all__ = ["configure_with_settings", "ensure_configured", "setup_logging"]
