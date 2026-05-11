# Changelog

## 0.4.0

### Added

- `setup_auto()` — environment-aware setup that chooses Rich dev logging,
  quiet test logging, or JSON production logging based on `ULTILOG_ENV`,
  `APP_ENV`, `ENVIRONMENT`, or `ENV`.
- `ultilog bootstrap` project planner for detecting dependencies, grouping
  recommended OpenTelemetry instrumentation, typing stubs, pytest, coverage,
  and formatting packages by pyproject target.
- `ultilog bootstrap --json`, `--commands`, `--snippet`, and `--apply --group`
  modes for project generators, copy-paste setup, startup snippets, and
  explicit package-manager setup.
- OpenTelemetry zero-code bootstrap guidance for `opentelemetry-bootstrap -a
  requirements`, `opentelemetry-bootstrap -a install`, and
  `opentelemetry-instrument`.
- Project bootstrap documentation and downstream-project e2e coverage.

### Changed

- Improved bootstrap CLI output with Rich panels and grouped install tables.
- Fixed strict mypy issues in settings, Rich handler typing, FastAPI middleware
  registration, and constants.

## 0.3.0

### Added

- `setup_dev()` — one-line super-pretty Rich setup (DEBUG, tracebacks with locals)
- `setup_prod()` — one-line JSON setup with optional `service_name` for OTel
- `setup_test()` — one-line plain WARNING setup for test suites
- Auto-attached `TraceCorrelationFilter` when `opentelemetry` is importable, so `trace_id` / `span_id` flow into log records under any active span without manual wiring
- Dev preset now enables `rich_tracebacks` and `tracebacks_show_locals` for richer error reports
- Renumbered and rewrote all examples to use the new helpers; added `08_otel_correlation.py`

### Changed

- Cleaned up examples folder: removed duplicate-numbered files (`04_environment_overrides.py`) and future-API stubs (`05_future_context_scope.py`, `06_future_otel.py`)

## 0.2.0

### Added

- Settings validation for invalid combinations (rich mode / rich disabled auto-fix, optional dep checks)
- structlog processor chains (`get_default_processors`, `get_json_processors`, `get_console_processors`)
- structlog renderer helpers with mode-aware selection
- structlog bridge availability check (dynamic `find_spec`)
- OpenTelemetry trace setup (`configure_otel_traces`)
- OpenTelemetry log export (`configure_otel_logs`)
- OpenTelemetry metrics setup (`configure_otel_metrics`)
- OpenTelemetry all-in-one exporter setup (`configure_exporters`)
- OpenTelemetry context propagation (W3C TraceContext + Baggage)
- Celery integration with signal-based context binding
- httpx integration with request/response logging hooks
- RQ integration with job context binding
- SQLAlchemy integration with engine logging configuration
- CLI `show-config` subcommand for dumping effective settings
- CLI `validate` subcommand for configuration checks
- Expanded diagnostics: formatters, env overrides, python version, dependency versions
- `validate_config()` helper for programmatic config validation
- Console script entry point (`ultilog` command)
- PyPI classifiers, keywords, and project URLs
- 39 new tests (79 total) covering settings validation, context decorators, async isolation, bootstrap reconfiguration, structlog, OTel, CLI, and more
- CLAUDE.md for Claude Code guidance
- Comprehensive documentation: concept guides, integration guides, API reference, settings reference

### Fixed

- All ruff lint errors resolved (import sorting, line length, type aliases, unused directives)
- New mypy errors from added code resolved

## 0.1.0 - Scaffold

Initial full scaffold for `ultilog`.

Added:

- zero-config logger access
- optional setup path
- Rich handler factory
- plain and JSON modes
- contextvars helpers
- ASGI/FastAPI integration shapes
- optional integration stubs
- testing helpers
- docs and examples
