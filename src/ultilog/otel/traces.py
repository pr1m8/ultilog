"""OpenTelemetry traces helpers for future ``ultilog`` integration.

Purpose
-------
Reserve a module boundary for OpenTelemetry traces support.
"""

from __future__ import annotations


def configure_otel_traces() -> None:
    """Configure future OpenTelemetry traces support.

    Args:
        None

    Returns:
        None

    Raises:
        NotImplementedError: Always in Phase 1.

    Examples:
        .. code-block:: python

            # configure_otel_traces()
    """
    raise NotImplementedError("OpenTelemetry traces support is planned for a later phase.")


__all__ = ["configure_otel_traces"]
