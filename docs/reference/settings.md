# Settings Reference

`ultilog` settings are internal-first but available for advanced users.

## Presets

- `dev`: Rich console logging, info-level output, context text enabled.
- `prod`: JSON logging, Rich disabled, path display disabled.
- `test`: plain warning-level output, Rich disabled.

## Environment Variables

Settings use the `ULTILOG_` prefix and nested keys use double underscores.

Examples:

```bash
export ULTILOG_PRESET=prod
export ULTILOG_LOGGING__LEVEL=DEBUG
export ULTILOG_LOGGING__MODE=json
export ULTILOG_RICH__SHOW_PATH=false
```

## Advanced Usage

```python
from ultilog import configure, UltilogSettings

settings = UltilogSettings(preset="prod")
configure(settings, force=True)
```
