# Public API Reference

## `get_logger(name=None, **bind_values)`

Returns a configured standard-library logger. If `name` is omitted, `ultilog`
attempts to infer the caller's module name.

```python
from ultilog import get_logger

log = get_logger()
log.info("hello")
```

## `setup(...)`

Optional lightweight setup.

```python
from ultilog import setup

setup(preset="dev", level="DEBUG", force=True)
```

## `configure(settings, force=False)`

Advanced settings-based configuration.

```python
from ultilog import configure, UltilogSettings

configure(UltilogSettings(preset="prod"), force=True)
```

## `logging_context(**values)`

Temporarily binds context values.

```python
from ultilog import logging_context, get_logger

log = get_logger()
with logging_context(request_id="abc"):
    log.info("inside.request")
```

## `bind_context`, `clear_context`, `get_context`

Lower-level context helpers for integrations and advanced users.
