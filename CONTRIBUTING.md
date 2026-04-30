# Contributing

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
