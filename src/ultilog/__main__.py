"""Command-line entry point for ``python -m ultilog``.

Purpose
-------
Provide a diagnostics and support CLI.

Design
------
The CLI intentionally uses ``argparse`` to avoid adding runtime dependencies.

Examples
--------
.. code-block:: bash

    python -m ultilog doctor
    python -m ultilog show-config
    python -m ultilog validate
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from ultilog import get_logger, setup
from ultilog.diagnostics import get_diagnostics, validate_config


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ultilog CLI.

    Args:
        argv: Optional argument vector for tests.

    Returns:
        Process exit code.

    Raises:
        None.

    Examples:
        >>> main(["doctor", "--json"])
        0
    """
    parser = argparse.ArgumentParser(prog="ultilog")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="print runtime diagnostics")
    doctor.add_argument("--json", action="store_true", help="emit JSON diagnostics")

    demo = subparsers.add_parser("demo", help="emit a demo log line")
    demo.add_argument("--mode", choices=["rich", "plain", "json"], default="plain")

    subparsers.add_parser("show-config", help="dump current effective settings")

    subparsers.add_parser("validate", help="validate configuration and environment")

    args = parser.parse_args(argv)

    if args.command == "doctor":
        return _cmd_doctor(args)

    if args.command == "demo":
        return _cmd_demo(args)

    if args.command == "show-config":
        return _cmd_show_config()

    if args.command == "validate":
        return _cmd_validate()

    return 2


def _cmd_doctor(args: argparse.Namespace) -> int:
    """Run the doctor subcommand.

    Args:
        args: Parsed CLI arguments.

    Returns:
        Exit code.

    Raises:
        None.
    """
    data = get_diagnostics()
    if args.json:
        print(json.dumps(data, sort_keys=True, default=str))
    else:
        for key, value in data.items():
            print(f"{key}: {value}")
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    """Run the demo subcommand.

    Args:
        args: Parsed CLI arguments.

    Returns:
        Exit code.

    Raises:
        None.
    """
    setup(mode=args.mode, force=True)
    log = get_logger("ultilog.demo", component="cli")
    log.info("cli.demo")
    return 0


def _cmd_show_config() -> int:
    """Dump effective settings as JSON.

    Args:
        None.

    Returns:
        Exit code.

    Raises:
        None.
    """
    from ultilog.config.export import export_settings
    from ultilog.settings import UltilogSettings

    settings = UltilogSettings()
    print(json.dumps(export_settings(settings), indent=2, sort_keys=True))
    return 0


def _cmd_validate() -> int:
    """Validate configuration and print warnings.

    Args:
        None.

    Returns:
        Exit code: 0 if valid, 1 if warnings found.

    Raises:
        None.
    """
    warnings = validate_config()
    if not warnings:
        print("Configuration is valid.")
        return 0

    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
