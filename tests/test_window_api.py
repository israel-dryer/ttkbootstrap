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
    # The window must land fully inside its target monitor. On a multi-monitor
    # layout that monitor can have a negative origin (a display left of/above the
    # primary), so asserting `x >= 0` is wrong — resolve the same monitor the
    # function centers on and assert against its bounds.
    x, y = positioning.center_on_screen(root)
    w_width, w_height = positioning._window_size(root)
    monitor = positioning._monitor_at_point(
        root.winfo_pointerx(), root.winfo_pointery()
    )
    if monitor:
        mx, my, mw, mh = monitor
    else:
        mx, my = 0, 0
        mw, mh = root.winfo_screenwidth(), root.winfo_screenheight()
    # `max(0, ...)` keeps the bound valid even if the window is larger than the
    # monitor, in which case the function pins it to the monitor's top-left.
    assert mx <= x <= mx + max(0, mw - w_width)
    assert my <= y <= my + max(0, mh - w_height)


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


def test_below_widget_drops_below_left_aligned(root):
    # A target with room beneath it: the popup's top-left sits at the target's
    # bottom-left (standard dropdown placement).
    target = ttk.Frame(root, width=120, height=24)
    target.place(x=10, y=10)
    target.update_idletasks()
    popup = ttk.Toplevel(size=(200, 100))
    popup.update_idletasks()
    x, y = positioning.below_widget(popup, target)
    assert x == target.winfo_rootx()
    assert y >= target.winfo_rooty() + target.winfo_height() - 1
    popup.destroy()
    target.destroy()


def test_below_widget_flips_above_when_no_room_below(root):
    # A target pinned near the bottom of its monitor: the popup flips to sit
    # above the target rather than overflowing the screen bottom.
    top = ttk.Toplevel(size=(300, 40))
    screen_h = top.winfo_screenheight()
    top.geometry(f"300x40+200+{screen_h - 60}")
    target = ttk.Frame(top, width=120, height=24)
    target.pack(padx=4, pady=4)
    top.update_idletasks()
    top.update()

    popup = ttk.Toplevel(size=(200, 220))
    popup.update_idletasks()
    x, y = positioning.below_widget(popup, target)
    # Placed above: the popup's bottom edge is at/above the target's top edge.
    assert y + 220 <= target.winfo_rooty() + 2
    popup.destroy()
    target.destroy()
    top.destroy()


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


# --------------------------------------------------------------------------
# aqua native window-style for borderless popups (tooltip titlebar fix)
# --------------------------------------------------------------------------

class _RecordingTk:
    """Records ``call(...)`` args; the helper touches nothing else on ``tk``."""
    def __init__(self):
        self.calls = []

    def call(self, *args):
        self.calls.append(args)
        return ""


def _capture_mac_style(top, window_type):
    # tkapp.call is read-only, so swap the whole tk handle for the duration of
    # the helper (restored before destroy so teardown still works).
    real_tk, rec = top.tk, _RecordingTk()
    top.tk = rec
    try:
        top._apply_mac_window_style(window_type)
    finally:
        top.tk = real_tk
    return rec.calls


def test_apply_mac_window_style_borderless_types(root):
    # On aqua the borderless types map to a native window class so the popup
    # isn't drawn with a titlebar. Simulate aqua and capture the Tk call.
    from ttkbootstrap.window import _AQUA_WINDOW_STYLES
    top = ttk.Toplevel(title="aqua")
    top.winsys = "aqua"
    calls = _capture_mac_style(top, "tooltip")
    assert calls == [("::tk::unsupported::MacWindowStyle", "style", top,
                      *_AQUA_WINDOW_STYLES["tooltip"])]
    top.destroy()


def test_apply_mac_window_style_noop_off_aqua(root):
    # Off aqua the native call must never fire (window_type stays x11-only).
    top = ttk.Toplevel(title="x11")
    top.winsys = "x11"
    assert _capture_mac_style(top, "tooltip") == []
    top.destroy()


def test_apply_mac_window_style_ignores_unknown_type(root):
    # A type with no native equivalent (e.g. "dialog") keeps default chrome.
    top = ttk.Toplevel(title="aqua")
    top.winsys = "aqua"
    assert _capture_mac_style(top, "dialog") == []
    top.destroy()


# --------------------------------------------------------------------------
# packaged app icon (built by tools/make_app_ico.py)
# --------------------------------------------------------------------------

def test_app_ico_is_packed_with_expected_sizes():
    """The committed .ico must exist and carry every advertised size, so a stale
    or un-regenerated asset is caught rather than shipping a broken icon."""
    from PIL import Image
    from ttkbootstrap.window import _APP_ICON_ICO

    assert _APP_ICON_ICO.is_file(), "run tools/make_app_ico.py to build the .ico"
    with Image.open(_APP_ICON_ICO) as im:
        packed = {s[0] for s in im.ico.sizes()}
    assert {16, 24, 32, 48, 64, 128, 256} <= packed


def test_default_icon_falls_back_when_asset_missing(root, monkeypatch):
    """If the packaged icon files are missing, the default brand icon still
    applies via the embedded base64 fallback (icon is always set)."""
    import ttkbootstrap.window as win
    from pathlib import Path

    monkeypatch.setattr(win, "_APP_ICON_ICO", Path("does-not-exist.ico"))
    monkeypatch.setattr(win, "_APP_ICON_PNG", Path("does-not-exist.png"))
    top = ttk.Toplevel(title="fallback")
    top._apply_default_icon(win._DEFAULT_ICON_DATA)
    assert top._icon is not None  # base64 fallback produced a PhotoImage
    top.destroy()
