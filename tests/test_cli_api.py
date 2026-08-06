"""Tests for `ttkbootstrap.__version__`."""
import importlib.metadata
import subprocess
import sys
from pathlib import Path

import ttkbootstrap as ttk

REPO = Path(__file__).parent.parent


def test_version_is_the_installed_distribution_version():
    # Read from the installed metadata rather than written into the source, so
    # pyproject.toml stays the one place the literal lives. The consequence is
    # that this reports what was *installed* -- an editable install keeps the
    # metadata it was built with -- so it is NOT asserted against pyproject.
    assert isinstance(ttk.__version__, str) and ttk.__version__
    assert ttk.__version__ == importlib.metadata.version("ttkbootstrap")


def test_version_is_declared_in_the_type_stub():
    # A .pyi replaces the module for type checkers, and the stub's re-export
    # pass sources every name from an import statement in __init__.py --
    # __version__ is an assignment, so it has to be declared explicitly or
    # `ttk.__version__` is an attribute error under mypy/pyright (verified).
    stub = (REPO / "src" / "ttkbootstrap" / "__init__.pyi").read_text(
        encoding="utf-8")
    assert "__version__: str" in stub


def test_version_survives_missing_metadata():
    # Running from a source tree that was never installed (PYTHONPATH=src) has
    # no metadata to read; the import must still work. In a subprocess because
    # ttkbootstrap is already imported here -- and the patch has to land before
    # the import, since `from importlib.metadata import version` binds then.
    code = (
        "import importlib.metadata as m\n"
        "def missing(name): raise m.PackageNotFoundError(name)\n"
        "m.version = missing\n"
        "import ttkbootstrap\n"
        "print(ttkbootstrap.__version__)\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "unknown"
