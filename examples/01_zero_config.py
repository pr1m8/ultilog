"""01 — Zero-config: just import and log.

The first call to get_logger() lazily configures Rich console output.

Run:
    PYTHONPATH=src python examples/01_zero_config.py
"""

from __future__ import annotations

from ultilog import get_logger

log = get_logger()
log.debug("zero_config.debug")  # not visible at default INFO
log.info("zero_config.started")
log.warning("zero_config.warning")
log.error("zero_config.error")
