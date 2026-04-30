"""OpenTelemetry propagation helpers for future ``ultilog`` integration.

Purpose
-------
Reserve a module boundary for OpenTelemetry propagation support.
"""

from __future__ import annotations


def configure_otel_propagation() -> None:
    """Configure future OpenTelemetry propagation support.

    Args:
        None

    Returns:
        None

    Raises:
        NotImplementedError: Always in Phase 1.

    Examples:
        .. code-block:: python

            # configure_otel_propagation()
    """
    raise NotImplementedError("OpenTelemetry propagation support is planned for a later phase.")


__all__ = ["configure_otel_propagation"]
