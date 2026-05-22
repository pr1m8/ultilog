# Project Bootstrap

`ultilog bootstrap` turns a project's dependency graph into a practical logging
and observability setup plan. It does not install anything by default.

```bash
python -m ultilog bootstrap
python -m ultilog bootstrap --json
python -m ultilog bootstrap --commands
```

The planner reads `pyproject.toml`, scans imports, detects the package manager,
and groups package recommendations by pyproject target.

## Groups

| Group | Kind | Purpose |
|-------|------|---------|
| `observability-core` | optional dependency | OpenTelemetry API/SDK/exporter, zero-code logging, system metrics, and core web/client/database instrumentation |
| `observability-extra` | optional dependency | Less-universal instrumentation such as Celery, grpc, botocore, urllib3, aiohttp, and asyncpg |
| `formatting` | dependency group | Ruff and formatting tools |
| `typing` | dependency group | Type checkers and `types-*` stub packages |
| `test-core` | dependency group | Pytest and common pytest plugins |
| `coverage` | dependency group | Coverage tooling |

For PDM projects, optional dependency groups are written with `-G`:

```bash
pdm add --no-sync -G observability-core opentelemetry-exporter-otlp
```

Development dependency groups use `-d -G`:

```bash
pdm add --no-sync -d -G typing mypy pyright types-requests
pdm add --no-sync -d -G test-core pytest pytest-cov pytest-mock
```

Run selected setup groups explicitly with `--apply`:

```bash
python -m ultilog bootstrap --apply --group observability-core
python -m ultilog bootstrap --apply --group typing --group test-core
python -m ultilog bootstrap --apply --all
```

`--apply` runs the package-manager commands shown in the plan. It requires
either `--group` or `--all`, so it will not apply every group by accident.
For PDM, generated commands include `--no-sync`; they update `pyproject.toml`
and the lockfile without pruning the active virtualenv. Run `pdm sync` with
the groups you actually want after reviewing the changes.

## Environment Check

Human output and `--apply` run a read-only dependency check before changing
anything:

```bash
pdm run python -m pip check
```

When a conflict is found, `ultilog bootstrap` prints the exact `pip check`
line and a repair command. For example, if an OpenTelemetry package requires a
newer `opentelemetry-util-genai`, the report will point at that requirement
before any grouped install command runs. Use `--no-env-check` to skip this
check or `--ignore-conflicts` if you intentionally want to continue.

Machine-readable plans stay read-only and avoid shelling out by default. Add
`--check-environment` with `--json` or `--commands` when tooling needs the
environment check in the output.

## OpenTelemetry Zero-Code

OpenTelemetry already ships bootstrap commands that inspect installed packages
and find matching instrumentation packages:

```bash
pdm run opentelemetry-bootstrap -a requirements
```

Use `requirements` when you want to inspect or capture the generated package
list. Use `install` only after reviewing that list, because it installs into
the active environment directly and then runs its own dependency check.

```bash
pdm run opentelemetry-bootstrap -a install
```

Run an application under zero-code instrumentation with:

```bash
pdm run opentelemetry-instrument python -m your_app
```

`ultilog bootstrap` includes these commands in the plan so a project can choose
between managed pyproject groups and OpenTelemetry's direct environment
bootstrap.

## Application Setup

Generate the startup snippet for a service:

```bash
python -m ultilog bootstrap --snippet --service-name orders-api
```

It calls `setup_auto(service_name="orders-api")`, which configures:

- Rich output and tracebacks for local development
- quiet plain output for test and CI-like environments
- JSON output and OTel trace/log correlation when `APP_ENV=prod`,
  `APP_ENV=production`, `ULTILOG_ENV=prod`, or `ULTILOG_ENV=production`

Use the snippet at your process entrypoint before creating loggers in the rest
of the application.

## Downstream Project Flow

For a PDM app with FastAPI and SQLAlchemy:

```bash
cd my-api
python -m pip install ultilog
python -m ultilog bootstrap
python -m ultilog bootstrap --commands
python -m ultilog bootstrap --apply --group observability-core
python -m ultilog bootstrap --apply --group typing
python -m ultilog bootstrap --snippet --service-name my-api
```

Put the generated snippet in a small module such as `src/my_api/logging.py`,
then import that module from your application entrypoint before creating
loggers elsewhere:

```python
import my_api.logging  # configures ultilog once

from ultilog import get_logger

log = get_logger(__name__)
```

Then inspect OpenTelemetry's own detected package list:

```bash
pdm run opentelemetry-bootstrap -a requirements
```

Run the app under zero-code instrumentation:

```bash
pdm run opentelemetry-instrument python -m my_api
```

## JSON Output

The JSON form is intended for project generators and templates:

```bash
python -m ultilog bootstrap --json
```

It includes detected dependencies, imported modules, package statuses, grouped
install commands, and zero-code commands.
