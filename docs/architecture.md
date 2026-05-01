# Architecture

ultilog is split into a small public API and a larger internal composition layer.

## Public surface

```python
from ultilog import get_logger, setup, configure, logging_context
```

The goal is to make logging available immediately while allowing advanced configuration when needed.

## Runtime flow

```
get_logger() -> ensure_configured() -> UltilogSettings -> configure_basic_logging()
                     |                       |                      |
              check state.configured   resolve preset      create handler + filter
                     |                  apply env vars      install on root logger
              thread-safe (RLock)       validate combos     set level
```

1. `get_logger()` calls `ensure_configured()`.
2. `ensure_configured()` checks `runtime_state.configured` under a re-entrant lock.
3. If not configured, builds `UltilogSettings` from defaults and `ULTILOG_*` environment variables.
4. Preset defaults and combination validation are applied.
5. `configure_basic_logging()` creates the appropriate handler (Rich, stream, or JSON) and installs a `ContextFilter`.
6. A standard-library logger is returned.

## Module responsibilities

| Module | Role |
|--------|------|
| `api.py` | Thin public API -- delegates to bootstrap |
| `bootstrap.py` | Idempotent configuration orchestration |
| `state.py` | Mutable runtime state and lock |
| `settings.py` | Root `UltilogSettings` (pydantic-settings) |
| `models/` | Typed settings models for each subsystem |
| `config/` | Stdlib logging configuration, presets, dictConfig, export |
| `handlers/` | Handler factories (Rich, stream, file, queue) |
| `formatters/` | JSON, key-value, and text formatters |
| `context/` | `contextvars` storage, managers, decorators, request helpers |
| `records/` | `ContextFilter` for injecting context into log records |
| `integrations/` | Framework middleware (ASGI, FastAPI, Celery, httpx, RQ, SQLAlchemy) |
| `otel/` | OpenTelemetry setup (traces, logs, metrics, correlation, propagation) |
| `structlog/` | structlog configuration, processors, renderers, bridge |
| `rich/` | Console factory, themes, render helpers |
| `testing/` | Reset, capture, factories, fixtures |
| `utils/` | Caller inference, env helpers, import tools |

## Key design patterns

- **Lazy bootstrap** -- configuration on first use, not import time
- **Idempotent** -- reconfiguration requires `force=True`
- **Execution-scoped context** -- `contextvars`, not logger-time binding
- **Presets drive defaults** -- dev/test/prod apply mode and level rules
- **Optional deps degrade gracefully** -- extras for structlog, otel, web
- **Stdlib as spine** -- all logging flows through Python's logging module
