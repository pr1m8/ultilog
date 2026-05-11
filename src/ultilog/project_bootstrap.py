"""Project bootstrap planning for ``ultilog``.

Purpose
-------
Inspect a Python project and build a non-destructive plan for logging,
OpenTelemetry zero-code instrumentation, typing stubs, and test tooling.

Design
------
The planner reads ``pyproject.toml`` when available, lightly scans Python
imports, and compares detected dependencies against known package maps. It
returns commands the user can run instead of installing packages implicitly.
"""

from __future__ import annotations

import ast
import re
import shutil
import subprocess
import tomllib
from dataclasses import asdict, dataclass
from importlib.metadata import PackageNotFoundError, distributions, version
from pathlib import Path
from shlex import join
from shlex import split as split_command
from typing import Any, Literal

PackageManager = Literal["pdm", "uv", "poetry", "pip"]
InstallGroupKind = Literal["runtime", "optional", "dev"]

_REQ_NAME_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)")
_SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pypackages__",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "site-packages",
    "venv",
}

OTEL_BASE_PACKAGES = {
    "opentelemetry-api": "OpenTelemetry API used by instrumented libraries.",
    "opentelemetry-exporter-otlp": "OTLP exporters for real collector endpoints.",
    "opentelemetry-sdk": "Provider and processor implementation for traces, metrics, and logs.",
    "opentelemetry-instrumentation": (
        "Provides opentelemetry-bootstrap and opentelemetry-instrument."
    ),
    "opentelemetry-instrumentation-logging": "Zero-code stdlib logging instrumentation.",
    "opentelemetry-instrumentation-system-metrics": "Host/runtime system metrics.",
}

OTEL_INSTRUMENTATION_PACKAGES = {
    "aiohttp": "opentelemetry-instrumentation-aiohttp-client",
    "aio-pika": "opentelemetry-instrumentation-aio-pika",
    "aioboto3": "opentelemetry-instrumentation-botocore",
    "aiobotocore": "opentelemetry-instrumentation-botocore",
    "asyncpg": "opentelemetry-instrumentation-asyncpg",
    "boto3": "opentelemetry-instrumentation-botocore",
    "botocore": "opentelemetry-instrumentation-botocore",
    "celery": "opentelemetry-instrumentation-celery",
    "django": "opentelemetry-instrumentation-django",
    "fastapi": "opentelemetry-instrumentation-fastapi",
    "flask": "opentelemetry-instrumentation-flask",
    "grpcio": "opentelemetry-instrumentation-grpc",
    "httpx": "opentelemetry-instrumentation-httpx",
    "kafka-python": "opentelemetry-instrumentation-kafka-python",
    "pika": "opentelemetry-instrumentation-pika",
    "pymongo": "opentelemetry-instrumentation-pymongo",
    "psycopg": "opentelemetry-instrumentation-psycopg",
    "psycopg2": "opentelemetry-instrumentation-psycopg2",
    "redis": "opentelemetry-instrumentation-redis",
    "requests": "opentelemetry-instrumentation-requests",
    "rq": "opentelemetry-instrumentation-rq",
    "sqlalchemy": "opentelemetry-instrumentation-sqlalchemy",
    "starlette": "opentelemetry-instrumentation-starlette",
    "urllib3": "opentelemetry-instrumentation-urllib3",
}

OTEL_ASGI_TRIGGER_DEPENDENCIES = {"fastapi", "starlette"}
OTEL_CORE_INSTRUMENTATION_SOURCES = {
    "asgi",
    "fastapi",
    "httpx",
    "psycopg",
    "psycopg2",
    "redis",
    "sqlalchemy",
    "starlette",
}

