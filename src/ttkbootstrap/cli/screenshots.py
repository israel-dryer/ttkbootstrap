"""ttkb screenshots command — render docs screenshots from the manifest.

Contributor-only: the renderer reads `docs_scripts/screenshots.toml` from
the ttkbootstrap source checkout. When invoked outside that checkout the
manifest is unavailable, so this command is a no-op for end users.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "screenshots",
        help="Render docs screenshots from the manifest (contributor-only)",
        description=(
            "Render documentation screenshots driven by "
            "`docs_scripts/screenshots.toml`. Only useful inside a "
            "ttkbootstrap source checkout."
        ),
    )
    parser.add_argument("--slug", help="Render only the shot with this slug.")
    parser.add_argument(
        "--page",
        help="Render only shots for this docs page (e.g. widgets/actions/button.md).",
    )
    parser.add_argument(
        "--theme",
        action="append",
        choices=["light", "dark"],
        help="Render only this theme variant (may be repeated).",
    )
    parser.set_defaults(func=run_screenshots)


def _find_repo_root() -> Path | None:
    """Walk up from the cwd until we find docs_scripts/screenshots.toml."""
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / "docs_scripts" / "screenshots.toml").is_file():
            return candidate
    return None


def run_screenshots(args: argparse.Namespace) -> None:
    repo_root = _find_repo_root()
    if repo_root is None:
        print(
            "ttkb screenshots: docs_scripts/screenshots.toml not found.\n"
            "This command renders documentation assets and only works "
            "from a ttkbootstrap source checkout.",
            file=sys.stderr,
        )
        sys.exit(1)
    cmd = [sys.executable, "-m", "docs_scripts.render"]
    if args.slug:
        cmd += ["--slug", args.slug]
    if args.page:
        cmd += ["--page", args.page]
    for t in args.theme or []:
        cmd += ["--theme", t]
    sys.exit(subprocess.call(cmd, cwd=repo_root))
