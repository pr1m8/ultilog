"""OpenTelemetry availability helpers."""

from __future__ import annotations

from importlib.util import find_spec


def otel_available() -> bool:
    """Return whether OpenTelemetry appears importable.

    Args:
        None.

    Returns:
        ``True`` when the base OpenTelemetry package can be found.

    Raises:
        None.

    Examples:
        >>> isinstance(otel_available(), bool)
        True
    """
    return find_spec("opentelemetry") is not None


__all__ = ["otel_available"]
