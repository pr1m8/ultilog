"""Tests for Rich handler factory."""

from __future__ import annotations

from rich.logging import RichHandler

from ultilog.handlers.rich import create_rich_handler
from ultilog.models.rich import RichSettings


def test_create_rich_handler_returns_handler() -> None:
    handler = create_rich_handler()
    assert isinstance(handler, RichHandler)


def test_create_rich_handler_applies_settings() -> None:
    handler = create_rich_handler(settings=RichSettings(show_path=False))
    assert handler._log_render.show_path is False  # noqa: SLF001
