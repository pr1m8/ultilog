"""Decorator helpers for future context support."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from ultilog.context.managers import logging_context

F = TypeVar("F", bound=Callable[..., Any])


def with_logging_context(**values: Any) -> Callable[[F], F]:
    """Decorate a function with temporary logging context.

    Args:
        **values: Context values.

    Returns:
        Decorator function.

    Raises:
        None

    Examples:
        >>> @with_logging_context(component="demo")
        ... def fn():
        ...     return 1
        >>> fn()
        1
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with logging_context(**values):
                return func(*args, **kwargs)
        return wrapper  # type: ignore[return-value]
    return decorator


__all__ = ["with_logging_context"]
