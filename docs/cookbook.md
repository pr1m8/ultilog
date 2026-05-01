# Cookbook

## Zero config

```python
from ultilog import get_logger

log = get_logger()
log.info("app.started")
```

## Explicit setup with level and mode

```python
from ultilog import setup, get_logger

setup(level="DEBUG", mode="plain", force=True)
log = get_logger(__name__)
log.debug("verbose output")
```

## JSON logging for production

```python
from ultilog import setup, get_logger

setup(mode="json", force=True)
get_logger("api").info("request.finished")
```

## Bind context at request boundaries

```python
from ultilog import get_logger, logging_context

log = get_logger("worker")

with logging_context(job_id="job_1"):
    log.info("job.started")
    log.info("job.finished")
```

## Nested context scopes

```python
with logging_context(service="api"):
    with logging_context(request_id="req_1"):
        log.info("handling")  # service=api request_id=req_1
    log.info("done")          # service=api
```

## Context decorator

```python
from ultilog.context.decorators import with_logging_context

@with_logging_context(component="worker")
def process_job():
    get_logger().info("processing")
```

## Environment variable overrides

```bash
ULTILOG_PRESET=prod ULTILOG_LOGGING__LEVEL=DEBUG python app.py
```

## Manual handler composition

```python
import logging
from ultilog.handlers.stream import create_stream_handler
from ultilog.formatters.key_value import KeyValueFormatter

handler = create_stream_handler()
handler.setFormatter(KeyValueFormatter())
logger = logging.getLogger("manual")
logger.addHandler(handler)
logger.warning("manual.warning")
```

## File handler

```python
from ultilog.handlers.file import create_file_handler

handler = create_file_handler("app.log", level=logging.INFO)
logging.getLogger().addHandler(handler)
```

## FastAPI integration

```python
from fastapi import FastAPI
from ultilog.integrations import install_fastapi_logging

app = FastAPI()
install_fastapi_logging(app)
```

## Celery integration

```python
from ultilog.integrations import install_celery_logging

app = Celery("tasks")
install_celery_logging(app)
```

## Advanced settings object

```python
from ultilog import configure, UltilogSettings
from ultilog.models.logging import LoggingSettings

settings = UltilogSettings(
    preset="prod",
    logging=LoggingSettings(level="DEBUG", mode="json"),
)
configure(settings, force=True)
```

## Diagnostics

```python
from ultilog.diagnostics import get_diagnostics

info = get_diagnostics()
print(info["active_preset"])
print(info["handlers"])
print(info["optional_dependencies"])
```

## Test isolation

```python
from ultilog.testing.reset import reset_ultilog
from ultilog.testing.capture import capture_logs

reset_ultilog()

with capture_logs("my.logger") as records:
    get_logger("my.logger").info("test message")
assert len(records) == 1
```
