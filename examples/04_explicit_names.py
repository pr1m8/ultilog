"""04 — Logger naming: inferred, module, and custom.

Run:
    PYTHONPATH=src python examples/04_explicit_names.py
"""

from __future__ import annotations

from ultilog import get_logger, setup_dev

setup_dev(level="INFO")

get_logger().info("auto_name.used")              # caller module inferred
get_logger(__name__).info("module_name.used")    # explicit module
get_logger("custom.name").info("custom_name.used")  # custom string
