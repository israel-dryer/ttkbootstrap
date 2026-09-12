"""Tests for the PyInstaller hook that bundles ttkbootstrap's package data.

The icon font and the element rasters are package *data*, which a freezer
collects only when a hook names it. A broken hook is invisible until someone
runs the frozen app, which then dies at its first icon render -- so these tests
pin every link PyInstaller follows, without needing PyInstaller installed.
"""
import ast
import importlib.metadata
from pathlib import Path

from ttkbootstrap._pyinstaller import get_hook_dirs

HOOK_GROUP = "pyinstaller40"
TARGET = "ttkbootstrap._pyinstaller:get_hook_dirs"


def _hook_path():
    return Path(get_hook_dirs()[0]) / "hook-ttkbootstrap.py"


def test_hook_dirs_name_the_directory_holding_the_hook():
    dirs = get_hook_dirs()
    assert len(dirs) == 1
    assert _hook_path().is_file()


def test_entry_point_is_installed_and_resolves():
    # Selected by value, not name: PyInstaller's own contrib package registers a
    # `hook-dirs` entry point in the same group.
    ours = [ep for ep in importlib.metadata.entry_points(group=HOOK_GROUP)
            if ep.value == TARGET]
    assert ours, "no pyinstaller40 entry point -- reinstall with `pip install -e .`"
    assert ours[0].load()() == get_hook_dirs()


def test_hook_assigns_the_collected_data_to_datas():
    # PyInstaller reads only the hook's `datas` global. Calling
    # collect_data_files without assigning it collects nothing, and a text
    # search for the call cannot tell the difference -- so parse the file.
    tree = ast.parse(_hook_path().read_text(encoding="utf-8-sig"))
    collected = [
        node.value.args[0].value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and [getattr(t, "id", None) for t in node.targets] == ["datas"]
        and isinstance(node.value, ast.Call)
        and getattr(node.value.func, "id", None) == "collect_data_files"
        and node.value.args
    ]
    assert collected == ["ttkbootstrap.assets"]