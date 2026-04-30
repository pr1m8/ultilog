# ultilog examples

Run examples from the repository root with:

```bash
PYTHONPATH=src python examples/01_zero_config.py
```

Current examples:

1. `01_zero_config.py` - import `get_logger()` and log immediately.
2. `02_explicit_names.py` - compare inferred, module, and custom logger names.
3. `03_setup_overrides.py` - use optional `setup(...)` before logger creation.
4. `04_json_mode.py` - emit structured JSON logs.
5. `05_context_scope.py` - bind request/job context for a scoped block.
6. `06_diagnostics.py` - inspect runtime diagnostics.
7. `07_fastapi_shape.py` - show the FastAPI integration call shape without requiring FastAPI.
