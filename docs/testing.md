# Testing Strategy

## Test layers

ultilog uses three test layers:

### Unit tests (`tests/unit/`)

Cover isolated behavior of individual components:

- Settings models and validation
- Handler and formatter factories
- Context binding, decorators, and request helpers
- State management and reset
- Caller name inference
- CLI argument parsing
- Diagnostics output
- Optional import helpers
- structlog renderers and bridge
- OTel correlation filter

### Integration tests (`tests/integration/`)

Cover module composition and end-to-end flows:

- `setup()` then `get_logger()` flow
- Bootstrap reconfiguration with `force=True`
- JSON and plain modes with context output
- ASGI middleware context binding
- FastAPI middleware installation
- Async context isolation between concurrent tasks

### E2E tests (`tests/e2e/`)

Run examples and CLI in subprocesses:

- CLI `doctor --json` via subprocess
- Example script execution and output validation
- Demo app execution

## Test isolation

The `conftest.py` provides an autouse fixture `clean_logging_state` that:

1. Saves root logger handlers and level
2. Resets ultilog runtime state
3. Clears `ULTILOG_*` environment variables
4. Yields to the test
5. Restores logging state
6. Resets ultilog again

This ensures no test leaks state to another.

## Test utilities for downstream users

ultilog exposes testing helpers so applications can isolate logging in their own tests:

```python
from ultilog.testing.reset import reset_ultilog
from ultilog.testing.capture import capture_logs

# Reset package state
reset_ultilog()

# Capture log records
with capture_logs("my.logger") as records:
    get_logger("my.logger").info("test message")
assert records[0].getMessage() == "test message"
```

### Test factories

```python
from ultilog.testing.factories import make_test_settings, make_log_record

settings = make_test_settings(level="DEBUG")
record = make_log_record(msg="test")
```

## Running tests

```bash
pdm run pytest                      # full suite
pdm run pytest tests/unit           # unit only
pdm run pytest tests/integration    # integration only
pdm run pytest tests/e2e            # e2e only
pdm run pytest -k test_name         # single test
pdm run pytest --cov=ultilog        # with coverage
```
