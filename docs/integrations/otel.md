# OpenTelemetry Integration

ultilog provides optional [OpenTelemetry](https://opentelemetry.io/) integration for traces, logs, and metrics when the `otel` extra is installed.

## Install

```bash
pip install "ultilog[otel]"
```

## Traces

Configure a `TracerProvider` with sensible defaults:

```python
from ultilog.otel.traces import configure_otel_traces

provider = configure_otel_traces(service_name="my-api")
```

With an OTLP endpoint:

```python
provider = configure_otel_traces(
    service_name="my-api",
    endpoint="http://localhost:4317",
)
```

When no endpoint is specified, traces are exported to the console for local development.

## Logs

Forward stdlib log records to the OTel log pipeline:

```python
from ultilog.otel.logs import configure_otel_logs

provider = configure_otel_logs(service_name="my-api")
```

This installs an OTel `LoggingHandler` on the root logger (or a named logger):

```python
configure_otel_logs(
    service_name="my-api",
    logger_name="my.app",
    endpoint="http://localhost:4317",
)
```

## Metrics

Configure a `MeterProvider`:

```python
from ultilog.otel.metrics import configure_otel_metrics

provider = configure_otel_metrics(service_name="my-api")
```

## All-in-one setup

Configure multiple signals at once using `OTelSettings`:

```python
from ultilog.otel.exporters import configure_exporters
from ultilog.models.otel import OTelSettings

providers = configure_exporters(OTelSettings(
    enabled=True,
    service_name="my-api",
    endpoint="http://localhost:4317",
    traces_enabled=True,
    logs_enabled=True,
    metrics_enabled=True,
))
```

## Trace/log correlation

The `TraceCorrelationFilter` adds `trace_id` and `span_id` to log records when an active OTel span exists:

```python
from ultilog.otel.correlation import TraceCorrelationFilter

handler.addFilter(TraceCorrelationFilter())
# Log records now have trace_id and span_id attributes
```

## Context propagation

Set up W3C TraceContext and Baggage propagation:

```python
from ultilog.otel.propagation import configure_otel_propagation

configure_otel_propagation()
```

## Availability check

```python
from ultilog.otel.availability import otel_available

if otel_available():
    configure_otel_traces(service_name="my-api")
```

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `False` | Activate OTel integration |
| `service_name` | `"ultilog-app"` | Service name for resources |
| `endpoint` | `None` | OTLP endpoint (console fallback) |
| `traces_enabled` | `False` | Enable trace export |
| `metrics_enabled` | `False` | Enable metric export |
| `logs_enabled` | `False` | Enable log export |
| `inject_trace_ids` | `True` | Add trace/span IDs to log records |
