"""OpenTelemetry exporter configuration for ``ultilog``.

Purpose
-------
Provide a single entry point that configures log, trace, and metric exporters
according to ``OTelSettings``.

Design
------
Delegates to the individual ``configure_otel_*`` helpers.  When specific
signals are disabled in settings they are silently skipped.
"""

from __future__ import annotations

from typing import Any

from ultilog.models.otel import OTelSettings


def configure_exporters(settings: OTelSettings | None = None) -> dict[str, Any]:
    """Configure OTel exporters based on settings.

    Args:
        settings: OTel settings.  Defaults to ``OTelSettings(enabled=True)``.

    Returns:
        Dictionary mapping signal names to their configured providers.

    Raises:
        RuntimeError: If the OpenTelemetry SDK is not installed.
    """
    resolved = settings or OTelSettings(enabled=True)
    providers: dict[str, Any] = {}

    kwargs: dict[str, Any] = {"service_name": resolved.service_name}
    if resolved.endpoint:
        kwargs["endpoint"] = resolved.endpoint

    if resolved.traces_enabled:
        from ultilog.otel.traces import configure_otel_traces

        providers["traces"] = configure_otel_traces(**kwargs)

    if resolved.metrics_enabled:
        from ultilog.otel.metrics import configure_otel_metrics

        providers["metrics"] = configure_otel_metrics(**kwargs)

    if resolved.logs_enabled:
        from ultilog.otel.logs import configure_otel_logs

        providers["logs"] = configure_otel_logs(**kwargs)

    return providers


__all__ = ["configure_exporters"]
