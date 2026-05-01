# Rich Integration

ultilog uses [Rich](https://github.com/Textualize/rich) as its default console handler for the `dev` preset.

## Default behavior

When `mode="rich"` (the default in the `dev` preset), ultilog installs a `RichHandler` that provides:

- Colored log levels
- Syntax-highlighted tracebacks
- Source file path and line numbers
- Timestamp formatting

```python
from ultilog import get_logger

log = get_logger()
log.info("pretty output")
log.error("with traceback", exc_info=True)
```

## Configuration

Rich settings are controlled through `RichSettings`:

```python
from ultilog import setup

setup(
    show_path=False,          # hide file paths
    rich_tracebacks=True,     # enable Rich tracebacks
    markup=False,             # disable Rich markup in messages
    force=True,
)
```

### Available settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `True` | Whether to use RichHandler |
| `show_time` | `True` | Show timestamps |
| `show_level` | `True` | Show log level |
| `show_path` | `True` | Show file path and line number |
| `markup` | `False` | Enable Rich markup in log messages |
| `rich_tracebacks` | `True` | Use Rich for traceback formatting |
| `tracebacks_show_locals` | `False` | Show local variables in tracebacks |
| `log_time_format` | `"[%X]"` | Timestamp format string |

## Manual handler creation

For custom handler composition:

```python
from ultilog.handlers.rich import create_rich_handler
from ultilog.models.rich import RichSettings

handler = create_rich_handler(
    settings=RichSettings(show_path=False, rich_tracebacks=True)
)
```

## Disabling Rich

Set `mode="plain"` or `mode="json"` to bypass the Rich handler entirely:

```python
setup(mode="plain", force=True)
```

The `test` and `prod` presets disable Rich automatically.

## Custom theme

ultilog defines a small Rich theme for diagnostics output:

```python
from ultilog.rich.themes import create_ultilog_theme
from ultilog.rich.console import create_console

console = create_console()  # uses stderr, soft_wrap
```
