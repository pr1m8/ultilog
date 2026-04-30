"""Run the demo application."""

from __future__ import annotations

from ultilog import setup

from demo_app.services import process_order
from demo_app.settings import DemoSettings


def main() -> None:
    """Run the demo app."""
    settings = DemoSettings()
    setup(mode=settings.log_mode, level=settings.log_level, force=True)
    process_order("ord_123", user_id="usr_456")


if __name__ == "__main__":
    main()
