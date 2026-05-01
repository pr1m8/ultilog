"""OpenTelemetry log bridge for ``ultilog``.

Purpose
-------
Install the OpenTelemetry logging handler so stdlib log records are forwarded
to the OTel log pipeline.

Design
------
The helper imports OTel lazily so core ultilog never depends on it at import
time.
"""

from __future__ import annotations

import logging
from typing import Any


def configure_otel_logs(
    *,
    service_name: str = "ultilog",
    endpoint: str | None = None,
    logger_name: str | None = None,
    level: int = logging.NOTSET,
) -> Any:
    """Install an OpenTelemetry log export handler on a stdlib logger.

    Args:
        service_name: Logical service name attached to exported logs.
        endpoint: Optional OTLP endpoint override.
        logger_name: Logger to attach the handler to.  ``None`` targets root.
        level: Minimum level for the OTel handler.

    Returns:
        The ``LoggerProvider`` that was configured.

    Raises:
        RuntimeError: If the OpenTelemetry SDK is not installed.
    """
    try:
        from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
        from opentelemetry.sdk._logs.export import (
            BatchLogRecordProcessor,
            ConsoleLogExporter,
        )
        from opentelemetry.sdk.resources import Resource
    except ImportError as exc:
        raise RuntimeError(
            "Install ultilog[otel] to enable OpenTelemetry log export."
        ) from exc

    resource = Resource.create({"service.name": service_name})
    provider = LoggerProvider(resource=resource)

    if endpoint is not None:
        try:
            from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (  # type: ignore[import-not-found]
                OTLPLogExporter,
            )

            provider.add_log_record_processor(
                BatchLogRecordProcessor(OTLPLogExporter(endpoint=endpoint))
            )
        except ImportError:
            provider.add_log_record_processor(
                BatchLogRecordProcessor(ConsoleLogExporter())
            )
    else:
        provider.add_log_record_processor(
            BatchLogRecordProcessor(ConsoleLogExporter())
        )

    handler = LoggingHandler(level=level, logger_provider=provider)
    target = logging.getLogger(logger_name)
    target.addHandler(handler)
    return provider


__all__ = ["configure_otel_logs"]
