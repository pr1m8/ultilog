"""09 — Manual handler composition without setup().

Advanced users can compose ultilog handler factories and formatters directly.

Run:
    PYTHONPATH=src python examples/09_manual_handlers.py
"""

from __future__ import annotations

import logging

from ultilog.formatters.key_value import KeyValueFormatter
from ultilog.handlers.stream import create_stream_handler

handler = create_stream_handler()
handler.setFormatter(KeyValueFormatter())

logger = logging.getLogger("examples.manual")
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.info("manual.handler", extra={"component": "example"})
