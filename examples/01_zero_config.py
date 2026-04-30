"""Zero-config usage example."""

from __future__ import annotations

from ultilog import get_logger

log = get_logger()
log.info("zero_config.started")
log.warning("zero_config.warning")
