"""CLI entry point for ttkbootstrap."""

from __future__ import annotations

import argparse
from typing import Sequence

from ttkbootstrap.cli.demo import run_demo


def main(argv: Sequence[str] | None = None) -> None:
    """Dispatch CLI commands registered in ttkbootstrap."""
    parser = argparse.ArgumentParser(prog="ttkb", description="ttkbootstrap command line helper")
    subparsers = parser.add_subparsers(dest="command")

    demo_parser = subparsers.add_parser("demo", help="Launch the widget demo")
    demo_parser.set_defaults(func=run_demo)

    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return

    func()
