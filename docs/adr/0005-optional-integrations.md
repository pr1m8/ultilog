# ADR: Optional integrations

## Status

Accepted for scaffold.

## Context

`ultilog` is intended to start as a small ergonomic logging package and grow
into a layered observability toolkit. The project needs decisions that keep
phase-one implementation simple without blocking structured logging,
OpenTelemetry, or framework integrations later.

## Decision

Structlog, OpenTelemetry, and web frameworks should be optional extras that degrade gracefully when dependencies are missing.

## Consequences

Positive consequences:

- The public API remains easy to explain.
- Internal modules can evolve without breaking simple use cases.
- Tests can target small behavior slices.
- Optional integrations can be added without bloating the default install.

Tradeoffs:

- Some advanced users may need to import lower-level helpers.
- The package must maintain clear documentation around where each concern
  belongs.
- The bootstrap layer needs careful tests to avoid surprising global state.

## Implementation Notes

The scaffold should include enough module boundaries to show the future
architecture, but only a subset should be fully implemented at first. The
implemented path should always remain runnable.
