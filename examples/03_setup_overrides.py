"""Setup override examples."""

from __future__ import annotations

from ultilog import get_logger, setup

setup(mode="plain", level="DEBUG", force=True)
log = get_logger("examples.setup")
log.debug("debug.enabled")
log.info("setup_overrides.started")
