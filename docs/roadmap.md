# Roadmap

## Completed

### Phase 1: Core Ergonomics

- [x] Zero-config `get_logger()` with caller name inference
- [x] Optional `setup(...)` with presets and overrides
- [x] Advanced `configure(settings)` with full `UltilogSettings`
- [x] Rich console handler factory
- [x] Plain and JSON output modes
- [x] `contextvars`-based context with managers, decorators, and request helpers
- [x] `ContextFilter` for automatic log record injection
- [x] Testing helpers (`reset_ultilog`, `capture_logs`)
- [x] CLI with `doctor`, `demo`, `show-config`, and `validate`
- [x] Unit, integration, and e2e test suite

### Phase 2: Settings and Presets

- [x] Pydantic v2 settings models for all subsystems
- [x] Preset system (dev, test, prod)
- [x] Settings validation for invalid combinations
- [x] Environment variable overrides (`ULTILOG_` prefix)
- [x] Exportable config summaries and dictConfig builder

### Phase 3: structlog

- [x] `configure_structlog()` with processor chain setup
- [x] Pre-built processor chains (default, JSON, console)
- [x] Renderer helpers mapping modes to structlog renderers
- [x] Bridge availability check

### Phase 4: OpenTelemetry

- [x] Trace setup (`configure_otel_traces`)
- [x] Log export (`configure_otel_logs`)
- [x] Metric setup (`configure_otel_metrics`)
- [x] All-in-one exporter setup via `OTelSettings`
- [x] Trace/log correlation filter
- [x] Context propagation (W3C TraceContext + Baggage)
- [x] Availability check

### Phase 5: Framework Integrations

- [x] ASGI middleware with request context
- [x] FastAPI installation helper
- [x] Celery signal-based context binding
- [x] httpx request/response logging hooks
- [x] RQ worker job context
- [x] SQLAlchemy engine logging configuration

### Phase 6: Packaging and Release

- [x] Console script entry point
- [x] PyPI classifiers, keywords, and project URLs
- [x] GitHub Actions CI and release workflows
- [x] Pre-commit hooks (ruff, yaml, toml)
- [x] Documentation site with MkDocs Material

## Future

- [ ] Prometheus / Grafana / Loki / Jaeger specific recipes
- [ ] FastAPI request/response body logging policies
- [ ] Async-native context decorators
- [ ] Log sampling and rate limiting
- [ ] Copier or cookiecutter project template
