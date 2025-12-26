"""ttkb promote command - Upgrade project to packaging-ready."""

from __future__ import annotations

import argparse
from pathlib import Path

from ttkbootstrap.cli.config import (
    BUILD_CONFIG_TEMPLATE,
    TtkbConfig,
    find_config,
)
from ttkbootstrap.cli.pyinstaller import generate_spec


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'promote' subcommand parser."""
    parser = subparsers.add_parser(
        "promote",
        help="Upgrade project to packaging-ready",
        description="Add build configuration and generate build files for distribution.",
    )
    parser.add_argument(
        "--pyinstaller",
        action="store_true",
        help="Enable PyInstaller build support",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing build configuration",
    )
    parser.set_defaults(func=run_promote)


def run_promote(args: argparse.Namespace) -> None:
    """Execute the promote command."""
    if not args.pyinstaller:
        print("Error: Please specify a build backend.")
        print("  ttkb promote --pyinstaller")
        return

    # Find project root
    config_path = find_config()
    if config_path is None:
        print("Error: No ttkb.toml found in current directory or parents.")
        print("Run 'ttkb start <appname>' to create a new project first.")
        return

    project_root = config_path.parent
    config = TtkbConfig.load(config_path)

    # Check if already promoted
    if config.build is not None and not args.force:
        print("Project already has build configuration.")
        print("Use --force to overwrite.")
        return

    print(f"Promoting project '{config.app.name}' for PyInstaller...")

    # Update ttkb.toml with build section
    _add_build_section(config_path)

    # Create build directory
    build_dir = project_root / "build" / "pyinstaller"
    build_dir.mkdir(parents=True, exist_ok=True)

    # Reload config to get build settings
    config = TtkbConfig.load(config_path)

    # Generate .spec file
    spec_path = build_dir / "app.spec"
    generate_spec(config, project_root, spec_path)

    print()
    print("Project promoted successfully!")
    print()
    print("Generated files:")
    print(f"  - {spec_path.relative_to(project_root)}")
    print()
    print("Updated:")
    print(f"  - ttkb.toml (added [build] section)")
    print()
    print("Next steps:")
    print("  1. (Optional) Edit ttkb.toml [build] section")
    print("  2. Run 'ttkb build' to create executable")


def _add_build_section(config_path: Path) -> None:
    """Add [build] section to existing ttkb.toml."""
    content = config_path.read_text(encoding="utf-8")

    # Check if [build] section already exists
    if "[build]" in content:
        # Remove existing build section and everything after
        lines = content.split("\n")
        new_lines = []
        skip = False
        for line in lines:
            if line.strip().startswith("[build"):
                skip = True
            if not skip:
                new_lines.append(line)
        content = "\n".join(new_lines).rstrip() + "\n"

    # Append build section
    content += BUILD_CONFIG_TEMPLATE

    config_path.write_text(content, encoding="utf-8")
