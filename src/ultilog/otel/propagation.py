"""OpenTelemetry context propagation for ``ultilog``.

Purpose
-------
Configure W3C TraceContext / Baggage propagation so trace context flows
across service boundaries automatically.

Design
------
Imports are lazy.  The helper is a thin wrapper around the OTel SDK
propagation API.
"""

from __future__ import annotations

from typing import Any


def configure_otel_propagation(
    *,
    propagators: list[str] | None = None,
) -> Any:
    """Set up OpenTelemetry context propagation.

    Args:
        propagators: Optional list of propagator names.  When ``None``, uses
            the SDK defaults (W3C TraceContext + Baggage).

    Returns:
        The composite propagator that was installed.

    Raises:
        RuntimeError: If the OpenTelemetry SDK is not installed.
    """
    try:
        from opentelemetry import propagate
        from opentelemetry.baggage.propagation import W3CBaggagePropagator
        from opentelemetry.propagators.composite import CompositeHTTPPropagator
        from opentelemetry.propagators.textmap import TextMapPropagator
        from opentelemetry.trace.propagation.tracecontext import (
            TraceContextTextMapPropagator,
        )
    except ImportError as exc:
        raise RuntimeError(
            "Install ultilog[otel] to enable OpenTelemetry propagation."
        ) from exc

    if propagators is not None:
        from opentelemetry.propagators import _import_propagator  # type: ignore[attr-defined]

        instances: list[TextMapPropagator] = [_import_propagator(p) for p in propagators]
    else:
        instances = [TraceContextTextMapPropagator(), W3CBaggagePropagator()]

    composite = CompositeHTTPPropagator(instances)
    propagate.set_global_textmap(composite)
    return composite


__all__ = ["configure_otel_propagation"]
