from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


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
    p.add_argument("-d", "--locales-dir", default=DEFAULT_LOCALES_DIR)
    p.add_argument("-D", "--domain", default=DEFAULT_DOMAIN)

    args = p.parse_args(argv)
    return compile_catalog(Path(args.locales_dir), args.domain)


if __name__ == "__main__":
    raise SystemExit(main())
