# Quickstart

```python
from ultilog import get_logger

log = get_logger()
log.info("app.started")
```

Run a local example:

```bash
PYTHONPATH=src python examples/01_zero_config.py
```

Run the test suite:

```bash
PYTHONPATH=src pytest
```
