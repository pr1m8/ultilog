"""OpenTelemetry trace setup for ``ultilog``.

Purpose
-------
Provide a lightweight helper that configures an OTel ``TracerProvider`` with
sensible defaults so applications can start emitting traces with minimal
boilerplate.

Design
------
All OTel imports are lazy.  When no OTLP endpoint is supplied the helper falls
back to a console exporter for local development.
"""

from __future__ import annotations

from typing import Any


def configure_otel_traces(
    *,
    service_name: str = "ultilog",
    endpoint: str | None = None,
) -> Any:
    """Configure an OpenTelemetry ``TracerProvider``.

    Args:
        service_name: Logical service name attached to spans.
        endpoint: Optional OTLP endpoint.  Defaults to console export.

    Returns:
        The configured ``TracerProvider``.

    Raises:
        RuntimeError: If the OpenTelemetry SDK is not installed.
    """
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import (
            BatchSpanProcessor,
            ConsoleSpanExporter,
        )
    except ImportError as exc:
        raise RuntimeError(
            "Install ultilog[otel] to enable OpenTelemetry trace support."
        ) from exc

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    if endpoint is not None:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # type: ignore[import-not-found]
                OTLPSpanExporter,
            )

            provider.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
            )
        except ImportError:
            provider.add_span_processor(
                BatchSpanProcessor(ConsoleSpanExporter())
            )
    else:
        provider.add_span_processor(
            BatchSpanProcessor(ConsoleSpanExporter())
        )

    trace.set_tracer_provider(provider)
    return provider


__all__ = ["configure_otel_traces"]
