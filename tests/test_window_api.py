"""Headless tests for the 2.0 Window/Toplevel API normalization (PR B).

Covers the parts that are checkable without a real display:
- deprecated raw-Tk kwarg spellings normalize to snake_case (with a warning),
- the combined/edge-relative geometry string construction,
- the positioning math (center + clamp),
- the unified icon/`iconphoto` semantics (including the old `Toplevel`
  `iconphoto=None` crash),
- the consistent `style` property and the aqua `overrideredirect` guard.
"""
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.internal import positioning
from ttkbootstrap.style import Style
from ttkbootstrap.style._compat import normalize_window_kwargs
from ttkbootstrap.window import Toplevel, Window, _BaseWindow


# --------------------------------------------------------------------------
# kwarg normalization
# --------------------------------------------------------------------------

def test_normalize_window_kwargs_maps_and_warns():
    kwargs = {"hdpi": False, "overrideredirect": True, "master": "x"}
    with pytest.warns(DeprecationWarning):
        out = normalize_window_kwargs(kwargs)
    assert out == {"high_dpi": False, "override_redirect": True}
    # only the legacy names are consumed; unrelated kwargs are left in place
    assert kwargs == {"master": "x"}


def test_normalize_window_kwargs_noop_when_absent():
    kwargs = {"background": "red"}
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        out = normalize_window_kwargs(kwargs)
    assert out == {}
    assert kwargs == {"background": "red"}


def test_toplevel_accepts_legacy_windowtype_with_warning(root):
    with pytest.warns(DeprecationWarning):
        top = ttk.Toplevel(title="legacy", windowtype="dialog")
    top.destroy()


def test_toplevel_new_names_are_warning_free(root):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        top = ttk.Toplevel(title="modern", window_type="dialog", iconify=True)
    top.destroy()


# --------------------------------------------------------------------------
# geometry string construction
# --------------------------------------------------------------------------

class _GeoRecorder(_BaseWindow):
    """Minimal stand-in that records geometry strings without a real window."""

    def __init__(self):
        self.calls = []

    def geometry(self, value=None):
        self.calls.append(value)


def test_apply_geometry_size_and_position_combined():
    rec = _GeoRecorder()
    rec._apply_geometry((800, 600), (100, 120))
    assert rec.calls == ["800x600+100+120"]


def test_apply_geometry_negative_position_is_edge_relative():
    rec = _GeoRecorder()
    rec._apply_geometry(None, (-10, -20))
    assert rec.calls == ["-10-20"]


def test_apply_geometry_size_only():
    rec = _GeoRecorder()
    rec._apply_geometry((640, 480), None)
    assert rec.calls == ["640x480"]


def test_apply_geometry_nothing_is_a_noop():
    rec = _GeoRecorder()
    rec._apply_geometry(None, None)
    assert rec.calls == []


# --------------------------------------------------------------------------
# positioning math
# --------------------------------------------------------------------------

def test_center_on_screen_is_within_bounds(root):
    x, y = positioning.center_on_screen(root)
    assert x >= 0 and y >= 0
    assert x <= root.winfo_screenwidth()
    assert y <= root.winfo_screenheight()


def test_center_on_parent_offsets_from_parent_origin(root):
    top = ttk.Toplevel(title="child", size=(200, 100))
    top.update_idletasks()
    x, y = positioning.center_on_parent(top, root)
    # centered coordinates never sit above/left of the parent's own origin
    assert x >= root.winfo_rootx()
    assert y >= root.winfo_rooty()
    top.destroy()


def test_ensure_on_screen_clamps_far_offscreen(root):
    x, y = positioning.ensure_on_screen(root, 100000, 100000)
    assert x < root.winfo_screenwidth()
    assert y < root.winfo_screenheight()


# --------------------------------------------------------------------------
# icon semantics
# --------------------------------------------------------------------------

def test_toplevel_iconphoto_none_does_not_crash(root):
    # Pre-2.0 this raised: iconphoto=None fell into PhotoImage(file=None).
    top = ttk.Toplevel(title="noicon", iconphoto=None)
    top.destroy()


def test_toplevel_bad_iconphoto_path_warns_not_prints(root):
    with pytest.warns(UserWarning):
        top = ttk.Toplevel(title="badicon", iconphoto="/no/such/file.png")
    top.destroy()


# --------------------------------------------------------------------------
# style property + aqua guard
# --------------------------------------------------------------------------

def test_style_property_returns_singleton_for_both(root):
    top = ttk.Toplevel(title="s")
    assert root.style is Style.get_instance()
    assert top.style is Style.get_instance()
    top.destroy()


def test_overrideredirect_noop_on_aqua(root):
    top = ttk.Toplevel(title="aqua")
    top.winsys = "aqua"  # simulate macOS
    assert top.overrideredirect(True) is None
    # the request was ignored: the window is still managed
    assert not top.overrideredirect()
    top.destroy()
