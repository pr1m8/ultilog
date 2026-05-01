# Context

## Design principle

Context belongs at **runtime boundaries**, not at logger creation time. Instead of creating loggers with bound fields, you bind context at request, job, or task boundaries and it flows into every log record within that scope.

## Context manager

```python
from ultilog import get_logger, logging_context

log = get_logger("worker")

with logging_context(job_id="job_1", queue="emails"):
    log.info("job.started")   # includes job_id and queue
    log.info("job.finished")  # same context
# context automatically restored
```

## Nesting

Context scopes nest correctly. Inner scopes merge with outer values, and restoration is token-based:

```python
with logging_context(outer="1"):
    with logging_context(inner="2"):
        get_context()  # {"outer": "1", "inner": "2"}
    get_context()      # {"outer": "1"}
```

## Async safety

Context uses Python's `contextvars.ContextVar`, which is natively safe with `asyncio`. Concurrent tasks get isolated context:

```python
async def handle_request(request_id: str):
    with logging_context(request_id=request_id):
        await do_work()  # context stays with this task
```

## Low-level API

For integrations that need direct control:

```python
from ultilog import bind_context, clear_context, get_context

token = bind_context(request_id="req_123")
get_context()     # {"request_id": "req_123"}
clear_context()   # {}
```

## Decorator

Wrap functions with automatic context:

```python
from ultilog.context.decorators import with_logging_context

@with_logging_context(component="worker")
def process_job():
    log.info("processing")  # component=worker
```

## How context reaches log records

The `ContextFilter` (installed automatically by bootstrap) reads the current context and injects it into each `LogRecord` as:

- `ultilog_context` -- dictionary of context values
- `ultilog_context_text` -- compact text suffix like ` request_id=r1`
- Individual record attributes for safe keys
