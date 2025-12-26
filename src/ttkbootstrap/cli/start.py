"""ttkb start command - Create a new ttkbootstrap project."""

from __future__ import annotations

import argparse
from pathlib import Path

from ttkbootstrap.cli.templates import create_project


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'start' subcommand parser."""
    parser = subparsers.add_parser(
        "start",
        help="Create a new ttkbootstrap project",
        description="Scaffold a new ttkbootstrap application with sensible defaults.",
    )
    parser.add_argument(
        "name",
        help="Application name (e.g., 'MyApp')",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Create minimal project without assets or build configuration",
    )
    parser.add_argument(
        "--container",
        choices=["grid", "pack"],
        default="grid",
        help="Default container type for views (default: grid)",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="Target directory (default: ./<appname>)",
    )
    parser.set_defaults(func=run_start)


def run_start(args: argparse.Namespace) -> None:
    """Execute the start command."""
    name = args.name
    simple = args.simple
    container = args.container

    # Determine target directory
    if args.dir:
        target_dir = args.dir
    else:
        # Use lowercase name with underscores for directory
        dir_name = name.lower().replace(" ", "_").replace("-", "_")
        target_dir = Path.cwd() / dir_name

    # Check if directory already exists and has content
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"Error: Directory '{target_dir}' already exists and is not empty.")
        print("Choose a different name or remove the existing directory.")
        return

    # Create the project
    print(f"Creating project '{name}' in {target_dir}...")
    create_project(
        name=name,
        target_dir=target_dir,
        container=container,
        simple=simple,
    )

    # Print success message
    print()
    print(f"Project '{name}' created successfully!")
    print()
    print("Next steps:")
    print(f"  cd {target_dir.name}")
    print("  ttkb run")
    print()
    if not simple:
        print("To build for distribution:")
        print("  ttkb promote --pyinstaller")
        print("  ttkb build")
