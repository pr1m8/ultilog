# Contributing

## Repository

Canonical Git remote is **`pr1m8/ultilog`** (package name `ultilog`, one `t` after `u`):

- [https://github.com/pr1m8/ultilog](https://github.com/pr1m8/ultilog)

An older typo-named remote (`utillog`) may still exist on GitHub; ignore it in favor of **`ultilog`**.

## PyPI trusted publishing

Releases publish from `.github/workflows/release.yml` using the GitHub Environment **`pypi`**. In [PyPI](https://pypi.org/manage/account/publishing/), the trusted publisher for this project must reference:

- **Repository:** `pr1m8/ultilog`
- **Workflow:** `release.yml`
- **Environment:** `pypi`

If you previously configured `pr1m8/utillog`, update or replace that entry so it matches **`pr1m8/ultilog`**.

## Development Setup

```bash
pdm sync -G dev -G docs
pdm run pytest
pdm run ruff check .
pdm run mypy src/ultilog
```

## Running Tests

```bash
pdm run pytest                      # full suite
pdm run pytest tests/unit           # unit only
pdm run pytest tests/integration    # integration only
pdm run pytest tests/e2e            # e2e only
pdm run pytest -k test_name         # single test
```

## Design Principles

- Keep the public API small.
- Keep bootstrap idempotent and thread-safe.
- Keep context separate from logger construction.
- Keep optional integrations optional -- all framework/library imports must be lazy.
- Add tests with every feature.
- Keep modules typed and mypy-strict-friendly.

## Test Layers

- **unit** -- isolated component behavior
- **integration** -- module composition and flows
- **e2e** -- examples and CLI in subprocesses

## Code Style

- Python 3.13+
- Full type hints (mypy strict mode)
- Google-style docstrings
- Pydantic v2 models for configuration
- Ruff for linting and formatting (line length 100)
- No hidden network calls

## Making Changes

1. Create a branch from `main`.
2. Make small, focused changes with tests.
3. Run `pdm run pytest && pdm run ruff check .` before pushing.
4. Open a pull request against `main`.