IMPORT_TO_DISTRIBUTION = {
    "aio_pika": "aio-pika",
    "aiohttp": "aiohttp",
    "aioboto3": "aioboto3",
    "aiobotocore": "aiobotocore",
    "asyncpg": "asyncpg",
    "boto3": "boto3",
    "botocore": "botocore",
    "celery": "celery",
    "django": "django",
    "fastapi": "fastapi",
    "flask": "flask",
    "grpc": "grpcio",
    "httpx": "httpx",
    "kafka": "kafka-python",
    "opentelemetry": "opentelemetry-api",
    "pika": "pika",
    "pymongo": "pymongo",
    "psycopg": "psycopg",
    "redis": "redis",
    "requests": "requests",
    "rq": "rq",
    "sqlalchemy": "sqlalchemy",
    "starlette": "starlette",
    "urllib3": "urllib3",
    "yaml": "pyyaml",
}

TYPE_STUB_PACKAGES = {
    "mock": "types-mock",
    "protobuf": "types-protobuf",
    "pyyaml": "types-PyYAML",
    "python-dateutil": "types-python-dateutil",
    "pytz": "types-pytz",
    "redis": "types-redis",
    "requests": "types-requests",
    "setuptools": "types-setuptools",
    "toml": "types-toml",
}

DEV_TOOL_PACKAGES = {
    "coverage": ("coverage", "Coverage collection and reporting."),
    "mypy": ("typing", "Static type checking."),
    "pyright": ("typing", "Optional second static type checker."),
    "pytest": ("test-core", "Test runner."),
    "pytest-cov": ("test-core", "Pytest coverage integration."),
    "pytest-mock": ("test-core", "Pytest fixture support for mocks."),
    "ruff": ("formatting", "Fast linting and formatting."),
}


@dataclass(frozen=True)
class PackageStatus:
    """Status for a recommended package."""

    package: str
    reason: str
    declared: bool
    installed: bool
    source: str | None = None


@dataclass(frozen=True)
class PackageInstallGroup:
    """Packages that should be installed into one pyproject target."""

    name: str
    kind: InstallGroupKind
    packages: tuple[PackageStatus, ...]
    command: str | None


@dataclass(frozen=True)
class BootstrapCommandResult:
    """Result from applying one bootstrap install command."""

    group: str
    command: str
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class ZeroCodeInstrumentation:
    """Commands and availability for OTel zero-code instrumentation."""

    available: bool
    requirements_command: str
    install_command: str
    run_command: str


