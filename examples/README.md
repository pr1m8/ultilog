# ultilog examples

Run examples from the repository root with:

```bash
PYTHONPATH=src python examples/01_zero_config.py
```

Or after installing the package:

```bash
pip install ultilog
python examples/01_zero_config.py
```

## Examples

| # | File | What it shows |
|---|------|---------------|
| 01 | `01_zero_config.py` | Just `from ultilog import get_logger` and log |
| 02 | `02_setup_dev.py` | `setup_dev()` — super-pretty Rich with locals in tracebacks |
| 03 | `03_setup_prod.py` | `setup_prod()` — JSON output with optional OTel correlation |
| 04 | `04_explicit_names.py` | Inferred, module, and custom logger names |
| 05 | `05_context_scope.py` | `logging_context()` for request/job context binding |
| 06 | `06_json_mode.py` | Direct JSON mode setup with extra fields |
| 07 | `07_diagnostics.py` | Inspect runtime diagnostics |
| 08 | `08_otel_correlation.py` | Auto-attached OTel `trace_id` / `span_id` on records |
| 09 | `09_manual_handlers.py` | Manual handler composition with factories |
| 10 | `10_asgi_shape.py` | ASGI middleware demo without FastAPI |
| 11 | `11_fastapi_shape.py` | FastAPI integration shape |
| 12 | `12_demo_app.py` | Full demo app with services and context propagation |

## Tip

For real apps, just use:

```python
from ultilog import setup_dev, get_logger

setup_dev()  # super-pretty Rich console for local development
log = get_logger(__name__)
log.info("ready")
```

Or for production:

```python
from ultilog import setup_prod, get_logger

setup_prod(service_name="my-api")
log = get_logger(__name__)
log.info("request.handled")  # JSON output, OTel-correlated when available
```
