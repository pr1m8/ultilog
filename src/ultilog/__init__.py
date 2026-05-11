"""Ergonomic logging for Python applications.

Purpose
-------
Expose the minimal public API for ``ultilog``.

Design
------
The public API starts small: ``get_logger()``, optional ``setup()``, explicit
``configure()``, and context helpers for request/job/task boundaries. Advanced
settings, handlers, and integrations live under submodules.

Examples
--------
>>> from ultilog import get_logger
>>> log = get_logger("example")
>>> log.name
'example'
"""

from ultilog.api import (
    UltilogSettings,
    bind_context,
    clear_context,
    configure,
    get_context,
    get_logger,
    logging_context,
    reset_logging,
    setup,
    setup_auto,
    setup_dev,
    setup_prod,
    setup_test,
)

__all__ = [
    "UltilogSettings",
    "bind_context",
    "clear_context",
    "configure",
    "get_context",
    "get_logger",
    "logging_context",
    "reset_logging",
    "setup",
    "setup_auto",
    "setup_dev",
    "setup_prod",
    "setup_test",
]
