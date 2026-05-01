# structlog Integration

ultilog provides optional [structlog](https://www.structlog.org/) integration when the `structlog` extra is installed.

## Install

```bash
pip install "ultilog[structlog]"
```

## Configuration

```python
from ultilog.structlog import configure_structlog

configure_structlog()
```

This sets up a structlog processor chain that:

- Merges `contextvars` context
- Adds logger name and log level
- Formats positional arguments
- Renders stack info
- Adds ISO timestamps
- Routes through stdlib logging (structlog wraps stdlib, not replaces it)

## Renderers

Choose a renderer based on your environment:

```python
from ultilog.models.structlog import StructlogSettings

# Console (default) -- colored dev output
configure_structlog(StructlogSettings(renderer="console"))

# JSON -- machine-readable production output
configure_structlog(StructlogSettings(renderer="json"))

# Key-value -- compact structured text
configure_structlog(StructlogSettings(renderer="key_value"))
```

## Processor chains

Pre-built processor chains are available:

```python
from ultilog.structlog.processors import (
    get_default_processors,
    get_json_processors,
    get_console_processors,
)

# Base chain (no renderer)
processors = get_default_processors()

# With JSON renderer appended
processors = get_json_processors()

# With console renderer appended
processors = get_console_processors()
```

## Renderer helpers

Map ultilog modes to structlog renderer names:

```python
from ultilog.structlog.renderers import get_renderer_name, get_renderer

get_renderer_name(mode="json")    # "json"
get_renderer_name(mode="plain")   # "key_value"
get_renderer_name(mode="rich")    # "console"

renderer = get_renderer("json")   # structlog.processors.JSONRenderer()
```

## Bridge availability

Check whether structlog is installed:

```python
from ultilog.structlog.bridge import bridge_enabled

if bridge_enabled():
    configure_structlog()
```

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `False` | Activate structlog integration |
| `renderer` | `"console"` | Renderer: `console`, `json`, or `key_value` |
| `cache_logger_on_first_use` | `True` | Cache bound loggers for performance |
