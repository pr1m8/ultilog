"""Context variable storage for ``ultilog``.

Purpose
-------
Store execution-scoped logging context in ``contextvars``.

Design
------
The context is intentionally separate from logger construction. It can be bound
at request, job, task, or manual scope boundaries and then injected into records
by ``ContextFilter``.

Examples
--------
>>> clear_context()
>>> bind_context(request_id="r1")
>>> get_context()["request_id"]
'r1'
"""

from __future__ import annotations

from contextvars import ContextVar, Token
from types import MappingProxyType
from typing import Any, Mapping

_context: ContextVar[dict[str, Any]] = ContextVar("ultilog_context", default={})


def get_context() -> Mapping[str, Any]:
    """Return current context values.

    Args:
        None.

    Returns:
        Read-only mapping of current context.

    Raises:
        None.

    Examples:
        >>> isinstance(get_context(), Mapping)
        True
    """
    return MappingProxyType(dict(_context.get()))


def set_context(values: Mapping[str, Any]) -> Token[dict[str, Any]]:
    """Set current context values.

    Args:
        values: Context values.

    Returns:
        Context variable token that can be used to reset the context.

    Raises:
        None.

    Examples:
        >>> token = set_context({"request_id": "x"})
        >>> reset_context(token)
    """
    return _context.set(dict(values))


def bind_context(**values: Any) -> Token[dict[str, Any]]:
    """Merge values into the current context.

    Args:
        **values: Context values to merge.

    Returns:
        Context variable token that can be reset.

    Raises:
        None.

    Examples:
        >>> clear_context()
        >>> token = bind_context(component="worker")
        >>> get_context()["component"]
        'worker'
        >>> reset_context(token)
    """
    merged = {**_context.get(), **values}
    return _context.set(merged)


def reset_context(token: Token[dict[str, Any]]) -> None:
    """Reset context to a previous token.

    Args:
        token: Token returned by ``set_context`` or ``bind_context``.

    Returns:
        None.

    Raises:
        ValueError: If the token belongs to a different context variable.

    Examples:
        >>> token = bind_context(x=1)
        >>> reset_context(token)
    """
    _context.reset(token)


def clear_context() -> None:
    """Clear context values.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> clear_context()
    """
    _context.set({})


__all__ = ["bind_context", "clear_context", "get_context", "reset_context", "set_context"]
