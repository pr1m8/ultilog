# ultilog

`ultilog` is an ergonomic Python logging package that starts with a tiny API and
scales toward structured observability.

The default experience is intentionally small:

```python
from ultilog import get_logger

log = get_logger()
log.info("app.started")
```

No explicit settings object is required for ordinary use. The package lazily
configures logging on first access, installs a useful console handler, and then
returns a standard-library logger.

## Install

```bash
pdm add ultilog
```

Other package managers:

```bash
pip install ultilog
uv add ultilog
poetry add ultilog
```

Future extras are designed to look like:

```bash
pip install "ultilog[structlog]"
pip install "ultilog[otel]"
pip install "ultilog[full]"
```

## Quickstart

```python
from ultilog import get_logger

log = get_logger()
log.info("hello")
```

Explicit naming is supported:

```python
log = get_logger(__name__)
```

Custom names are supported:

```python
log = get_logger("my.service")
```

Optional setup is available when needed:

```python
from ultilog import setup, get_logger

setup(level="DEBUG", force=True)
log = get_logger()
```

## Modes

The scaffold supports three modes:

- `rich`: pretty local console logs
- `plain`: simple stream logging
- `json`: machine-readable JSON logs

```python
from ultilog import setup, get_logger

setup(mode="json", force=True)
get_logger("api").info("request.finished")
```

## Context

Context belongs at runtime boundaries, not logger creation time.

```python
from ultilog import get_logger, logging_context

log = get_logger("worker")

with logging_context(job_id="job_1", queue="emails"):
    log.info("job.started")
```

## Current Scaffold Includes

- zero-config `get_logger()`
- optional `setup(...)`
- explicit `configure(settings)` for advanced use
- Rich console handler factory
- plain and JSON output modes
- contextvars-based context helpers
- ASGI/FastAPI integration shapes
- optional dependency helpers
- diagnostics CLI
- unit, integration, and e2e test layout
- docs, examples, CI skeleton, and future integration namespaces

## CLI

```bash
python -m ultilog doctor --json
python -m ultilog demo --mode plain
python -m ultilog demo --mode json
```

## Development

```bash
pdm sync -G dev
pdm run pytest
pdm run ruff check .
pdm run mypy src/ultilog
```

For local source-tree experiments without installing the package:

```bash
PYTHONPATH=src python examples/01_zero_config.py
PYTHONPATH=src python -m ultilog doctor --json
```

## Design Direction

`ultilog` should remain easy at the surface and layered underneath. The default
API should stay tiny while internals grow to support structured logging,
OpenTelemetry, context propagation, exporters, and framework integrations.

See `docs/` for architecture, testing strategy, roadmap, and cookbook notes.
