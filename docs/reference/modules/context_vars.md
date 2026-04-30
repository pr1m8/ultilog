# `ultilog.context.vars`

Contextvars storage for execution-scoped fields.

## Design Role

This module exists as part of the layered package architecture. The top-level
API should stay small, but implementation details need stable homes so the
package can grow without becoming a single monolithic configuration file.

## Common Usage

Most users should not need to import this module directly unless they are
composing custom logging behavior or contributing to the package.

## Testing Expectations

Tests for this module should prefer isolated behavior over full application
bootstrapping. Global logging state should be reset before and after tests.

## Future Growth

This module may gain additional options as `ultilog` adds structured logging,
OpenTelemetry, and framework integration support. New behavior should remain
additive whenever possible.
