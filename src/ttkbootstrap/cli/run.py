"""ttkb run command - Run a ttkbootstrap application."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from ttkbootstrap.cli.config import TtkbConfig, find_config


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'run' subcommand parser."""
    parser = subparsers.add_parser(
        "run",
        help="Run the ttkbootstrap application",
        description="Run the application using the entry point defined in ttkb.toml.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Path to entry point or directory containing ttkb.toml (default: current directory)",
    )
    parser.set_defaults(func=run_run)


def run_run(args: argparse.Namespace) -> None:
    """Execute the run command."""
    path = args.path

    # Determine what to run
    if path:
        path = Path(path)
        if path.is_file() and path.suffix == ".py":
            # Direct path to a Python file
            entry_point = path
            project_root = path.parent
        elif path.is_dir():
            # Directory - look for ttkb.toml
            config_path = path / "ttkb.toml"
            if not config_path.exists():
                print(f"Error: No ttkb.toml found in '{path}'")
                return
            config = TtkbConfig.load(config_path)
            entry_point = path / config.app.entry
            project_root = path
        else:
            print(f"Error: '{path}' is not a valid file or directory")
            return
    else:
        # No path specified - find ttkb.toml
        config_path = find_config()
        if config_path is None:
            print("Error: No ttkb.toml found in current directory or parents.")
            print("Run 'ttkb start <appname>' to create a new project.")
            return

        config = TtkbConfig.load(config_path)
        project_root = config_path.parent
        entry_point = project_root / config.app.entry

    # Verify entry point exists
    if not entry_point.exists():
        print(f"Error: Entry point '{entry_point}' does not exist.")
        return

    print(f"Running {entry_point.relative_to(project_root)}...")
    print()

    # Run the application
    # Add project src directory to PYTHONPATH
    src_dir = project_root / "src"
    env = dict(__import__("os").environ)
    python_path = env.get("PYTHONPATH", "")
    if src_dir.exists():
        if python_path:
            env["PYTHONPATH"] = f"{src_dir}{__import__('os').pathsep}{python_path}"
        else:
            env["PYTHONPATH"] = str(src_dir)

    try:
        result = subprocess.run(
            [sys.executable, str(entry_point)],
            cwd=str(project_root),
            env=env,
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
