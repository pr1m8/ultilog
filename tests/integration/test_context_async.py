"""Tests for async context isolation."""

from __future__ import annotations

import asyncio

import pytest

from ultilog.context.managers import logging_context
from ultilog.context.vars import get_context


@pytest.mark.anyio
async def test_async_context_isolation() -> None:
    results: dict[str, dict] = {}

    async def task_a() -> None:
        with logging_context(task="a"):
            await asyncio.sleep(0.01)
            results["a"] = dict(get_context())

    async def task_b() -> None:
        with logging_context(task="b"):
            await asyncio.sleep(0.01)
            results["b"] = dict(get_context())

    await asyncio.gather(task_a(), task_b())
    assert results["a"]["task"] == "a"
    assert results["b"]["task"] == "b"


@pytest.mark.anyio
async def test_async_nested_context() -> None:
    with logging_context(outer="1"):
        assert get_context()["outer"] == "1"
        with logging_context(inner="2"):
            ctx = get_context()
            assert ctx["outer"] == "1"
            assert ctx["inner"] == "2"
        assert "inner" not in get_context()
