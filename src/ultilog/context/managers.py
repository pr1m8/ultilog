"""Context manager helpers for ``ultilog``.

Purpose
-------
Provide ergonomic scoped logging context helpers.

Design
------
The context manager uses context variable tokens, so nested and async-adjacent
scopes restore prior values predictably.

Examples
--------
>>> from ultilog.context.vars import get_context
>>> with logging_context(request_id="x"):
...     assert get_context()["request_id"] == "x"
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from ultilog.context.vars import bind_context, reset_context


@contextmanager
def logging_context(**values: Any) -> Iterator[None]:
    """Temporarily bind logging context values.

    Args:
        **values: Context key-value pairs.

    Returns:
        Iterator that yields once inside the context.

    Raises:
        ValueError: If context token reset fails.

    Examples:
        >>> with logging_context(request_id="req_1"):
        ...     pass
    """
    token = bind_context(**values)
    try:
        yield
    finally:
        reset_context(token)


__all__ = ["logging_context"]
