"""OpenTelemetry logs helpers for future ``ultilog`` integration.

Purpose
-------
Reserve a module boundary for OpenTelemetry logs support.
"""

from __future__ import annotations


def configure_otel_logs() -> None:
    """Configure future OpenTelemetry logs support.

    Args:
        None

    Returns:
        None

    Raises:
        NotImplementedError: Always in Phase 1.

    Examples:
        .. code-block:: python

            # configure_otel_logs()
    """
    raise NotImplementedError("OpenTelemetry logs support is planned for a later phase.")


__all__ = ["configure_otel_logs"]
