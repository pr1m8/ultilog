"""Tests for optional import helpers."""

from __future__ import annotations

import pytest

from ultilog.exceptions import UltilogOptionalDependencyError
from ultilog.utils.import_tools import is_module_available, require_module


def test_is_module_available_for_stdlib() -> None:
    assert is_module_available("logging")


def test_require_module_raises_for_missing_module() -> None:
    with pytest.raises(UltilogOptionalDependencyError):
        require_module("not_a_real_ultilog_optional_dependency", extra="demo")
