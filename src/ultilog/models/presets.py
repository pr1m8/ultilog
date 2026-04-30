"""Preset models for ``ultilog``.

Purpose
-------
Define supported preset names.

Design
------
A literal type keeps the public preset surface small in Phase 1.

Examples
--------
>>> preset: PresetName = "dev"
>>> preset
'dev'
"""

from __future__ import annotations

from typing import Literal

PresetName = Literal["dev", "prod", "test"]

__all__ = ["PresetName"]
