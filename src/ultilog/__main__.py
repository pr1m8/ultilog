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

    bootstrap = subparsers.add_parser("bootstrap", help="plan project logging bootstrap")
    bootstrap.add_argument("path", nargs="?", default=".", help="project path to inspect")
    bootstrap.add_argument("--json", action="store_true", help="emit JSON bootstrap plan")
    bootstrap.add_argument("--commands", action="store_true", help="print setup commands")
    bootstrap.add_argument("--snippet", action="store_true", help="print application setup snippet")
    bootstrap.add_argument(
        "--service-name",
        default="my-app",
        help="service name used by --snippet",
    )
    bootstrap.add_argument(
        "--apply",
        action="store_true",
        help="run missing package install commands for selected groups",
    )
    bootstrap.add_argument(
        "--group",
        action="append",
        default=[],
        help="install group to apply; may be repeated",
    )
    bootstrap.add_argument(
        "--all",
        action="store_true",
        help="apply every missing install group",
    )
    bootstrap.add_argument(
        "--check-environment",
        action="store_true",
        help="include a read-only pip check in JSON or commands output",
    )
    bootstrap.add_argument(
        "--no-env-check",
        action="store_true",
        help="skip the read-only environment dependency check",
    )
    bootstrap.add_argument(
        "--ignore-conflicts",
        action="store_true",
        help="apply even when the environment check reports dependency conflicts",
    )

    demo = subparsers.add_parser("demo", help="emit a demo log line")
    demo.add_argument("--mode", choices=["rich", "plain", "json"], default="plain")

    subparsers.add_parser("show-config", help="dump current effective settings")

    subparsers.add_parser("validate", help="validate configuration and environment")

    args = parser.parse_args(argv)

    if args.command == "doctor":
        return _cmd_doctor(args)

    if args.command == "bootstrap":
        return _cmd_bootstrap(args)

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


def _cmd_bootstrap(args: argparse.Namespace) -> int:
    """Run the bootstrap planner subcommand.

    Args:
        args: Parsed CLI arguments.

    Returns:
        Exit code.

    Raises:
        None.
    """
    from ultilog.project_bootstrap import (
        apply_project_bootstrap_plan,
        build_project_bootstrap_plan,
        setup_snippet,
    )

    should_check_environment = (
        not args.no_env_check
        and (
            args.check_environment
            or args.apply
            or not (args.json or args.commands or args.snippet)
        )
    )
    plan = build_project_bootstrap_plan(
        args.path,
        check_environment=should_check_environment,
    )
    data = plan.to_dict()
    if args.snippet:
        print(setup_snippet(service_name=args.service_name))
        return 0

    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return 0

    if args.commands:
        for command in plan.commands.values():
            print(command)
        if plan.environment_check is not None:
            print(plan.environment_check.command)
            for issue in plan.environment_check.issues:
                print(f"# Environment issue: {issue}")
            for command in plan.environment_check.repair_commands:
                print(f"# Suggested repair: {command}")
        print(plan.zero_code.requirements_command)
        print(plan.zero_code.run_command)
        print(f"# Optional after reviewing requirements: {plan.zero_code.install_command}")
        return 0

    if args.apply:
        if args.group and args.all:
            print("Use either --group or --all, not both.")
            return 2
        if not args.group and not args.all:
            print("Refusing to apply every group implicitly. Pass --group NAME or --all.")
            return 2
        if (
            plan.environment_check is not None
            and plan.environment_check.issues
            and not args.ignore_conflicts
        ):
            print("Environment dependency conflicts were detected before applying changes.")
            for issue in plan.environment_check.issues:
                print(f"- {issue}")
            if plan.environment_check.repair_commands:
                print("Suggested repair commands:")
                for command in plan.environment_check.repair_commands:
                    print(command)
            print("Fix the environment first, or pass --ignore-conflicts to continue anyway.")
            return 1

        selected_groups = None if args.all else set(args.group)
        results = apply_project_bootstrap_plan(plan, groups=selected_groups)
        if not results:
            print("No bootstrap install commands to run.")
            return 0
        for result in results:
            print(f"{result.group}: {result.command}")
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="")
        return 0

    _print_bootstrap_report(plan)
    return 0


