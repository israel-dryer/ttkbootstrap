"""Tests for `ttkbootstrap.__version__` and the `ttkb` command line.

The CLI is a thin dispatcher: what is worth pinning is that every subcommand is
reachable, that `convert-theme` behaves identically to its `python -m` spelling,
and that a failing command names itself rather than the bare `ttkb`.
"""
import importlib.metadata
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

import ttkbootstrap as ttk
from ttkbootstrap import cli, convert_theme

REPO = Path(__file__).parent.parent

LEGACY_THEME = {
    "acme": {
        "type": "light",
        "colors": {
            "primary": "#6a5acd", "secondary": "#6c757d", "success": "#02b875",
            "info": "#17a2b8", "warning": "#f0ad4e", "danger": "#d9534f",
            "light": "#ADB5BD", "dark": "#2b2b2b",
            "bg": "#ffffff", "fg": "#212529",
            "selectbg": "#555555", "selectfg": "#ffffff", "border": "#ced4da",
            "inputfg": "#212529", "inputbg": "#ffffff", "active": "#e5e5e5",
        },
    }
}


@pytest.fixture
def legacy_file(tmp_path):
    """A 1.x ``user.py`` store to convert."""
    path = tmp_path / "user.py"
    path.write_text(
        "USER_THEMES = " + json.dumps(LEGACY_THEME, indent=4), encoding="utf-8"
    )
    return path


# --------------------------------------------------------------------------
# __version__
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------

def test_pyproject_installs_both_console_scripts():
    data = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = data["project"]["scripts"]
    assert scripts == {
        "ttkbootstrap": "ttkbootstrap.cli:main",
        "ttkb": "ttkbootstrap.cli:main",
    }


def test_every_subcommand_is_reachable():
    parser = cli.build_parser()
    choices = parser._subparsers._group_actions[0].choices
    assert set(choices) == {"version", "demo", "convert-theme", "creator"}
    for name, subparser in choices.items():
        args = subparser.parse_args([] if name != "convert-theme" else ["f.py"])
        assert callable(args.func)
        assert args.parser is subparser  # so errors name the subcommand


# --------------------------------------------------------------------------
# dispatch
# --------------------------------------------------------------------------

def test_version_command_prints_the_version(capsys):
    assert cli.main(["version"]) == 0
    assert capsys.readouterr().out.strip() == ttk.__version__


def test_bare_ttkb_prints_help_and_fails(capsys):
    # argparse can require a subcommand, but its error names the missing
    # argument rather than showing what is available -- and a bare `ttkb` is
    # someone asking exactly that.
    assert cli.main([]) == 2
    out = capsys.readouterr().out
    for command in ("version", "demo", "convert-theme", "creator"):
        assert command in out


@pytest.mark.parametrize("command, module, attribute", [
    ("demo", "ttkbootstrap.__main__", "main"),
    ("creator", "ttkcreator.__main__", "main"),
])
def test_gui_commands_call_their_entry_point(command, module, attribute,
                                             monkeypatch):
    # The launchers open a window and block, so the dispatch is what is tested;
    # that the target exists at all is the half that silently rots.
    import importlib

    target = importlib.import_module(module)
    calls = []
    monkeypatch.setattr(target, attribute, lambda: calls.append(command) or 0)
    assert cli.main([command]) == 0
    assert calls == [command]


# --------------------------------------------------------------------------
# convert-theme, through the CLI
# --------------------------------------------------------------------------

def test_convert_theme_matches_the_module_spelling(legacy_file, capsys):
    assert cli.main(["convert-theme", str(legacy_file)]) == 0
    through_cli = capsys.readouterr().out
    assert convert_theme.main([str(legacy_file)]) == 0
    assert capsys.readouterr().out == through_cli
    assert 'ttk.Theme(' in through_cli


def test_convert_theme_writes_the_output_file(legacy_file, tmp_path, capsys):
    out = tmp_path / "brand.py"
    assert cli.main(["convert-theme", str(legacy_file), "-o", str(out)]) == 0
    assert "ttk.Theme(" in out.read_text(encoding="utf-8")
    assert f"Wrote {out}" in capsys.readouterr().err


def test_convert_theme_failure_names_the_subcommand(tmp_path, capsys):
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["convert-theme", str(tmp_path / "missing.py")])
    assert exit_info.value.code == 2
    assert capsys.readouterr().err.startswith("ttkb convert-theme:")
