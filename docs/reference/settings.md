# Settings Reference

## Presets

| Preset | Mode | Level | Rich | Context text | Use case |
|--------|------|-------|------|-------------|----------|
| `dev` | `rich` | INFO | Enabled | Yes | Local development |
| `test` | `plain` | WARNING | Disabled | No | Test suites |
| `prod` | `json` | INFO | Disabled | N/A | Production |

```python
from ultilog import setup

setup(preset="prod", force=True)
```

## Environment variables

All settings use the `ULTILOG_` prefix. Nested keys use double underscores:

```bash
export ULTILOG_PRESET=prod
export ULTILOG_LOGGING__LEVEL=DEBUG
export ULTILOG_LOGGING__MODE=json
export ULTILOG_RICH__SHOW_PATH=false
export ULTILOG_CONTEXT__ENABLED=true
export ULTILOG_STRUCTLOG__ENABLED=true
export ULTILOG_OTEL__ENABLED=true
export ULTILOG_OTEL__SERVICE_NAME=my-api
```

## Settings models

### LoggingSettings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `level` | `str \| int` | `"INFO"` | Logging threshold |
| `mode` | `"rich" \| "plain" \| "json"` | `"rich"` | Output mode |
| `force` | `bool` | `False` | Replace existing root handlers |
| `format` | `str` | `"%(message)s"` | Format string |
| `stream` | `"stdout" \| "stderr"` | `"stdout"` | Output stream |
| `include_context` | `bool` | `True` | Append context to text logs |

### RichSettings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `True` | Use RichHandler |
| `show_time` | `bool` | `True` | Show timestamps |
| `show_level` | `bool` | `True` | Show log level |
| `show_path` | `bool` | `True` | Show file path |
| `markup` | `bool` | `False` | Enable Rich markup |
| `rich_tracebacks` | `bool` | `True` | Rich tracebacks |
| `tracebacks_show_locals` | `bool` | `False` | Show locals in tracebacks |

### ContextSettings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable context system |
| `include_in_records` | `bool` | `True` | Inject context into log records |
| `include_in_text` | `bool` | `True` | Append context text to messages |

### StructlogSettings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `False` | Activate structlog |
| `renderer` | `str` | `"console"` | `console`, `json`, or `key_value` |
| `cache_logger_on_first_use` | `bool` | `True` | Cache bound loggers |

### OTelSettings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `False` | Activate OpenTelemetry |
| `service_name` | `str` | `"ultilog-app"` | Service name |
| `endpoint` | `str \| None` | `None` | OTLP endpoint |
| `traces_enabled` | `bool` | `False` | Enable traces |
| `metrics_enabled` | `bool` | `False` | Enable metrics |
| `logs_enabled` | `bool` | `False` | Enable log export |
| `inject_trace_ids` | `bool` | `True` | Add trace/span IDs |

## Validation

Settings validate automatically:

- `mode="rich"` with `rich.enabled=False` auto-corrects to `mode="plain"` with a warning
- `structlog.enabled=True` requires the `structlog` package to be installed
- `otel.enabled=True` requires the `opentelemetry` package to be installed
- Log levels accept names (`"DEBUG"`) or integers (`10`)

## Advanced usage

```python
from ultilog import configure, UltilogSettings
from ultilog.models.logging import LoggingSettings

settings = UltilogSettings(
    preset="prod",
    logging=LoggingSettings(level="DEBUG", mode="json"),
)
configure(settings, force=True)
```

## Export and debug

```python
from ultilog.config.export import export_settings, summarize_settings
from ultilog.settings import UltilogSettings

settings = UltilogSettings()
export_settings(settings)      # full dict
summarize_settings(settings)   # compact summary
```
