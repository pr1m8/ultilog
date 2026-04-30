"""Preset resolution helpers for ``ultilog``."""

from __future__ import annotations

from ultilog.settings import UltilogSettings


def resolve_preset(name: str) -> UltilogSettings:
    """Resolve a preset name into settings.

    Args:
        name: Preset name.

    Returns:
        Settings for the preset.

    Raises:
        ValueError: If the preset is invalid.

    Examples:
        >>> resolve_preset("dev").preset
        'dev'
    """
    return UltilogSettings(preset=name)  # type: ignore[arg-type]


__all__ = ["resolve_preset"]
