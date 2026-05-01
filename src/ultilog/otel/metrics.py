"""OpenTelemetry metrics setup for ``ultilog``.

Purpose
-------
Provide a lightweight helper that configures an OTel ``MeterProvider`` so
applications can start recording metrics with minimal boilerplate.

Design
------
All OTel imports are lazy.  When no OTLP endpoint is supplied the helper falls
back to a console exporter.
"""

from __future__ import annotations

from typing import Any


def configure_otel_metrics(
    *,
    service_name: str = "ultilog",
    endpoint: str | None = None,
) -> Any:
    """Configure an OpenTelemetry ``MeterProvider``.

    Args:
        service_name: Logical service name attached to metrics.
        endpoint: Optional OTLP endpoint.  Defaults to console export.

    Returns:
        The configured ``MeterProvider``.

    Raises:
        RuntimeError: If the OpenTelemetry SDK is not installed.
    """
    try:
        from opentelemetry import metrics
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import (
            ConsoleMetricExporter,
            PeriodicExportingMetricReader,
        )
        from opentelemetry.sdk.resources import Resource
    except ImportError as exc:
        raise RuntimeError(
            "Install ultilog[otel] to enable OpenTelemetry metrics support."
        ) from exc

    resource = Resource.create({"service.name": service_name})

    if endpoint is not None:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (  # type: ignore[import-not-found]
                OTLPMetricExporter,
            )

            reader = PeriodicExportingMetricReader(
                OTLPMetricExporter(endpoint=endpoint)
            )
        except ImportError:
            reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    else:
        reader = PeriodicExportingMetricReader(ConsoleMetricExporter())

    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)
    return provider


__all__ = ["configure_otel_metrics"]
