# Roadmap

## Phase 1: Core Ergonomics

- zero-config `get_logger()`
- optional `setup(...)`
- Rich handler factory
- plain and JSON modes
- context values on records
- testing helpers

## Phase 2: Settings and Presets

- richer settings models
- preset registry
- exportable config summaries
- environment reference docs

## Phase 3: Structlog

- structlog processor presets
- JSON renderer bridge
- structured exception handling
- test helpers for structured events

## Phase 4: OpenTelemetry

- trace/span correlation
- logging handler bridge
- OTLP exporter setup
- propagation helpers

## Phase 5: Framework Integrations

- ASGI middleware
- FastAPI helper
- Celery/RQ workers
- httpx and SQLAlchemy instrumentation helpers

## Phase 6: Developer Experience

- CLI diagnostics
- rich diagnostics tables
- docs site
- copier or cookiecutter template
