"""ttkb build command - Build the application for distribution."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from ttkbootstrap.cli.config import TtkbConfig, find_config


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'build' subcommand parser."""
    parser = subparsers.add_parser(
        "build",
        help="Build the application for distribution",
        description="Build the application using the configured build backend.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build artifacts before building",
    )
    parser.set_defaults(func=run_build)


def run_build(args: argparse.Namespace) -> None:
    """Execute the build command."""
    # Find project root
    config_path = find_config()
    if config_path is None:
        print("Error: No ttkb.toml found in current directory or parents.")
        print("Run 'ttkb start <appname>' to create a new project first.")
        return

    project_root = config_path.parent
    config = TtkbConfig.load(config_path)

    # Check if project has been promoted
    if config.build is None:
        print("Error: Project has not been promoted for building.")
        print("Run 'ttkb promote --pyinstaller' first.")
        return

    backend = config.build.backend

    if backend == "pyinstaller":
        _build_pyinstaller(config, project_root, clean=args.clean)
    else:
        print(f"Error: Unknown build backend '{backend}'")
        return


def _build_pyinstaller(
    config: TtkbConfig,
    project_root: Path,
    clean: bool = False,
) -> None:
    """Build using PyInstaller."""
    # Check if PyInstaller is installed
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("Error: PyInstaller is not installed.")
        print("Install it with: pip install pyinstaller")
        return

    spec_path = project_root / "build" / "pyinstaller" / "app.spec"
    if not spec_path.exists():
        print("Error: PyInstaller spec file not found.")
        print("Run 'ttkb promote --pyinstaller' to generate it.")
        return

    # Clean if requested
    if clean:
        print("Cleaning build artifacts...")
        dist_dir = project_root / "dist"
        build_dir = project_root / "build" / "pyinstaller" / "build"
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        if build_dir.exists():
            shutil.rmtree(build_dir)

    print(f"Building '{config.app.name}' with PyInstaller...")
    print()

    # Run PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(spec_path),
        "--distpath",
        str(project_root / "dist"),
        "--workpath",
        str(project_root / "build" / "pyinstaller" / "build"),
        "--noconfirm",
    ]

    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        if result.returncode == 0:
            print()
            print("Build completed successfully!")
            print()
            print(f"Output: {project_root / 'dist' / config.app.name}")
        else:
            print()
            print("Build failed.")
            sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nBuild interrupted.")
        sys.exit(1)
