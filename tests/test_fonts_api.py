"""Headless tests for the 2.0 typography utility (Slice 4).

`ttkbootstrap.utils.fonts` is a tiny surface over the standard Tk named fonts:
the `Fonts` namespace (live-root helpers) plus the module-level
`set_global_family`, which rides the deferred-config seam (Slice 5) so it can be
called before `App()` exists.

The suite shares one session root, and named fonts are interpreter-global, so
every test that retints a font snapshots and restores it via the
`restore_fonts` fixture to avoid bleeding into other tests.
"""
import warnings
from tkinter import font

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.utils import config, fonts
from ttkbootstrap.utils.fonts import Fonts


@pytest.fixture
def restore_fonts(root):
    """Snapshot + restore the managed named fonts, the wrapper cache, and the
    pending-config registry so a test that pokes them does not leak."""
    before = {}
    for name in Fonts.names():
        try:
            before[name] = dict(font.nametofont(name, root=root).actual())
        except Exception:
            pass
    pending_before = dict(config._pending)
    try:
        yield root
    finally:
        for name, spec in before.items():
            try:
                font.nametofont(name, root=root).configure(**spec)
            except Exception:
                pass
        Fonts.reset()
        config._pending.clear()
        config._pending.update(pending_before)


# --------------------------------------------------------------------------
# exposure
# --------------------------------------------------------------------------

def test_surface_is_exported():
    assert ttk.set_global_family is fonts.set_global_family
    assert ttk.Fonts is Fonts
    assert "set_global_family" in ttk.__all__
    assert "Fonts" in ttk.__all__
    from ttkbootstrap import utils
    assert utils.set_global_family is fonts.set_global_family
    assert utils.Fonts is Fonts
    assert "set_global_family" in utils.__all__
    assert "Fonts" in utils.__all__


# --------------------------------------------------------------------------
# Fonts namespace (live root)
# --------------------------------------------------------------------------

def test_set_global_family_retints_proportional_fonts(restore_fonts):
    root = restore_fonts
    Fonts.set_global_family("Georgia")
    for name in fonts.PROPORTIONAL_FONTS:
        try:
            actual = font.nametofont(name, root=root).actual("family")
        except Exception:
            continue  # not on this platform
        assert actual == "Georgia", name


def test_set_global_family_leaves_fixed_font_unless_mono_given(restore_fonts):
    root = restore_fonts
    fixed_before = font.nametofont("TkFixedFont", root=root).actual("family")
    Fonts.set_global_family("Georgia")
    assert font.nametofont("TkFixedFont", root=root).actual("family") == fixed_before
    Fonts.set_global_family("Georgia", mono_family="Courier New")
    assert font.nametofont("TkFixedFont", root=root).actual("family") == "Courier New"


def test_configure_tweaks_a_single_named_font(restore_fonts):
    root = restore_fonts
    default_before = font.nametofont("TkDefaultFont", root=root).actual("size")
    Fonts.configure("TkHeadingFont", size=22)
    assert font.nametofont("TkHeadingFont", root=root).actual("size") == 22
    # a sibling proportional font is untouched -- configure targets one font
    assert font.nametofont("TkDefaultFont", root=root).actual("size") == default_before


def test_names_lists_the_managed_fonts():
    names = Fonts.names()
    assert "TkDefaultFont" in names
    assert "TkFixedFont" in names
    assert set(fonts.PROPORTIONAL_FONTS + fonts.MONOSPACE_FONTS) == set(names)


def test_describe_all_and_single(restore_fonts):
    all_specs = Fonts.describe()
    assert "TkDefaultFont" in all_specs
    assert "family" in all_specs["TkDefaultFont"]
    one = Fonts.describe("TkDefaultFont")
    assert one["family"] == all_specs["TkDefaultFont"]["family"]


def test_create_alias_registers_a_named_font(restore_fonts):
    root = restore_fonts
    alias = Fonts.create_alias("TtkbTestBody", family="Georgia", size=13)
    try:
        assert alias.actual("family") == "Georgia"
        # resolvable by name from a fresh lookup -> usable as font="TtkbTestBody"
        assert font.nametofont("TtkbTestBody", root=root).actual("size") == 13
        # re-registering the same name reconfigures rather than erroring
        again = Fonts.create_alias("TtkbTestBody", size=20)
        assert again.actual("size") == 20
        assert font.nametofont("TtkbTestBody", root=root).actual("size") == 20
    finally:
        try:
            root.tk.call("font", "delete", "TtkbTestBody")
        except Exception:
            pass


def test_reset_clears_the_wrapper_cache(restore_fonts):
    Fonts.describe()  # populates the cache
    assert fonts._font_cache
    Fonts.reset()
    assert not fonts._font_cache


# --------------------------------------------------------------------------
# module-level set_global_family -- the deferred-config seam
# --------------------------------------------------------------------------

def test_module_set_global_family_applies_live_when_root_exists(restore_fonts):
    root = restore_fonts
    # a root exists (session root), so the seam applies immediately, no queue
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ttk.set_global_family("Georgia")
    assert font.nametofont("TkDefaultFont", root=root).actual("family") == "Georgia"
    assert "global_family" not in config._pending


def test_module_set_global_family_queues_before_root(restore_fonts, monkeypatch):
    root = restore_fonts
    config._pending.clear()
    # simulate "no root yet" -> the setter queues silently instead of applying
    monkeypatch.setattr(Style, "instance", None)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ttk.set_global_family("Georgia", mono_family="Courier New")
    assert "global_family" in config._pending

    # root is back -> flush runs the queued applier
    monkeypatch.undo()
    config.flush_pending_config()
    assert font.nametofont("TkDefaultFont", root=root).actual("family") == "Georgia"
    assert font.nametofont("TkFixedFont", root=root).actual("family") == "Courier New"
    assert "global_family" not in config._pending
