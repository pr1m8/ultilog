"""Explicit logger naming examples."""

from __future__ import annotations

from ultilog import get_logger, setup

setup(mode="plain", force=True)

get_logger().info("auto_name.used")
get_logger(__name__).info("module_name.used")
get_logger("custom.name").info("custom_name.used")
