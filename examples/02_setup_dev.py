"""02 — Super-pretty dev setup with Rich tracebacks + locals.

setup_dev() turns on every visual feature: colors, file paths, time stamps,
and tracebacks that show local variables when something blows up.

Run:
    PYTHONPATH=src python examples/02_setup_dev.py
"""

from __future__ import annotations

from ultilog import get_logger, setup_dev

setup_dev()
log = get_logger("examples.dev")

log.debug("dev.debug.visible")
log.info("dev.info")
log.warning("dev.warning")
log.error("dev.error")

# Trigger a Rich traceback with local variables shown.
try:
    user = {"id": 42, "name": "alice"}
    raise ValueError("demo error")
except ValueError:
    log.exception("dev.traceback")
