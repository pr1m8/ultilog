# Scaffold Checklist

## Package Root

- [x] `pyproject.toml`
- [x] `README.md`
- [x] `LICENSE`
- [x] `CHANGELOG.md`
- [x] `CONTRIBUTING.md`
- [x] `SECURITY.md`
- [x] `Makefile`
- [x] `noxfile.py`
- [x] `.pre-commit-config.yaml`
- [x] GitHub Actions skeleton

## Source Package

- [x] public API
- [x] bootstrap state
- [x] settings models
- [x] handler factories
- [x] formatter helpers
- [x] context helpers
- [x] ASGI/FastAPI shapes
- [x] optional import helpers
- [x] diagnostics CLI
- [x] testing utilities

## Tests

- [x] unit tests
- [x] integration tests
- [x] e2e layout
- [x] example subprocess tests
- [x] fixture isolation

## Documentation

- [x] quickstart
- [x] architecture
- [x] testing strategy
- [x] cookbook
- [x] roadmap
- [x] ADRs
- [x] module reference pages

## Deferred Implementation

- [ ] full structlog processor bridge
- [ ] OpenTelemetry provider setup
- [ ] OTLP exporter configuration
- [ ] Prometheus/Grafana/Loki/Jaeger specific docs
- [ ] FastAPI app-level request/response logging policy
- [ ] Celery/RQ worker decorators
