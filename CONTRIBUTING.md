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
pdm sync -G dev
pdm run pytest
```

## Design Principles

- Keep the public API small.
- Keep bootstrap idempotent.
- Keep context separate from logger construction.
- Keep optional integrations optional.
- Add tests with every feature.

## Test Layers

- unit tests for isolated behavior
- integration tests for composition
- e2e tests for examples and CLI behavior

## Code Style

- Python 3.13+
- full type hints
- Google-style docstrings
- Pydantic v2 models for configuration
- no hidden network calls
