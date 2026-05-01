# ultilog

Ergonomic Python logging that starts with zero config and scales to structured observability.

```python
from ultilog import get_logger

log = get_logger()
log.info("app.started")
```

## Documentation

- [Quickstart](quickstart.md) -- get running in 30 seconds
- [Architecture](architecture.md) -- how the package is structured
- [Cookbook](cookbook.md) -- common usage patterns
- [Testing](testing.md) -- testing strategy and helpers
- [Roadmap](roadmap.md) -- what's done and what's next

## Concepts

- [Bootstrap](concepts/bootstrap.md) -- lazy configuration and idempotency
- [Logger Lifecycle](concepts/logger-lifecycle.md) -- how loggers are created and named
- [Context](concepts/context.md) -- execution-scoped context binding
- [Presets](concepts/presets.md) -- dev, test, and prod defaults

## Reference

- [Public API](reference/public-api.md) -- `get_logger`, `setup`, `configure`, context helpers
- [Settings](reference/settings.md) -- presets, environment variables, advanced configuration

## Integrations

- [Rich](integrations/rich.md) -- Rich console handler (default)
- [structlog](integrations/structlog.md) -- structured logging processors
- [OpenTelemetry](integrations/otel.md) -- traces, logs, metrics
- [Web Frameworks](integrations/web.md) -- FastAPI, ASGI, Celery, httpx, RQ, SQLAlchemy
