"""07 — Inspect runtime diagnostics.

Run:
    PYTHONPATH=src python examples/07_diagnostics.py
"""

from __future__ import annotations

from pprint import pprint

from ultilog import get_logger, setup_dev
from ultilog.diagnostics import get_diagnostics

setup_dev()
get_logger("examples.diagnostics").info("diagnostics.started")
pprint(get_diagnostics())
