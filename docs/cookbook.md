# Cookbook

## Start With Zero Config

```python
from ultilog import get_logger

log = get_logger()
log.info("app.started")
```

## Use Explicit Setup

```python
from ultilog import setup, get_logger

setup(level="DEBUG", force=True)
log = get_logger(__name__)
```

## Emit JSON Logs

```python
from ultilog import setup, get_logger

setup(mode="json", force=True)
get_logger("api").info("request.finished")
```

## Bind Context

```python
from ultilog import get_logger, logging_context

log = get_logger("worker")
with logging_context(job_id="job_1"):
    log.info("job.started")
```

## Build a Manual Handler

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
