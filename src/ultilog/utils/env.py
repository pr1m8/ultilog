"""Environment helpers for ``ultilog``.

Purpose
-------
Keep environment variable discovery and documentation-related helpers in one
small module.

Design
------
The helpers do not mutate the environment. Tests and callers can use the return
values to explain or validate configuration.

Examples
--------
>>> is_ultilog_env_key("ULTILOG_LOGGING__LEVEL")
True
"""

from __future__ import annotations

import os
from collections.abc import Mapping

from ultilog.constants import ENV_PREFIX


def is_ultilog_env_key(key: str) -> bool:
    """Return whether an environment key belongs to ``ultilog``.

    Args:
        key: Environment variable name.

    Returns:
        ``True`` if the key starts with the package prefix.

    Raises:
        None.

    Examples:
        >>> is_ultilog_env_key("PATH")
        False
    """
    return key.startswith(ENV_PREFIX)


def collect_ultilog_env(environ: Mapping[str, str] | None = None) -> dict[str, str]:
    """Collect active ``ultilog`` environment variables.

    Args:
        environ: Optional environment mapping. Defaults to ``os.environ``.

    Returns:
        Dictionary of matching environment variables.

    Raises:
        None.

    Examples:
        >>> collect_ultilog_env({"ULTILOG_PRESET": "test", "X": "1"})
        {'ULTILOG_PRESET': 'test'}
    """
    source = os.environ if environ is None else environ
    return {key: value for key, value in source.items() if is_ultilog_env_key(key)}


def describe_env_prefix() -> str:
    """Return the environment prefix documentation string.

    Args:
        None.

    Returns:
        Prefix description.

    Raises:
        None.

    Examples:
        >>> describe_env_prefix().startswith("ULTILOG_")
        True
    """
    return f"{ENV_PREFIX} variables configure ultilog; nested settings use double underscores."


__all__ = ["collect_ultilog_env", "describe_env_prefix", "is_ultilog_env_key"]
