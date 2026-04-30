"""Show environment override shape.

Run with:
    ULTILOG_LOGGING__LEVEL=DEBUG PYTHONPATH=src python examples/04_environment_overrides.py
"""

from ultilog import get_logger

log = get_logger()
log.debug("debug.maybe_visible")
log.info("environment.example.complete")
