"""Nox sessions for ``ultilog``.

Purpose
-------
Provide repeatable local and CI automation for tests, linting, typing, docs,
and examples.

Design
------
The sessions delegate to PDM so dependency resolution stays centralized in
``pyproject.toml``.
"""

from __future__ import annotations

import nox

nox.options.sessions = ["tests", "lint", "typecheck"]


@nox.session(python="3.13")
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.run("pdm", "sync", "-G", "dev", external=True)
    session.run("pdm", "run", "pytest", external=True)


@nox.session(python="3.13")
def lint(session: nox.Session) -> None:
    """Run Ruff checks."""
    session.run("pdm", "sync", "-G", "dev", external=True)
    session.run("pdm", "run", "ruff", "check", ".", external=True)


@nox.session(python="3.13")
def typecheck(session: nox.Session) -> None:
    """Run Mypy."""
    session.run("pdm", "sync", "-G", "dev", external=True)
    session.run("pdm", "run", "mypy", "src/ultilog", external=True)


@nox.session(python="3.13")
def docs(session: nox.Session) -> None:
    """Build documentation."""
    session.run("pdm", "sync", "-G", "docs", external=True)
    session.run("pdm", "run", "mkdocs", "build", external=True)
