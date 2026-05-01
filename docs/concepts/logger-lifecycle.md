# Logger Lifecycle

## Creation

`get_logger()` returns a standard-library `logging.Logger` (or `LoggerAdapter` if bind values are provided). It does not create a custom logger class.

```python
from ultilog import get_logger

log = get_logger("my.service")
type(log)  # <class 'logging.Logger'>
```

## Name inference

When no name is provided, ultilog walks the call stack and infers the caller's module name:

```python
# In my_app/worker.py:
log = get_logger()  # logger name: "my_app.worker"
```

The inference skips frames from the `ultilog` package itself and returns the first external module name.

## Bind values

Static context can be attached at creation time using keyword arguments. This returns a `LoggerAdapter`:

```python
log = get_logger("api", service="auth")
log.info("request")  # extra includes service="auth"
```

This is separate from `logging_context`, which binds execution-scoped context.

## Lazy bootstrap

The first `get_logger()` call triggers configuration if it hasn't happened yet. All subsequent calls return loggers without re-running bootstrap.

## Relationship to stdlib

ultilog loggers **are** stdlib loggers. They participate in the standard logger hierarchy, respect the root handler configuration, and work with any stdlib-compatible tooling.
