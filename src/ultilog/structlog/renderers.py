"""Structlog renderers for ``ultilog``.

Purpose
-------
Map ultilog mode names to structlog renderer names and provide renderer
factory helpers.

Design
------
Renderers are selected by mode name so ``configure_structlog`` can use the same
mode vocabulary as the rest of ultilog.
"""

from __future__ import annotations

from typing import Any, Literal


def get_renderer_name(json_logs: bool = False, *, mode: str | None = None) -> str:
    """Return the structlog renderer name for the given configuration.

    Args:
        json_logs: Legacy flag — ``True`` selects the JSON renderer.
        mode: ultilog mode name (``"json"``, ``"plain"``, ``"rich"``).
            Takes precedence over *json_logs* when provided.

    Returns:
        Renderer name: ``"json"``, ``"key_value"``, or ``"console"``.

    Raises:
        None.

    Examples:
        >>> get_renderer_name(mode="json")
        'json'
        >>> get_renderer_name(mode="plain")
        'key_value'
        >>> get_renderer_name(True)
        'json'
    """
    if mode is not None:
        if mode == "json":
            return "json"
        if mode == "plain":
            return "key_value"
        return "console"
    return "json" if json_logs else "console"


def get_renderer(name: Literal["json", "key_value", "console"] = "console") -> Any:
    """Return a structlog renderer instance.

    Args:
        name: Renderer name.

    Returns:
        A structlog renderer callable.

    Raises:
        RuntimeError: If structlog is not installed.
        ValueError: If the renderer name is unknown.

    Examples:
        >>> get_renderer("console")  # doctest: +SKIP
        ConsoleRenderer(...)
    """
    try:
        import structlog
    except ImportError as exc:
        raise RuntimeError("Install ultilog[structlog] for renderer support.") from exc

    if name == "json":
        return structlog.processors.JSONRenderer()
    if name == "key_value":
        return structlog.processors.KeyValueRenderer()
    if name == "console":
        return structlog.dev.ConsoleRenderer()
    msg = f"Unknown renderer: {name!r}"
    raise ValueError(msg)


__all__ = ["get_renderer", "get_renderer_name"]
