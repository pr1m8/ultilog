# Quickstart

## Install

```bash
pip install ultilog
```

## Zero config

```python
from ultilog import get_logger

log = get_logger()
log.info("app.started")
```

This lazily configures logging with the `dev` preset (Rich console, INFO level) and returns a standard-library logger.

## Automatic setup

```python
from ultilog import setup_auto, get_logger

setup_auto(service_name="my-api")
log = get_logger(__name__)
log.info("app.started")
```

`setup_auto()` uses Rich output locally, quiet plain output for tests, and JSON
production output when `APP_ENV=prod` or `ULTILOG_ENV=prod`.

## Explicit setup

```python
from ultilog import setup, get_logger

setup(level="DEBUG", mode="plain", force=True)
log = get_logger(__name__)
log.debug("debugging")
```

## JSON logging

```python
from ultilog import setup, get_logger

setup(mode="json", force=True)
get_logger("api").info("request.finished")
```

## Context binding

```python
from ultilog import get_logger, logging_context

log = get_logger("worker")

with logging_context(job_id="job_1", queue="emails"):
    log.info("job.started")
```

## Presets

```python
setup(preset="prod", force=True)   # JSON mode, Rich disabled
setup(preset="test", force=True)   # plain mode, WARNING level
```

## CLI diagnostics

```bash
python -m ultilog doctor --json
python -m ultilog bootstrap
python -m ultilog bootstrap --commands
python -m ultilog bootstrap --snippet --service-name my-api
python -m ultilog show-config
python -m ultilog demo --mode json
```

`bootstrap` prints grouped install hints for OpenTelemetry instrumentation,
typing stubs, pytest, coverage, and formatting tools. It is non-destructive by
default.

## Run examples

```bash
PYTHONPATH=src python examples/01_zero_config.py
PYTHONPATH=src python examples/04_json_mode.py
PYTHONPATH=src python examples/05_context_scope.py
```

## Run tests

```bash
pdm sync -G dev
pdm run pytest
```
