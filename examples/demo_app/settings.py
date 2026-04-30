"""Demo application settings."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DemoSettings:
    """Small demo settings object."""

    service_name: str = "demo-app"
    log_mode: str = "plain"
    log_level: str = "INFO"
