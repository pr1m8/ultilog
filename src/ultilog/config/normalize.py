"""Configuration normalization helpers."""

from __future__ import annotations

import logging


def normalize_level(level: str | int) -> int:
    """Normalize a logging level into an integer.

    Args:
        level: Level name or integer.

    Returns:
        Numeric logging level.

    Raises:
        ValueError: If the level is unknown.

    Examples:
        >>> normalize_level("INFO")
        20
    """
    if isinstance(level, int):
        return level
    try:
        return logging._nameToLevel[level.upper()]  # noqa: SLF001
    except KeyError as exc:
        raise ValueError(f"Unknown logging level: {level!r}") from exc


__all__ = ["normalize_level"]
