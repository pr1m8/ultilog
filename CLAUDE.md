# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository

**Package:** `ultilog` (one `t` after `u`) — ergonomic Python logging with Rich-first defaults.
**Canonical remote:** `pr1m8/ultilog` on GitHub. An older `utillog` remote may exist; ignore it.
**Python:** 3.13+ only. **Package manager:** PDM.

## Commands

```bash
# Setup
pdm sync -G dev -G docs

# Test / Lint / Type-check
pdm run pytest                    # full test suite
pdm run pytest tests/unit         # unit tests only
pdm run pytest tests/integration  # integration tests only
pdm run pytest tests/e2e          # end-to-end tests only
pdm run pytest -k test_name       # single test by name
pdm run ruff check .              # lint
pdm run ruff format .             # auto-format
pdm run mypy src/ultilog          # type-check (strict mode)

# Docs
pdm run mkdocs build
pdm run mkdocs serve              # local preview

# CLI
pdm run python -m ultilog doctor --json
pdm run python -m ultilog demo --mode plain
pdm run python -m ultilog demo --mode json

# Examples (without installing the package)
PYTHONPATH=src python examples/01_zero_config.py

# Nox (CI-style multi-session runner)
nox                               # runs: tests, lint, typecheck
nox -s tests                      # single session
```

Always use `pdm run ...` so commands resolve from the project virtualenv.

## Architecture

### Public API (src/ultilog/\_\_init\_\_.py)

The entire public surface re-exports from `api.py`:
`get_logger()`, `setup()`, `configure()`, `logging_context()`, `bind_context()`, `clear_context()`, `get_context()`, `reset_logging()`, `UltilogSettings`.

### Runtime flow

1. `get_logger()` calls `ensure_configured()` in `bootstrap.py`
2. `bootstrap.py` checks `state.runtime_state.configured` (thread-safe via RLock)
3. If not configured, builds `UltilogSettings` (pydantic-settings, env prefix `ULTILOG_` with `__` nesting) and calls `configure_basic_logging()`
4. Handler/formatter selected by **preset** (`dev`/`test`/`prod`) which maps to a **mode** (`rich`/`plain`/`json`)
5. Returns a standard-library `logging.Logger`

### Key design patterns

- **Lazy bootstrap** — configuration happens on first `get_logger()` call, not at import time
- **Idempotent** — reconfiguration requires `force=True`
- **Execution-scoped context** — `contextvars.ContextVar`, not logger-creation-time binding. `ContextFilter` injects context into `LogRecord` attributes
- **Presets drive defaults** — `dev` (Rich console), `test` (plain/WARNING), `prod` (JSON)
- **Optional deps degrade gracefully** — extras: `structlog`, `otel`, `web`, `full`

### Source layout

- `src/ultilog/` — package root (72 files)
  - `api.py` + `bootstrap.py` + `state.py` + `settings.py` — core runtime
  - `config/` — stdlib logging configuration, presets, normalization
  - `models/` — pydantic settings models (logging, rich, context, structlog, otel)
  - `handlers/` — handler factories (rich, stream, file, queue)
  - `formatters/` — JSON, key-value, text formatters
  - `context/` — contextvars storage, managers, decorators
  - `records/` — LogRecord filters (context injection)
  - `integrations/` — framework middleware (ASGI, FastAPI, Celery, HTTPX, RQ, SQLAlchemy)
  - `otel/` — OpenTelemetry bridge (logs, traces, metrics, correlation, exporters)
  - `structlog/` — structlog bridge, processors, renderers
  - `rich/` — console factory, themes, render helpers
  - `testing/` — `reset_ultilog()`, capture, factories, fixtures
  - `utils/` — caller inference, env helpers, import tools

### Test layout

- `tests/unit/` — isolated behavior (18 files)
- `tests/integration/` — composition tests (4 files)
- `tests/e2e/` — subprocess/example validation (3 files)
- `tests/conftest.py` — autouse `clean_logging_state` fixture resets root logger, env, and ultilog state per test

### Release

- Version in `pyproject.toml`
- Git tag `v*` triggers `.github/workflows/release.yml` (PyPI trusted publishing)

## Coding guidelines

- Keep modules typed and mypy-strict-friendly
- Google-style docstrings
- Pydantic v2 models for all configuration
- Prefer explicit, testable helpers over framework-coupled logic
- Preserve existing import style and module conventions
- No broad refactors unless requested
- Add tests with every feature
