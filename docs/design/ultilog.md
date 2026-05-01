# ultilog Design

ultilog is designed around a small public API and a layered implementation.

## Public API

```python
from ultilog import get_logger, setup, configure, logging_context
```

`get_logger()` is enough for most users. `setup(...)` is optional. `configure(settings)` is for advanced programmatic control.

## Runtime model

1. `get_logger()` calls lazy bootstrap.
2. Bootstrap resolves settings from defaults, environment variables, and optional overrides.
3. Logging is configured once unless `force=True` is used.
4. Runtime context is bound at request/job/task boundaries, not logger construction.

## Design principles

- **Stdlib as spine** -- all logging flows through Python's `logging` module
- **Lazy by default** -- no setup required for basic use
- **Idempotent** -- safe to call `get_logger()` from anywhere
- **Context at boundaries** -- `contextvars` for request/task scoping
- **Optional extras** -- structlog, OTel, and web frameworks are opt-in
- **Preset-driven** -- dev/test/prod presets apply sensible defaults

## Current implementation

- Standard-library root logging configuration
- Rich, plain, and JSON output modes
- `contextvars`-backed scoped context with managers and decorators
- Log record context injection via `ContextFilter`
- Pydantic v2 settings with environment variable overrides
- Framework integrations: ASGI, FastAPI, Celery, httpx, RQ, SQLAlchemy
- structlog processor chains and renderer helpers
- OpenTelemetry setup for traces, logs, metrics, and correlation
- CLI diagnostics, config export, and validation
- Comprehensive test suite with 79 tests across three layers
