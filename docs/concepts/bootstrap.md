# Bootstrap

## How it works

ultilog uses lazy bootstrap: logging is configured automatically on the first `get_logger()` call. No explicit setup is required.

```python
from ultilog import get_logger

log = get_logger()  # triggers bootstrap here
log.info("ready")
```

## Configuration order

1. **Default** -- `get_logger()` triggers `ensure_configured()`, which builds `UltilogSettings` from defaults and environment variables, then calls `configure_basic_logging()`.
2. **Explicit** -- `setup(...)` pre-configures before first logger use. If logging is already configured, `setup()` is a no-op unless `force=True`.
3. **Advanced** -- `configure(settings)` accepts a full `UltilogSettings` object for programmatic control.

## Thread safety

Bootstrap is protected by a re-entrant lock (`threading.RLock`). Multiple threads calling `get_logger()` concurrently will not install duplicate handlers.

## Idempotency

Configuration runs at most once. Subsequent `get_logger()` calls skip bootstrap. To reconfigure, pass `force=True`:

```python
from ultilog import setup

setup(mode="json", force=True)  # replaces existing configuration
```

## Reset

For tests and notebooks, `reset_logging()` clears runtime state so bootstrap can run again:

```python
from ultilog import reset_logging

reset_logging()
```
