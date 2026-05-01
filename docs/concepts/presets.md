# Presets

Presets apply opinionated defaults for common environments so you don't have to configure every setting manually.

## Available presets

| Preset | Mode | Level | Rich | Context in text | Use case |
|--------|------|-------|------|-----------------|----------|
| `dev` | `rich` | INFO | Enabled | Yes | Local development |
| `test` | `plain` | WARNING | Disabled | No | Test suites |
| `prod` | `json` | INFO | Disabled | N/A (in JSON) | Production / containers |

## Usage

```python
from ultilog import setup

setup(preset="prod", force=True)
```

Or via environment variable:

```bash
export ULTILOG_PRESET=prod
```

## What presets change

Presets are applied as a model validator on `UltilogSettings`. They override defaults but not explicit user values. For example, `preset="test"` only lowers the level to WARNING if it was still at the default INFO.

## Custom configuration

Presets are a starting point. You can override individual settings after selecting a preset:

```python
setup(preset="prod", level="DEBUG", force=True)
# JSON mode from prod preset, but with DEBUG level
```
