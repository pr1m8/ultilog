# Public API Reference

## `get_logger(name=None, **bind_values)`

Return a configured standard-library logger. If `name` is omitted, the caller's module name is inferred from the call stack.

```python
from ultilog import get_logger

log = get_logger()              # infers caller module
log = get_logger(__name__)      # explicit module name
log = get_logger("my.service")  # custom name
```

With bind values, returns a `LoggerAdapter`:

```python
log = get_logger("api", service="auth")
log.info("request")  # extra includes service="auth"
```

**Raises:** `UltilogConfigurationError` if lazy bootstrap fails.

## `setup(*, preset=None, force=False, **overrides)`

Optional lightweight setup. Call before first `get_logger()` to control configuration. After bootstrap, `setup()` is a no-op unless `force=True`.

```python
from ultilog import setup

setup(preset="prod", force=True)
setup(level="DEBUG", mode="json", force=True)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `preset` | `str \| None` | Preset name: `dev`, `test`, `prod` |
| `force` | `bool` | Reconfigure even if already configured |
| `**overrides` | | Flat settings: `level`, `mode`, `show_path`, etc. |

## `configure(settings, *, force=False)`

Advanced configuration using an explicit `UltilogSettings` object.

```python
from ultilog import configure, UltilogSettings

configure(UltilogSettings(preset="prod"), force=True)
```

## `logging_context(**values)`

Context manager that temporarily binds context values to all log records within the scope.

```python
from ultilog import logging_context, get_logger

log = get_logger()
with logging_context(request_id="abc"):
    log.info("inside")  # request_id=abc
```

## `bind_context(**values)`

Merge values into the current context. Returns a token for manual reset.

```python
from ultilog import bind_context

token = bind_context(request_id="abc")
```

## `get_context()`

Return a read-only mapping of current context values.

```python
from ultilog import get_context

ctx = get_context()  # MappingProxyType({"request_id": "abc"})
```

## `clear_context()`

Clear all context values.

```python
from ultilog import clear_context

clear_context()
```

## `reset_logging()`

Reset package and root logging state. Intended for tests, notebooks, and local experiments.

```python
from ultilog import reset_logging

reset_logging()
```

## `UltilogSettings`

Root settings class (re-exported for convenience). See [Settings Reference](settings.md).
