# ultilog

[![CI](https://github.com/pr1m8/ultilog/actions/workflows/ci.yml/badge.svg)](https://github.com/pr1m8/ultilog/actions/workflows/ci.yml)
[![Docs](https://github.com/pr1m8/ultilog/actions/workflows/docs.yml/badge.svg)](https://pr1m8.github.io/ultilog/)
[![PyPI](https://img.shields.io/pypi/v/ultilog)](https://pypi.org/project/ultilog/)
[![Python](https://img.shields.io/pypi/pyversions/ultilog)](https://pypi.org/project/ultilog/)
[![License](https://img.shields.io/github/license/pr1m8/ultilog)](https://github.com/pr1m8/ultilog/blob/main/LICENSE)

**Ergonomic Python logging** that starts with a tiny API and scales to structured observability.

```python
from ultilog import get_logger

log = get_logger()
log.info("app.started")
```

No explicit settings required. The package lazily configures logging on first access, installs a Rich console handler, and returns a standard-library logger.

## Install

```bash
pip install ultilog
```

With extras:

```bash
pip install "ultilog[structlog]"   # structlog processor bridge
pip install "ultilog[otel]"        # OpenTelemetry traces, logs, metrics
pip install "ultilog[web]"         # FastAPI / Starlette middleware
pip install "ultilog[full]"        # everything
```

## Quickstart

### Zero config

```python
from ultilog import get_logger

log = get_logger()
log.info("hello")
```

### One-line helpers

```python
from ultilog import setup_auto, setup_dev, setup_prod, setup_test, get_logger

setup_auto(service_name="my-api")       # env-aware: Rich dev, JSON prod, quiet tests
setup_dev()                           # super-pretty Rich, DEBUG, tracebacks with locals
setup_prod(service_name="my-api")     # JSON, INFO, OTel correlation auto-attached
setup_test()                          # plain WARNING, quiet test output

log = get_logger(__name__)
log.info("ready")
```

### Explicit naming

```python
log = get_logger(__name__)
log = get_logger("my.service")
```

### Custom setup

```python
from ultilog import setup

setup(level="DEBUG", mode="json", force=True)
```

### Presets

| Preset | Mode | Level | Rich |
|--------|------|-------|------|
| `dev` (default) | `rich` | INFO | Enabled, tracebacks + locals |
| `test` | `plain` | WARNING | Disabled |
| `prod` | `json` | INFO | Disabled |

```python
setup(preset="prod", force=True)
```

### OpenTelemetry auto-correlation

If the `opentelemetry` package is installed, ultilog auto-attaches a trace correlation filter so `trace_id` and `span_id` appear on log records inside any active span — no extra setup required. Install with:

```bash
pip install "ultilog[otel]"
```

## Modes

### Rich (default)

Pretty console output with colors, tracebacks, and path info.

```python
setup(mode="rich", force=True)
get_logger("demo").info("colored output")
```

### Plain

Simple stream logging for CI, containers, or piped output.

```python
setup(mode="plain", force=True)
get_logger("demo").info("plain output")
```

### JSON

Machine-readable JSON logs for production and log aggregators.

```python
setup(mode="json", force=True)
get_logger("api").info("request.finished")
# {"level": "INFO", "logger": "api", "message": "request.finished", ...}
```

## Context

Context belongs at runtime boundaries, not logger creation time. Use `logging_context` to bind values that appear in every log record within a scope:

```python
from ultilog import get_logger, logging_context

log = get_logger("worker")

with logging_context(job_id="job_1", queue="emails"):
    log.info("job.started")   # job_id=job_1 queue=emails
    log.info("job.finished")  # job_id=job_1 queue=emails
# context automatically restored
```

Context is `contextvars`-based, so it works correctly with `asyncio` and nested scopes:

```python
with logging_context(outer="1"):
    with logging_context(inner="2"):
        log.info("both")  # outer=1 inner=2
    log.info("outer only")  # outer=1
```

Lower-level helpers are available for integrations:

```python
from ultilog import bind_context, clear_context, get_context

bind_context(request_id="req_123")
get_context()  # {"request_id": "req_123"}
clear_context()
```

## Framework Integrations

### FastAPI / Starlette

```python
from fastapi import FastAPI
from ultilog.integrations import install_fastapi_logging

app = FastAPI()
install_fastapi_logging(app)
# Every request gets logging context with request_id, http.method, http.path
```

### ASGI Middleware

```python
from ultilog.integrations import UltilogASGIMiddleware

app = UltilogASGIMiddleware(app)
```

### Celery

```python
from ultilog.integrations import install_celery_logging

install_celery_logging(app)
# Tasks get context with celery_task_id and celery_task_name
```

### httpx

```python
from ultilog.integrations import install_httpx_logging

client = httpx.Client()
install_httpx_logging(client)
# Logs outgoing HTTP requests at DEBUG level
```

### SQLAlchemy

```python
from ultilog.integrations import install_sqlalchemy_logging

install_sqlalchemy_logging(engine, level=logging.DEBUG)
```

## Structlog

When `structlog` is installed, ultilog can configure it with pre-built processor chains:

```python
from ultilog.structlog import configure_structlog

configure_structlog()  # console renderer for dev
```

Choose a renderer that matches your mode:

```python
from ultilog.models.structlog import StructlogSettings

configure_structlog(StructlogSettings(renderer="json"))
```

## OpenTelemetry

With the `otel` extra installed, configure traces, logs, and metrics:

```python
from ultilog.otel.traces import configure_otel_traces
from ultilog.otel.logs import configure_otel_logs
from ultilog.otel.metrics import configure_otel_metrics

configure_otel_traces(service_name="my-api")
configure_otel_logs(service_name="my-api")
configure_otel_metrics(service_name="my-api")
```

Or configure all signals at once:

```python
from ultilog.otel.exporters import configure_exporters
from ultilog.models.otel import OTelSettings

configure_exporters(OTelSettings(
    enabled=True,
    service_name="my-api",
    traces_enabled=True,
    logs_enabled=True,
))
```

Trace/log correlation is automatic when a span is active:

```python
from ultilog.otel.correlation import TraceCorrelationFilter

handler.addFilter(TraceCorrelationFilter())
# Log records get trace_id and span_id attributes
```

## Environment Variables

Settings use the `ULTILOG_` prefix with `__` for nesting:

```bash
export ULTILOG_PRESET=prod
export ULTILOG_LOGGING__LEVEL=DEBUG
export ULTILOG_LOGGING__MODE=json
export ULTILOG_RICH__SHOW_PATH=false
```

## CLI

```bash
ultilog doctor --json          # runtime diagnostics
ultilog bootstrap              # inspect a project and print grouped install hints
ultilog bootstrap --json       # machine-readable bootstrap plan
ultilog bootstrap --commands   # grouped setup plus OTel zero-code commands
ultilog bootstrap --snippet --service-name my-api
ultilog show-config            # dump effective settings
ultilog validate               # check configuration
ultilog demo --mode plain      # emit a demo log line
ultilog demo --mode json
```

Or via module:

```bash
python -m ultilog doctor --json
```

## Project Bootstrap

`ultilog bootstrap` inspects a project and prints a non-destructive plan for the
packages that make logging and observability work end to end. It reads
`pyproject.toml`, lightly scans imports, detects the package manager, and groups
recommendations by where they belong:

| Target | pyproject location | Examples |
|--------|--------------------|----------|
| `observability-core` | `[project.optional-dependencies]` | OTel API/SDK/exporter, logging, ASGI/FastAPI/httpx/SQLAlchemy/Redis instrumentation |
| `observability-extra` | `[project.optional-dependencies]` | Celery, botocore, grpc, urllib3, aiohttp, asyncpg instrumentation |
| `formatting` | `[dependency-groups]` | `ruff` |
| `typing` | `[dependency-groups]` | `mypy`, `pyright`, `types-*` packages |
| `test-core` | `[dependency-groups]` | `pytest`, `pytest-cov`, `pytest-mock` |
| `coverage` | `[dependency-groups]` | `coverage` |

For PDM projects, the suggested commands use the right target directly:

```bash
pdm add --no-sync -G observability-core opentelemetry-exporter-otlp ...
pdm add --no-sync -d -G typing mypy pyright types-requests
pdm add --no-sync -d -G test-core pytest pytest-cov pytest-mock
```

When OpenTelemetry zero-code tooling is installed, the plan also shows the
official bootstrap commands:

```bash
pdm run opentelemetry-bootstrap -a requirements
pdm run opentelemetry-instrument python -m your_app
# Optional after reviewing requirements:
pdm run opentelemetry-bootstrap -a install
```

`ultilog bootstrap` runs a read-only environment check for human output and
`--apply`. If `pip check` reports a conflict, the CLI prints the conflicting
requirement and a repair command before touching packages.

To intentionally run package-manager setup from the CLI, use `--apply` with
one or more groups:

```bash
ultilog bootstrap --apply --group observability-core
ultilog bootstrap --apply --group typing --group test-core
ultilog bootstrap --apply --all
```

For PDM, `--apply` uses `pdm add --no-sync` so it updates `pyproject.toml` and
the lockfile without pruning the active virtualenv. Run `pdm sync` with the
groups you actually want only after reviewing the result.

For application startup, generate a small setup snippet:

```bash
ultilog bootstrap --snippet --service-name my-api
```

The snippet calls `setup_auto(service_name="my-api")`, which uses Rich logging
in development, quiet plain logging for tests, and production JSON logging with
OTel trace/log correlation when `APP_ENV=prod` or `ULTILOG_ENV=prod`.

Recommended repo shape:

```python
# src/my_api/logging.py
from ultilog import get_logger, setup_auto

setup_auto(service_name="my-api")
log = get_logger(__name__)
```

Import that module once from your app entrypoint before creating other loggers.

## Testing

ultilog provides test utilities so downstream projects can isolate logging state:

```python
from ultilog.testing.reset import reset_ultilog
from ultilog.testing.capture import capture_logs

reset_ultilog()  # reset package state

with capture_logs("my.logger") as records:
    get_logger("my.logger").info("captured")
assert records[0].getMessage() == "captured"
```

## Advanced Configuration

For full control, use `configure()` with an explicit settings object:

```python
from ultilog import configure, UltilogSettings

settings = UltilogSettings(
    preset="prod",
    logging=LoggingSettings(level="DEBUG", mode="json"),
    context=ContextSettings(enabled=True),
)
configure(settings, force=True)
```

## Development

```bash
pdm sync -G dev -G docs
pdm run pytest                 # tests
pdm run ruff check .           # lint
pdm run mypy src/ultilog       # type-check
pdm run mkdocs serve           # docs preview
```

## License

MIT
