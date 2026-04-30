# Architecture

`ultilog` is intentionally split into a small public API and a larger internal
composition layer.

## Public Surface

The primary user-facing API is:

```python
from ultilog import get_logger, setup
```

The goal is to make logging feel available immediately while still allowing
advanced configuration later.

## Runtime Flow

1. User calls `get_logger()`.
2. `ensure_configured()` checks runtime state.
3. If needed, default settings are loaded.
4. The root logging handler is installed.
5. A standard-library logger is returned.

This means most applications can start without explicit setup, while applications
that need control can call `setup(...)` before logger creation.

## Module Responsibilities

### `api.py`

Owns the public API and should remain thin.

### `bootstrap.py`

Owns idempotent configuration and setup orchestration.

### `state.py`

Owns runtime state and reset behavior.

### `settings.py` and `models/`

Own typed configuration.

### `handlers/`

Creates handler instances and does not attach them globally.

### `context/`

Owns runtime context. Context is intentionally separate from logger creation.

### `integrations/`

Owns optional framework integration points.

### `otel/`

Owns optional OpenTelemetry integration paths.

## Why This Shape Works

The package can grow from simple Rich-backed console logging into a structured
observability toolkit without changing the basic import path.
