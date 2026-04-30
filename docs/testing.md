# Testing Strategy

`ultilog` should be tested in layers.

## Unit Tests

Unit tests cover small deterministic pieces:

- settings models
- handler factories
- formatters
- state reset
- caller inference
- context helpers

## Integration Tests

Integration tests cover module composition:

- setup flow
- JSON mode
- plain mode with context
- ASGI middleware behavior
- optional integration availability

## End-to-End Tests

E2E tests should run examples and CLI flows in subprocesses once the runtime
stabilizes.

## Fixtures

The key fixture responsibility is logging isolation. Tests must not leak root
handlers, root levels, or package runtime state.

A good fixture should:

1. save root handlers and level,
2. reset `ultilog`,
3. clear `ULTILOG_*` env vars,
4. run the test,
5. restore logging state,
6. reset `ultilog` again.

## Downstream Testing Helpers

The package exposes `ultilog.testing.capture` and `ultilog.testing.reset` so
users can test applications that use `ultilog` without copying internals.
