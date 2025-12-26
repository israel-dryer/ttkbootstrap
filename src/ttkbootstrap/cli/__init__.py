"""CLI entry point for ttkbootstrap.

The ttkb CLI provides commands for:
- Creating new projects (start)
- Running applications (run)
- Building for distribution (build)
- Adding components (add)

Usage:
    ttkb start <appname>        Create a new project
    ttkb run [path]             Run the application
    ttkb promote --pyinstaller  Enable PyInstaller support
    ttkb build                  Build for distribution
    ttkb add view <ClassName>   Add a new view
    ttkb add dialog <ClassName> Add a new dialog
    ttkb add theme <name>       Add a custom theme
    ttkb add i18n               Add i18n support
    ttkb demo                   Launch the widget demo
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from ttkbootstrap.cli import add, build, promote, run, start
from ttkbootstrap.cli.demo import run_demo


def main(argv: Sequence[str] | None = None) -> None:
    """Dispatch CLI commands registered in ttkbootstrap."""
    parser = argparse.ArgumentParser(
        prog="ttkb",
        description="ttkbootstrap command line interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  ttkb start MyApp              Create a new project
  ttkb start MyApp --simple     Create minimal project
  ttkb run                      Run the application
  ttkb promote --pyinstaller    Enable PyInstaller support
  ttkb build                    Build for distribution
  ttkb add view SettingsView    Add a new view
  ttkb demo                     Launch the widget demo

For more information on a command:
  ttkb <command> --help
""",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=_get_version(),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        metavar="<command>",
    )

    # Register commands
    start.add_parser(subparsers)
    run.add_parser(subparsers)
    promote.add_parser(subparsers)
    build.add_parser(subparsers)
    add.add_parser(subparsers)

    # Demo command (kept for backwards compatibility)
    demo_parser = subparsers.add_parser(
        "demo",
        help="Launch the widget demo",
    )
    demo_parser.set_defaults(func=lambda args: run_demo())

    # Parse arguments
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)

    if func is None:
        parser.print_help()
        sys.exit(0)

    # Execute command
    try:
        func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def _get_version() -> str:
    """Get the ttkbootstrap version string."""
    try:
        import ttkbootstrap

        return f"ttkbootstrap {ttkbootstrap.__version__}"
    except Exception:
        return "ttkbootstrap (unknown version)"
