"""OpenTelemetry metrics helpers for future ``ultilog`` integration.

Purpose
-------
Reserve a module boundary for OpenTelemetry metrics support.
"""

from __future__ import annotations


def configure_otel_metrics() -> None:
    """Configure future OpenTelemetry metrics support.

    Args:
        None

    Returns:
        None

    Raises:
        NotImplementedError: Always in Phase 1.

    Examples:
        .. code-block:: python

            # configure_otel_metrics()
    """
    raise NotImplementedError("OpenTelemetry metrics support is planned for a later phase.")


__all__ = ["configure_otel_metrics"]
