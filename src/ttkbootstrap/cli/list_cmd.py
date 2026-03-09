"""ttkb list command - List available themes and other resources."""

from __future__ import annotations

import argparse
import json


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'list' subcommand parser."""
    parser = subparsers.add_parser(
        "list",
        help="List available resources",
        description="List themes and other available resources.",
    )
    list_subparsers = parser.add_subparsers(dest="resource")

    # ttkb list themes
    themes_parser = list_subparsers.add_parser(
        "themes",
        help="List available themes",
    )
    themes_parser.set_defaults(func=run_list_themes)

    parser.set_defaults(func=lambda args: parser.print_help())


def run_list_themes(args: argparse.Namespace) -> None:
    """List available themes by reading theme JSON files from the package."""
    from importlib import resources

    themes: list[dict[str, str]] = []

    for package in ("ttkbootstrap.assets.themes", "ttkbootstrap.assets.themes.legacy"):
        try:
            base = resources.files(package)
        except (ModuleNotFoundError, FileNotFoundError):
            continue
        for item in base.iterdir():
            if not item.name.endswith(".json"):
                continue
            try:
                data = json.loads(item.read_text(encoding="utf-8"))
                themes.append({
                    "name": data.get("name", item.name.removesuffix(".json")),
                    "display_name": data.get("display_name", ""),
                    "mode": data.get("mode", ""),
                })
            except (json.JSONDecodeError, OSError):
                continue

    if not themes:
        print("No themes found.")
        return

    themes.sort(key=lambda t: (t["mode"], t["name"]))

    # Print table
    name_width = max(len(t["name"]) for t in themes)
    display_width = max(len(t["display_name"]) for t in themes)

    header = f"  {'Name':<{name_width}}  {'Display Name':<{display_width}}  Mode"
    print(header)
    print(f"  {'-' * name_width}  {'-' * display_width}  ----")

    for t in themes:
        print(f"  {t['name']:<{name_width}}  {t['display_name']:<{display_width}}  {t['mode']}")

    print(f"\n  {len(themes)} themes available.")
