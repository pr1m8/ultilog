"""OpenTelemetry settings for ``ultilog``.

Purpose
-------
Represent OpenTelemetry settings for future traces, logs, metrics, and
propagation without forcing OpenTelemetry imports during normal package import.

Design
------
OTel functionality is optional and activated by integration helpers. Settings
are intentionally explicit so the package can later map them to official OTel
providers, exporters, and instrumentation libraries.

Examples
--------
>>> OTelSettings(service_name="api").service_name
'api'
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class OTelSettings(BaseModel):
    """Settings for optional OpenTelemetry integration.

    Args:
        enabled: Whether OTel integration is enabled.
        service_name: Logical service name for telemetry resources.
        endpoint: Optional OTLP endpoint.
        traces_enabled: Whether traces are enabled.
        metrics_enabled: Whether metrics are enabled.
        logs_enabled: Whether OTel log export is enabled.
        inject_trace_ids: Whether trace and span IDs should be added to log records
            when a current span is available.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> OTelSettings(enabled=True).enabled
        True
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = False
    service_name: str = "ultilog-app"
    endpoint: str | None = None
    traces_enabled: bool = False
    metrics_enabled: bool = False
    logs_enabled: bool = False
    inject_trace_ids: bool = True


__all__ = ["OTelSettings"]