@dataclass(frozen=True)
class ProjectBootstrapPlan:
    """Serializable bootstrap plan for a project."""

    root: str
    pyproject_path: str | None
    package_manager: PackageManager
    detected_dependencies: tuple[str, ...]
    imported_modules: tuple[str, ...]
    otel_base_packages: tuple[PackageStatus, ...]
    otel_instrumentation_packages: tuple[PackageStatus, ...]
    dev_tool_packages: tuple[PackageStatus, ...]
    type_stub_packages: tuple[PackageStatus, ...]
    install_groups: tuple[PackageInstallGroup, ...]
    zero_code: ZeroCodeInstrumentation
    commands: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the plan."""
        return asdict(self)


def build_project_bootstrap_plan(path: str | Path = ".") -> ProjectBootstrapPlan:
    """Build a non-destructive package bootstrap plan for a project.

    Args:
        path: Project root or a path inside the project.

    Returns:
        A project bootstrap plan.
    """
    root, pyproject_path = _resolve_project_root(Path(path))
    package_manager = _detect_package_manager(root, pyproject_path)
    parsed = _read_pyproject(pyproject_path)
    declared_dependencies = _declared_dependencies(parsed)
    imported_modules = _discover_imports(root)
    import_dependencies = {
        _normalize_package_name(IMPORT_TO_DISTRIBUTION[module])
        for module in imported_modules
        if module in IMPORT_TO_DISTRIBUTION
    }
    detected_dependencies = tuple(sorted(declared_dependencies | import_dependencies))
    installed_packages = _installed_packages()

    otel_base = tuple(
        _status_for_package(
            package,
            reason=reason,
            declared_dependencies=declared_dependencies,
            installed_packages=installed_packages,
        )
        for package, reason in sorted(OTEL_BASE_PACKAGES.items())
    )
    instrumentable_dependencies = declared_dependencies | {
        dependency for dependency in import_dependencies if dependency in installed_packages
    }
    otel_instrumentations = _otel_instrumentation_statuses(
        instrumentable_dependencies=instrumentable_dependencies,
        declared_dependencies=declared_dependencies,
        installed_packages=installed_packages,
    )
    dev_tools = tuple(
        _status_for_package(
            package,
            reason=reason,
            declared_dependencies=declared_dependencies,
            installed_packages=installed_packages,
        )
        for package, (_group, reason) in sorted(DEV_TOOL_PACKAGES.items())
    )
    type_stubs = tuple(
        _status_for_package(
            stub_package,
            reason=f"Typing stubs for {dependency}.",
            declared_dependencies=declared_dependencies,
            installed_packages=installed_packages,
            source=dependency,
        )
        for dependency, stub_package in sorted(TYPE_STUB_PACKAGES.items())
        if dependency in detected_dependencies
    )

    install_groups = _build_install_groups(
        package_manager=package_manager,
        otel_base=otel_base,
        otel_instrumentations=otel_instrumentations,
        dev_tools=dev_tools,
        type_stubs=type_stubs,
    )
    commands = {
        f"add_{group.name.replace('-', '_')}": group.command
        for group in install_groups
        if group.command is not None
    }

    return ProjectBootstrapPlan(
        root=str(root),
        pyproject_path=str(pyproject_path) if pyproject_path is not None else None,
        package_manager=package_manager,
        detected_dependencies=detected_dependencies,
        imported_modules=imported_modules,
        otel_base_packages=otel_base,
        otel_instrumentation_packages=otel_instrumentations,
        dev_tool_packages=dev_tools,
        type_stub_packages=type_stubs,
        install_groups=install_groups,
        zero_code=_zero_code_commands(package_manager, installed_packages),
        commands=commands,
    )


def setup_snippet(*, service_name: str = "my-app") -> str:
    """Return a small application bootstrap snippet.

    Args:
        service_name: Service name used by production logging and OTel resources.

    Returns:
        Python source text that configures ``ultilog``.
    """
    return f'''"""Application logging setup."""

from __future__ import annotations

from ultilog import get_logger, setup_auto


setup_auto(service_name="{service_name}")
log = get_logger(__name__)
'''


def apply_project_bootstrap_plan(
    plan: ProjectBootstrapPlan,
    *,
    groups: set[str] | None = None,
) -> tuple[BootstrapCommandResult, ...]:
    """Run missing package install commands from a bootstrap plan.

    Args:
        plan: Bootstrap plan to apply.
        groups: Optional group names to apply. Defaults to all groups with commands.

    Returns:
        One result per executed command.

    Raises:
        RuntimeError: If any command exits non-zero.
    """
    results: list[BootstrapCommandResult] = []
    for install_group in plan.install_groups:
        if install_group.command is None:
            continue
        if groups is not None and install_group.name not in groups:
            continue

        completed = subprocess.run(
            split_command(install_group.command),
            cwd=plan.root,
            text=True,
            capture_output=True,
            check=False,
        )
        result = BootstrapCommandResult(
            group=install_group.name,
            command=install_group.command,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
        results.append(result)
        if completed.returncode != 0:
            msg = f"Bootstrap command failed for group {install_group.name!r}."
            raise RuntimeError(msg)

    return tuple(results)


def _resolve_project_root(path: Path) -> tuple[Path, Path | None]:
    resolved = path.expanduser().resolve()
    if resolved.is_file() and resolved.name == "pyproject.toml":
        return resolved.parent, resolved
    start = resolved if resolved.is_dir() else resolved.parent
    for candidate in (start, *start.parents):
        pyproject = candidate / "pyproject.toml"
        if pyproject.exists():
            return candidate, pyproject
    return start, None


def _read_pyproject(pyproject_path: Path | None) -> dict[str, Any]:
    if pyproject_path is None:
        return {}
    with pyproject_path.open("rb") as file:
        data = tomllib.load(file)
    return data if isinstance(data, dict) else {}


def _declared_dependencies(data: dict[str, Any]) -> set[str]:
    dependencies: set[str] = set()
    project = _dict_value(data, "project")
    dependencies.update(_names_from_requirements(_list_value(project, "dependencies")))

    optional_dependencies = _dict_value(project, "optional-dependencies")
    for values in optional_dependencies.values():
        if isinstance(values, list):
            dependencies.update(_names_from_requirements(values))

    dependency_groups = _dict_value(data, "dependency-groups")
    for values in dependency_groups.values():
        if isinstance(values, list):
            dependencies.update(_names_from_requirements(values))

    return dependencies


def _names_from_requirements(requirements: list[Any]) -> set[str]:
    names: set[str] = set()
    for requirement in requirements:
        if not isinstance(requirement, str):
            continue
        match = _REQ_NAME_RE.match(requirement)
        if match is not None:
            names.add(_normalize_package_name(match.group(1)))
    return names


def _discover_imports(root: Path, *, max_python_files: int = 500) -> tuple[str, ...]:
    imports: set[str] = set()
    count = 0
    for file_path in root.rglob("*.py"):
        if _should_skip_path(file_path, root):
            continue
        count += 1
        if count > max_python_files:
            break
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.partition(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imports.add(node.module.partition(".")[0])
    return tuple(sorted(imports))


def _should_skip_path(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in _SKIP_DIRS for part in relative.parts)


def _installed_packages() -> set[str]:
    return {
        _normalize_package_name(distribution.metadata["Name"])
        for distribution in distributions()
        if distribution.metadata.get("Name")
    }


def _status_for_package(
    package: str,
    *,
    reason: str,
    declared_dependencies: set[str],
    installed_packages: set[str],
    source: str | None = None,
) -> PackageStatus:
    normalized = _normalize_package_name(package)
    return PackageStatus(
        package=package,
        reason=reason,
        declared=normalized in declared_dependencies,
        installed=normalized in installed_packages,
        source=source,
    )


def _otel_instrumentation_statuses(
    *,
    instrumentable_dependencies: set[str],
    declared_dependencies: set[str],
    installed_packages: set[str],
) -> tuple[PackageStatus, ...]:
    statuses: list[PackageStatus] = []
    candidates = {
        dependency: package
        for dependency, package in OTEL_INSTRUMENTATION_PACKAGES.items()
        if dependency in instrumentable_dependencies
    }
    if instrumentable_dependencies & OTEL_ASGI_TRIGGER_DEPENDENCIES:
        candidates["asgi"] = "opentelemetry-instrumentation-asgi"

    for dependency, package in sorted(candidates.items()):
        statuses.append(
            _status_for_package(
                package,
                reason=f"Instrumentation for {dependency}.",
                declared_dependencies=declared_dependencies,
                installed_packages=installed_packages,
                source=dependency,
            )
        )
    return tuple(statuses)


def _missing_declared_package_names(statuses: tuple[PackageStatus, ...]) -> tuple[str, ...]:
    return tuple(status.package for status in statuses if not status.declared)


def _build_install_groups(
    *,
    package_manager: PackageManager,
    otel_base: tuple[PackageStatus, ...],
    otel_instrumentations: tuple[PackageStatus, ...],
    dev_tools: tuple[PackageStatus, ...],
    type_stubs: tuple[PackageStatus, ...],
) -> tuple[PackageInstallGroup, ...]:
    groups: list[PackageInstallGroup] = []
    observability_core = tuple(
        status
        for status in (otel_base + otel_instrumentations)
        if status.source is None or status.source in OTEL_CORE_INSTRUMENTATION_SOURCES
    )
    observability_extra = tuple(
        status
        for status in otel_instrumentations
        if status.source is not None and status.source not in OTEL_CORE_INSTRUMENTATION_SOURCES
    )
    groups.append(
        _package_install_group(
            package_manager=package_manager,
            name="observability-core",
            kind="optional",
            statuses=observability_core,
        )
    )
    if observability_extra:
        groups.append(
            _package_install_group(
                package_manager=package_manager,
                name="observability-extra",
                kind="optional",
                statuses=observability_extra,
            )
        )

    dev_group_names = sorted({group for group, _reason in DEV_TOOL_PACKAGES.values()})
    for group_name in dev_group_names:
        statuses = tuple(
            status
            for status in dev_tools
            if DEV_TOOL_PACKAGES[status.package][0] == group_name
        )
        if group_name == "typing":
            statuses = statuses + type_stubs
        groups.append(
            _package_install_group(
                package_manager=package_manager,
                name=group_name,
                kind="dev",
                statuses=statuses,
            )
        )

    return tuple(group for group in groups if group.packages)


def _package_install_group(
    *,
    package_manager: PackageManager,
    name: str,
    kind: InstallGroupKind,
    statuses: tuple[PackageStatus, ...],
) -> PackageInstallGroup:
    missing = _missing_declared_package_names(statuses)
    command = (
        _install_command(package_manager, missing, kind=kind, group=name)
        if missing
        else None
    )
    return PackageInstallGroup(
        name=name,
        kind=kind,
        packages=statuses,
        command=command,
    )


def _install_command(
    package_manager: PackageManager,
    packages: tuple[str, ...],
    *,
    kind: InstallGroupKind = "runtime",
    group: str | None = None,
) -> str:
    if package_manager == "pdm":
        base = ["pdm", "add"]
        if kind == "dev" and group is not None:
            base.extend(["-d", "-G", group])
        elif kind == "optional" and group is not None:
            base.extend(["-G", group])
        return join([*base, *packages])
    if package_manager == "uv":
        base = ["uv", "add"]
        if kind == "dev" and group is not None:
            base.extend(["--group", group])
        elif kind == "optional" and group is not None:
            base.extend(["--optional", group])
        return join([*base, *packages])
    if package_manager == "poetry":
        base = ["poetry", "add"]
        if kind == "dev" and group is not None:
            base.extend(["--group", group])
        elif kind == "optional":
            base.append("--optional")
        return join([*base, *packages])
    return join(["python", "-m", "pip", "install", *packages])


def _zero_code_commands(
    package_manager: PackageManager,
    installed_packages: set[str],
) -> ZeroCodeInstrumentation:
    prefix = _run_prefix(package_manager)
    return ZeroCodeInstrumentation(
        available=(
            "opentelemetry-instrumentation" in installed_packages
            or shutil.which("opentelemetry-bootstrap") is not None
        ),
        requirements_command=f"{prefix}opentelemetry-bootstrap -a requirements",
        install_command=f"{prefix}opentelemetry-bootstrap -a install",
        run_command=f"{prefix}opentelemetry-instrument python -m your_app",
    )


def _run_prefix(package_manager: PackageManager) -> str:
    if package_manager == "pdm":
        return "pdm run "
    if package_manager == "uv":
        return "uv run "
    if package_manager == "poetry":
        return "poetry run "
    return ""


def _detect_package_manager(root: Path, pyproject_path: Path | None) -> PackageManager:
    if (root / "pdm.lock").exists():
        return "pdm"
    if (root / "uv.lock").exists():
        return "uv"
    if (root / "poetry.lock").exists():
        return "poetry"
    if pyproject_path is not None:
        data = _read_pyproject(pyproject_path)
        if "tool" in data and isinstance(data["tool"], dict) and "pdm" in data["tool"]:
            return "pdm"
    return "pip"


def _dict_value(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def _list_value(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def _normalize_package_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def installed_version(package: str) -> str | None:
    """Return the installed version for a package, if available."""
    try:
        return version(package)
    except PackageNotFoundError:
        return None


__all__ = [
    "DEV_TOOL_PACKAGES",
    "OTEL_BASE_PACKAGES",
    "OTEL_INSTRUMENTATION_PACKAGES",
    "TYPE_STUB_PACKAGES",
    "BootstrapCommandResult",
    "InstallGroupKind",
    "PackageInstallGroup",
    "PackageStatus",
    "ProjectBootstrapPlan",
    "ZeroCodeInstrumentation",
    "apply_project_bootstrap_plan",
    "build_project_bootstrap_plan",
    "installed_version",
    "setup_snippet",
]
