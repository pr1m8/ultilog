"""OpenTelemetry exporters helpers for future ``ultilog`` integration.

Purpose
-------
Reserve a module boundary for OpenTelemetry exporters support.
"""

from __future__ import annotations


def configure_exporters() -> None:
    """Configure future OpenTelemetry exporters support.

    Args:
        None

    Returns:
        None

    Raises:
        NotImplementedError: Always in Phase 1.

    Examples:
        .. code-block:: python

            # configure_exporters()
    """
    raise NotImplementedError("OpenTelemetry exporters support is planned for a later phase.")


__all__ = ["configure_exporters"]
