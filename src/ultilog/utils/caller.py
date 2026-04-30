"""Caller inference helpers.

Purpose
-------
Infer a useful logger name when users call ``get_logger()`` without arguments.

Design
------
The helper walks the call stack and returns the first module outside the
``ultilog`` package.

Examples
--------
>>> isinstance(infer_caller_logger_name(), str)
True
"""

from __future__ import annotations

import inspect
from types import FrameType

from ultilog.constants import DEFAULT_LOGGER_NAME


def infer_caller_logger_name(*, package_prefix: str = "ultilog") -> str:
    """Infer the caller's module name.

    Args:
        package_prefix: Package prefix to skip while walking frames.

    Returns:
        Inferred module name, or a stable fallback name.

    Raises:
        None

    Examples:
        >>> infer_caller_logger_name(package_prefix="definitely_not_this_module")
        'ultilog.utils.caller'
    """
    frame: FrameType | None = inspect.currentframe()
    if frame is not None:
        frame = frame.f_back

    while frame is not None:
        module_name = frame.f_globals.get("__name__")
        if isinstance(module_name, str) and not module_name.startswith(package_prefix):
            return module_name
        frame = frame.f_back

    return DEFAULT_LOGGER_NAME


__all__ = ["infer_caller_logger_name"]
