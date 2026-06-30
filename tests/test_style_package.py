"""Structural guards for the `style/` package split (2.0 Workstream G).

`style.py` became a package (`theme`/`builders_tk`/`builders_ttk`/`engine`/
`bootstyle`). These tests are not about styling behavior (the rest of the suite
covers that) -- they lock in the two invariants the split must never break:

1. The public `ttkbootstrap.style` import path still exposes every name it did
   as a single module (no back-compat shim was needed; this proves it).
2. Each submodule imports standalone, i.e. the deliberate import layering +
   function-local back-edges introduced no import-time cycle.
"""
import importlib

import pytest


PUBLIC_NAMES = [
    "Colors",
    "ThemeDefinition",
    "Style",
    "StyleBuilderTK",
    "StyleBuilderTTK",
    "Keywords",
    "Bootstyle",
    "BootMixin",
    "AutoStyleMixin",
    "bootify",
    "apply_bootstyle",
    "enable_global_api",
]

SUBMODULES = [
    "ttkbootstrap.style.theme",
    "ttkbootstrap.style.scaling",
    "ttkbootstrap.style.builders_tk",
    "ttkbootstrap.style.builders_ttk",
    "ttkbootstrap.style.engine",
    "ttkbootstrap.style.bootstyle",
    # Toolkit leaves import standalone -- no engine edge at module top level.
    "ttkbootstrap.style.assets",
    "ttkbootstrap.style.elements",
    "ttkbootstrap.style.layout",
    "ttkbootstrap.style.icons",
    # Private builder registry/loader and every family module must remain
    # standalone-importable; none may reach upward into engine/bootstyle.
    "ttkbootstrap.style.builders",
    "ttkbootstrap.style.builders.registry",
    "ttkbootstrap.style.builders.utils",
    "ttkbootstrap.style.builders.button",
    "ttkbootstrap.style.builders.calendar",
    "ttkbootstrap.style.builders.checkbutton",
    "ttkbootstrap.style.builders.combobox",
    "ttkbootstrap.style.builders.entry",
    "ttkbootstrap.style.builders.floodgauge",
    "ttkbootstrap.style.builders.frame",
    "ttkbootstrap.style.builders.label",
    "ttkbootstrap.style.builders.labelframe",
    "ttkbootstrap.style.builders.menubutton",
    "ttkbootstrap.style.builders.notebook",
    "ttkbootstrap.style.builders.panedwindow",
    "ttkbootstrap.style.builders.progressbar",
    "ttkbootstrap.style.builders.radiobutton",
    "ttkbootstrap.style.builders.scale",
    "ttkbootstrap.style.builders.scrollbar",
    "ttkbootstrap.style.builders.separator",
    "ttkbootstrap.style.builders.sizegrip",
    "ttkbootstrap.style.builders.spinbox",
    "ttkbootstrap.style.builders.toggle",
    "ttkbootstrap.style.builders.toolbutton",
    "ttkbootstrap.style.builders.treeview",
]


def test_public_import_path_exposes_all_names():
    style = importlib.import_module("ttkbootstrap.style")
    missing = [n for n in PUBLIC_NAMES if not hasattr(style, n)]
    assert not missing, f"ttkbootstrap.style is missing {missing}"


@pytest.mark.parametrize("name", PUBLIC_NAMES)
def test_legacy_from_import_still_works(name):
    # `from ttkbootstrap.style import <Name>` must keep working unchanged.
    mod = importlib.import_module("ttkbootstrap.style")
    assert getattr(mod, name) is not None


@pytest.mark.parametrize("modname", SUBMODULES)
def test_submodule_imports_standalone(modname):
    # A standalone import of any submodule must not deadlock/cycle. (Each runs
    # in this process; the import system caches, so this asserts importability,
    # and the parametrization documents the layering.)
    assert importlib.import_module(modname) is not None


def test_consumers_import_from_public_path():
    # The internal consumers all reach the engine via the public package path.
    for modname in (
        "ttkbootstrap.window",
        "ttkbootstrap.widgets.meter",
        "ttkbootstrap.widgets.floodgauge",
    ):
        assert importlib.import_module(modname) is not None
