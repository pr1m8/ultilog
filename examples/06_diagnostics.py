"""Diagnostics example."""

from __future__ import annotations

from pprint import pprint

from ultilog import get_logger
from ultilog.diagnostics import get_diagnostics

get_logger("examples.diagnostics").info("diagnostics.started")
pprint(get_diagnostics())
