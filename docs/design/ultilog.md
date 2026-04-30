# ultilog design

`ultilog` is designed around a small public API and a layered implementation.

## Public API

```python
from ultilog import get_logger, setup
```

`get_logger()` should be enough for most users. `setup(...)` is optional and exists for early configuration.

## Runtime model

1. `get_logger()` calls lazy bootstrap.
2. Bootstrap resolves settings from defaults, environment, and optional overrides.
3. Logging is configured once unless `force=True` is used.
4. Runtime context is bound at request/job/task boundaries, not logger construction.

## Implemented scaffold

The current scaffold includes:

- standard-library root logging configuration
- Rich, plain, and JSON modes
- contextvars-backed scoped context
- log-record context injection
- diagnostics CLI
- examples and e2e tests

## Future layers

- structlog processor presets
- OpenTelemetry traces/logs/metrics
- framework integrations
- exporter adapters for OTLP, Jaeger, Loki, and Prometheus-oriented workflows
