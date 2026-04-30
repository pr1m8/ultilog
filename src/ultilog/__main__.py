"""Command-line entry point for ``python -m ultilog``.

Purpose
-------
Provide a tiny diagnostics CLI for the scaffold.

Design
------
The CLI intentionally uses ``argparse`` to avoid adding runtime dependencies.

Examples
--------
.. code-block:: bash

    python -m ultilog doctor
"""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from ultilog import get_logger, setup
from ultilog.diagnostics import get_diagnostics


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

    args = parser.parse_args(argv)
    if args.command == "doctor":
        data = get_diagnostics()
        if args.json:
            print(json.dumps(data, sort_keys=True))
        else:
            for key, value in data.items():
                print(f"{key}: {value}")
        return 0

    if args.command == "demo":
        setup(mode=args.mode, force=True)
        log = get_logger("ultilog.demo", component="cli")
        log.info("cli.demo")
        return 0

    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
