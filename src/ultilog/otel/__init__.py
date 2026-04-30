"""Optional OpenTelemetry integration namespace for ``ultilog``."""

from ultilog.otel.availability import otel_available
from ultilog.otel.correlation import TraceCorrelationFilter

__all__ = ["TraceCorrelationFilter", "otel_available"]
