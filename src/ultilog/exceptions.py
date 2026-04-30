"""Custom exceptions for ``ultilog``.

Purpose
-------
Define package-specific exceptions so callers can handle configuration and
optional-dependency failures precisely.

Design
------
Exceptions are intentionally lightweight. They add semantic meaning without
requiring complex inheritance.

Examples
--------
>>> issubclass(UltilogConfigurationError, UltilogError)
True
"""

from __future__ import annotations


class UltilogError(Exception):
    """Base exception for package errors.

    Args:
        *args: Exception arguments.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> raise UltilogError("demo")
        Traceback (most recent call last):
        ...
        ultilog.exceptions.UltilogError: demo
    """


class UltilogConfigurationError(UltilogError):
    """Raised when logging configuration fails.

    Args:
        *args: Exception arguments.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> issubclass(UltilogConfigurationError, UltilogError)
        True
    """


class UltilogOptionalDependencyError(UltilogError):
    """Raised when an optional integration dependency is missing.

    Args:
        *args: Exception arguments.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> issubclass(UltilogOptionalDependencyError, UltilogError)
        True
    """


class UltilogStateError(UltilogError):
    """Raised when runtime state cannot satisfy a requested operation.

    Args:
        *args: Exception arguments.

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> issubclass(UltilogStateError, UltilogError)
        True
    """


__all__ = [
    "UltilogConfigurationError",
    "UltilogError",
    "UltilogOptionalDependencyError",
    "UltilogStateError",
]