def _print_bootstrap_report(plan: object) -> None:
    """Render a human-friendly project bootstrap report."""
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table

    from ultilog.project_bootstrap import ProjectBootstrapPlan

    resolved = plan
    if not isinstance(resolved, ProjectBootstrapPlan):  # pragma: no cover
        return

    console = Console()
    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="bold cyan")
    summary.add_column()
    summary.add_row("Project", resolved.root)
    summary.add_row("Package manager", resolved.package_manager)
    summary.add_row("pyproject", resolved.pyproject_path or "(not found)")
    summary.add_row("Detected deps", str(len(resolved.detected_dependencies)))
    console.print(Panel(summary, title="ultilog bootstrap", border_style="cyan"))

    if resolved.environment_check is not None:
        _print_environment_check(console, resolved.environment_check)

    groups = Table(
        "Group",
        "Target",
        "Packages",
        "Missing command",
        title="Install Groups",
        box=box.SIMPLE_HEAVY,
        expand=True,
    )
    for group in resolved.install_groups:
        missing = [status.package for status in group.packages if not status.declared]
        declared = len(group.packages) - len(missing)
        status = f"{declared}/{len(group.packages)} declared"
        packages = ", ".join(status.package for status in group.packages)
        groups.add_row(
            group.name,
            group.kind,
            f"{status}\n{packages}",
            group.command or "(already declared)",
        )
    console.print(groups)

    zero_code = Table(
        "Step",
        "Command",
        title="OpenTelemetry Zero-Code",
        box=box.SIMPLE,
        expand=True,
    )
    zero_code.add_row("Review generated requirements", resolved.zero_code.requirements_command)
    zero_code.add_row("Run app with instrumentation", resolved.zero_code.run_command)
    zero_code.add_row("Optional direct install after review", resolved.zero_code.install_command)
    console.print(zero_code)

    console.print(
        Panel(
            "Prefer grouped pyproject commands for repeatable installs. "
            "Use OpenTelemetry's direct install command only after reviewing "
            "the generated requirements for your active environment.",
            title="Zero-Code Install Safety",
            border_style="yellow",
        )
    )

    if resolved.commands:
        commands = "\n".join(resolved.commands.values())
        console.print(
            Panel(
                Syntax(commands, "bash", word_wrap=True),
                title="Setup Commands (raw: --commands)",
                border_style="green",
            )
        )
    else:
        console.print(Panel("All planned groups are already declared.", border_style="green"))

    console.print(
        Panel(
            "Generate app startup code with:\n"
            "python -m ultilog bootstrap --snippet --service-name my-api",
            title="Use In Your App",
            border_style="magenta",
        )
    )


def _print_environment_check(console: object, environment_check: object) -> None:
    """Render read-only environment health details."""
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    from ultilog.project_bootstrap import EnvironmentCheck

    if not isinstance(console, Console):  # pragma: no cover
        return
    if not isinstance(environment_check, EnvironmentCheck):  # pragma: no cover
        return

    if environment_check.error is not None:
        console.print(
            Panel(
                f"{environment_check.command}\n{environment_check.error}",
                title="Environment Check Unavailable",
                border_style="yellow",
            )
        )
        return

    if not environment_check.issues:
        console.print(
            Panel(
                environment_check.command,
                title="Environment Check Passed",
                border_style="green",
            )
        )
        return

    table = Table(
        "Issue",
        title="Environment Check",
        box=box.SIMPLE,
        expand=True,
    )
    for issue in environment_check.issues:
        table.add_row(issue)
    console.print(table)

    if environment_check.repair_commands:
        repairs = "\n".join(environment_check.repair_commands)
        console.print(
            Panel(
                repairs,
                title="Suggested Repair Commands",
                border_style="yellow",
            )
        )


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
