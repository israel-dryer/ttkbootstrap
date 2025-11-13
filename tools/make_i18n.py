from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_CONFIG = "babel.cfg"
DEFAULT_DOMAIN = "ttkbootstrap"
# Compile catalogs directly into the package assets so wheels include them.
DEFAULT_LOCALES_DIR = "src/ttkbootstrap/assets/locales"


def which_babel() -> list[str] | None:
    """Return a command list to invoke Babel, preferring `pybabel`.
    Falls back to python -m if the CLI is not on PATH.
    """
    if shutil.which("pybabel"):
        return ["pybabel"]
    # Fallbacks for environments without the console script
    py = shutil.which("python") or shutil.which("py")
    if py:
        return [py, "-m", "babel.messages.frontend"]
    return None


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    proc = subprocess.run(cmd)
    return proc.returncode


def extract(config: Path, locales_dir: Path, domain: str) -> int:
    locales_dir.mkdir(parents=True, exist_ok=True)
    pot = locales_dir / f"{domain}.pot"
    babel = which_babel()
    if not babel:
        print("Error: Babel not found. Install with `pip install Babel`.", file=sys.stderr)
        return 1
    cmd = babel + [
        "extract",
        "-F", str(config),
        "-o", str(pot),
        ".",
    ]
    return run(cmd)


def init_locales(locales: list[str], locales_dir: Path, domain: str) -> int:
    pot = locales_dir / f"{domain}.pot"
    if not pot.exists():
        print(f"Error: template not found: {pot}. Run `extract` first.", file=sys.stderr)
        return 1
    babel = which_babel()
    if not babel:
        print("Error: Babel not found. Install with `pip install Babel`.", file=sys.stderr)
        return 1
    rc = 0
    for lang in locales:
        cmd = babel + [
            "init",
            "-i", str(pot),
            "-d", str(locales_dir),
            "-D", domain,
            "-l", lang,
        ]
        rc |= run(cmd)
    return rc


def update_catalog(locales_dir: Path, domain: str) -> int:
    pot = locales_dir / f"{domain}.pot"
    if not pot.exists():
        print(f"Error: template not found: {pot}. Run `extract` first.", file=sys.stderr)
        return 1
    babel = which_babel()
    if not babel:
        print("Error: Babel not found. Install with `pip install Babel`.", file=sys.stderr)
        return 1
    cmd = babel + [
        "update",
        "-i", str(pot),
        "-d", str(locales_dir),
        "-D", domain,
    ]
    return run(cmd)


def compile_catalog(locales_dir: Path, domain: str) -> int:
    babel = which_babel()
    if not babel:
        print("Error: Babel not found. Install with `pip install Babel`.", file=sys.stderr)
        return 1
    cmd = babel + [
        "compile",
        "-d", str(locales_dir),
        "-D", domain,
    ]
    return run(cmd)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Babel i18n helper for ttkbootstrap")
    sub = p.add_subparsers(dest="cmd", required=True)

    # extract
    p_ext = sub.add_parser("extract", help="Extract messages to POT")
    p_ext.add_argument("-F", "--config", default=DEFAULT_CONFIG)
    p_ext.add_argument("-d", "--locales-dir", default=DEFAULT_LOCALES_DIR)
    p_ext.add_argument("-D", "--domain", default=DEFAULT_DOMAIN)

    # init
    p_init = sub.add_parser("init", help="Initialize locales from POT")
    p_init.add_argument("-d", "--locales-dir", default=DEFAULT_LOCALES_DIR)
    p_init.add_argument("-D", "--domain", default=DEFAULT_DOMAIN)
    p_init.add_argument("-l", "--locales", nargs="+", required=True, help="e.g. de fr zh_CN")

    # update
    p_upd = sub.add_parser("update", help="Update existing catalogs from POT")
    p_upd.add_argument("-d", "--locales-dir", default=DEFAULT_LOCALES_DIR)
    p_upd.add_argument("-D", "--domain", default=DEFAULT_DOMAIN)

    # compile
    p_cmp = sub.add_parser("compile", help="Compile catalogs to .mo")
    p_cmp.add_argument("-d", "--locales-dir", default=DEFAULT_LOCALES_DIR)
    p_cmp.add_argument("-D", "--domain", default=DEFAULT_DOMAIN)

    args = p.parse_args(argv)
    if args.cmd == "extract":
        return extract(Path(args.config), Path(args.locales_dir), args.domain)
    if args.cmd == "init":
        return init_locales(args.locales, Path(args.locales_dir), args.domain)
    if args.cmd == "update":
        return update_catalog(Path(args.locales_dir), args.domain)
    if args.cmd == "compile":
        return compile_catalog(Path(args.locales_dir), args.domain)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
