# AGENTS.md

## Purpose

This repository contains `ultilog`, a Python package for ergonomic logging.
Agents working here should prioritize small, test-backed changes and keep the
public API simple.

## Environment

- Python: `3.13+`
- Package manager: `pdm`
- Source root: `src/ultilog`
- Tests: `tests/` (`unit`, `integration`, `e2e`)

## Fast Start

- Install deps: `pdm sync -G dev -G docs`
- Run tests: `pdm run pytest`
- Run lint: `pdm run ruff check .`
- Typecheck: `pdm run mypy src/ultilog`
- Build docs: `pdm run mkdocs build`

## E2E Commands

- CLI doctor: `pdm run python -m ultilog doctor --json`
- Demo app: `pdm run python examples/10_demo_app.py`

Use `pdm run ...` for executable commands so runtime dependencies resolve from
the project virtualenv.

## Coding Guidelines

- Keep new modules typed and mypy-friendly.
- Prefer explicit, testable helpers over framework-coupled logic.
- Preserve current import style and docstring conventions.
- Avoid broad refactors unless requested.

## Release Notes

- Version is declared in `pyproject.toml`.
- Release workflow is in `.github/workflows/release.yml`.
- Tagging `v*` triggers build + PyPI publish workflow.
