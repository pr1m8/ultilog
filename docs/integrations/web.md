# Web Framework Integrations

## FastAPI

Install logging context middleware on a FastAPI application:

```python
from fastapi import FastAPI
from ultilog.integrations import install_fastapi_logging

app = FastAPI()
install_fastapi_logging(app)
```

Every request automatically gets logging context with:

- `request_id` -- from `X-Request-ID` header or auto-generated UUID
- `http.method` -- request method
- `http.path` -- request path

```python
from ultilog import get_logger

log = get_logger("api")

@app.get("/items")
async def list_items():
    log.info("listing items")  # request_id=... http.method=GET http.path=/items
    return []
```

### Custom request ID header

```python
install_fastapi_logging(app, request_id_header=b"x-correlation-id")
```

## ASGI Middleware

For any ASGI framework (Starlette, Litestar, etc.):

```python
from ultilog.integrations import UltilogASGIMiddleware

app = UltilogASGIMiddleware(app)
```

Or use the factory:

```python
from ultilog.integrations import install_asgi_logging

app = install_asgi_logging(app)
```

## Celery

Bind task metadata into logging context for every task execution:

```python
from celery import Celery
from ultilog.integrations import install_celery_logging

app = Celery("tasks")
install_celery_logging(app)
```

Every task gets context with `celery_task_id` and `celery_task_name`. Context is cleared after each task completes.

## httpx

Log outgoing HTTP requests and responses:

```python
import httpx
from ultilog.integrations import install_httpx_logging

client = httpx.Client()
install_httpx_logging(client)
```

Logs at DEBUG level with `http.method`, `http.url`, and `http.status_code`.

Works with both `httpx.Client` and `httpx.AsyncClient`.

## RQ (Redis Queue)

Bind job metadata into logging context:

```python
from rq import Worker
from ultilog.integrations import install_rq_logging

worker = Worker(queues)
install_rq_logging(worker)
```

Each job gets context with `rq_job_id` and `rq_func_name`.

## SQLAlchemy

Configure SQLAlchemy engine logging:

```python
import logging
from sqlalchemy import create_engine
from ultilog.integrations import install_sqlalchemy_logging

engine = create_engine("sqlite:///app.db")
install_sqlalchemy_logging(engine, level=logging.DEBUG, echo=True)
```

This sets the `sqlalchemy.engine` logger level and optionally enables query echo.
