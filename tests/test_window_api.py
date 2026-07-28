"""Headless tests for the 2.0 Window/Toplevel API normalization (PR B).

Covers the parts that are checkable without a real display:
- deprecated raw-Tk kwarg spellings normalize to snake_case (with a warning),
- the combined/edge-relative geometry string construction,
- the positioning math (center + clamp),
- the unified icon/`iconphoto` semantics (including the old `Toplevel`
  `iconphoto=None` crash),
- the consistent `style` property and the aqua `overrideredirect` guard.
"""
import re
import time
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.internal import positioning
from ttkbootstrap.style import Style
from ttkbootstrap.style._compat import normalize_window_kwargs
from ttkbootstrap.window import App, Toplevel, Window, _BaseWindow


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


def _settled(window, tries=40):
    """Wait until the window manager has actually placed `window`.

    A geometry request is not applied synchronously. Until the window has been
    mapped and positioned, `winfo_rootx()` can report a sentinel far off-screen
    (-32730 under XWayland), so a test that reads it immediately measures
    nothing at all -- and passes or fails on whether some earlier test happened
    to pump the event loop for long enough.
    """
    for _ in range(tries):
        window.update_idletasks()
        window.update()
        if window.winfo_rootx() > -10000:
            return window
        time.sleep(0.05)
    return window


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


def test_below_widget_stays_aligned_near_the_screen_edge(root):
    # A dropdown is anchored to its widget, so the free-window breathing room in
    # ensure_on_screen must not apply: with it, a target within 20px of the screen
    # edge had its dropdown pushed inward, off the widget it belongs to, while
    # nowhere near leaving the screen. Only a real overflow may move it.
    top = ttk.Toplevel(size=(300, 200))
    top.geometry("300x200+2+300")  # hard against the left edge
    target = ttk.Frame(top, width=120, height=24)
    target.place(x=0, y=0)
    _settled(top)

    popup = ttk.Toplevel(size=(200, 100))
    popup.update_idletasks()
    x, _ = positioning.below_widget(popup, target)
    assert x == target.winfo_rootx(), "the dropdown drifted off its target"
    popup.destroy()
    target.destroy()
    top.destroy()


def test_below_widget_flips_above_when_no_room_below(root):
    # A target pinned near the bottom of its monitor: the popup flips to sit
    # above the target rather than overflowing the screen bottom.
    top = ttk.Toplevel(size=(300, 40))
    screen_h = top.winfo_screenheight()
    top.geometry(f"300x40+200+{screen_h - 60}")
    target = ttk.Frame(top, width=120, height=24)
    target.pack(padx=4, pady=4)
    _settled(top)

    popup = ttk.Toplevel(size=(200, 220))
    popup.update_idletasks()
    x, y = positioning.below_widget(popup, target)
    # Placed above: the popup's bottom edge is at/above the target's top edge.
    assert y + 220 <= target.winfo_rooty() + 2
    popup.destroy()
    target.destroy()
    top.destroy()


# --------------------------------------------------------------------------
# centering before the first map
# --------------------------------------------------------------------------

def test_geometry_records_the_size_it_applies(root):
    win = ttk.Toplevel(master=root)
    win.withdraw()
    win.geometry("640x480")
    assert win._applied_size == (640, 480)
    # A move carries no size and must not clear the one already applied.
    win.geometry("+10+10")
    assert win._applied_size == (640, 480)
    # `geometry("")` hands the window back to its natural size, so the
    # remembered one stops being true and must not outlive it.
    win.geometry("")
    assert win._applied_size is None
    win.destroy()


def test_unmapped_size_prefers_the_size_that_was_applied(root):
    # The whole point: a window's content request is nothing like the size a
    # WxH geometry pins, and only the latter is what it will map at.
    win = ttk.Toplevel(master=root, size=(600, 400))
    ttk.Label(win, text="hi").pack()
    win.withdraw()
    win.update_idletasks()
    assert win.winfo_reqwidth() < 600, "expected the content to ask for less"
    assert win._unmapped_size() == (600, 400)
    win.destroy()


def test_unmapped_size_falls_back_to_content_raised_to_minsize(root):
    # No size was ever applied, so the content's request stands -- but Tk will
    # not map it smaller than minsize, so that floor is part of the answer.
    win = ttk.Toplevel(master=root)
    ttk.Label(win, text="hi").pack()
    win.withdraw()
    win.update_idletasks()
    win.minsize(500, 300)
    # The floor has to be the part doing the work, or this passes for the wrong
    # reason -- assert a value, not the implementation's own expression.
    assert win.winfo_reqwidth() < 500 and win.winfo_reqheight() < 300
    assert win._unmapped_size() == (500, 300)
    win.destroy()


def test_place_window_center_before_first_map_uses_the_size_it_will_have(root):
    # Centering a withdrawn window against its content request puts the window's
    # top-left near the screen center rather than the window itself -- measured
    # at ~(298, 216) out for a 600x400 window. This is what makes the
    # withdraw -> center -> deiconify recipe (a window that appears centered
    # instead of appearing and then jumping) actually land centered.
    win = ttk.Toplevel(master=root, size=(600, 400))
    ttk.Label(win, text="hi").pack()
    win.withdraw()
    win.update_idletasks()

    applied = []
    real = win.geometry

    def spy(spec=None):
        # Only a set call carries a spec; a query would append None and break
        # the parse below.
        if spec is not None:
            applied.append(spec)
        return real(spec)

    win.geometry = spy
    try:
        win.place_window_center()
    finally:
        del win.geometry

    def centered_for(size):
        x, y = positioning.center_on_screen(win, size=size)
        return positioning.ensure_on_screen(win, x, y, size=size)

    assert applied, "no geometry was applied"
    match = re.search(r"\+(-?\d+)\+(-?\d+)$", applied[-1])
    assert match is not None, f"no +x+y in {applied[-1]!r}"
    got = (int(match.group(1)), int(match.group(2)))
    assert got == centered_for((600, 400))
    request = (win.winfo_reqwidth(), win.winfo_reqheight())
    assert got != centered_for(request), "centered against the content request"
    win.destroy()


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


def test_app_default_icon_uses_default_flag_on_win32(root):
    # Regression: dialogs/pickers showed the Tk feather because the win32 app
    # icon was applied via `wm_iconbitmap(path)` (no `-default`), so child
    # toplevels did not inherit it. It must be applied with `default=` so it
    # becomes the app-wide default for every future toplevel.
    from ttkbootstrap.window import _APP_ICON_ICO, _DEFAULT_ICON_DATA
    if not _APP_ICON_ICO.is_file():
        pytest.skip("packaged .ico not present")
    top = ttk.Toplevel(title="iconspy")
    top.winsys = "win32"  # exercise the win32 branch regardless of host OS
    recorded = {}
    top.wm_iconbitmap = lambda bitmap=None, default=None: recorded.update(
        bitmap=bitmap, default=default
    )
    top._apply_default_icon(_DEFAULT_ICON_DATA)
    assert recorded.get("default") == str(_APP_ICON_ICO)
    assert recorded.get("bitmap") is None  # not the per-window positional form
    top.destroy()


def test_toplevel_explicit_ico_is_per_window_not_app_wide(root):
    # Regression: a secondary Toplevel's own .ico must apply to that window
    # only, not become the app-wide default (which would re-skin App + every
    # sibling toplevel). Only the root App's icon is app-wide (default=).
    top = ttk.Toplevel(title="own-icon")
    top.winsys = "win32"  # exercise the win32 branch regardless of host OS
    recorded = {}
    top.wm_iconbitmap = lambda bitmap=None, default=None: recorded.update(
        bitmap=bitmap, default=default
    )
    top._setup_icon("C:/some/custom.ico", default_data=None)
    assert recorded.get("default") is None                  # NOT app-wide
    assert recorded.get("bitmap") == "C:/some/custom.ico"   # this window only
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


# --------------------------------------------------------------------------
# Slice 2: App/Window and theme/themename naming aliases
# --------------------------------------------------------------------------

def test_app_is_canonical_and_window_is_a_permanent_alias():
    # App is the real class; Window is the same object, not a subclass -- so
    # repr/type().__name__/tracebacks read "App" while Window(...) keeps working.
    assert App is Window
    assert App.__name__ == "App"
    assert ttk.App is App and ttk.Window is App


def test_window_alias_isinstance_and_type_name(root):
    # The shared session root is created as ttk.Window(); it must be an App and
    # report App as its type name (the disambiguation payoff).
    assert isinstance(root, App)
    assert isinstance(root, Window)
    assert type(root).__name__ == "App"


def test_style_accepts_theme_and_themename_alias(root):
    # Both spellings reach the singleton and switch the theme; the fixture
    # restores the active theme on teardown.
    ttk.Style(themename="pydata-light")
    assert root.style.theme.name == "pydata-light"
    ttk.Style(theme="pydata-dark")
    assert root.style.theme.name == "pydata-dark"


def test_style_prefers_theme_when_both_given(root):
    # theme is canonical, so it wins when both are passed.
    ttk.Style(theme="pydata-dark", themename="pydata-light")
    assert root.style.theme.name == "pydata-dark"


def test_window_kwargs_are_warning_free_for_new_names():
    # theme/themename are permanent aliases -- neither may emit a warning. Verify
    # at the signature level (a second live root can't be constructed here).
    import inspect
    params = inspect.signature(App.__init__).parameters
    assert "theme" in params and "themename" in params
    # theme is the second positional; themename is keyword-only.
    assert params["theme"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params["themename"].kind is inspect.Parameter.KEYWORD_ONLY


# --------------------------------------------------------------------------
# on_close lifecycle handler
# --------------------------------------------------------------------------

def _fire_close(win):
    """Invoke the WM_DELETE_WINDOW handler the way the window manager would."""
    cmd = win.tk.call("wm", "protocol", win._w, "WM_DELETE_WINDOW")
    win.tk.call(cmd)


def test_on_close_runs_callback_then_destroys(root):
    top = ttk.Toplevel(title="closes")
    calls = []
    top.on_close(lambda: calls.append(1))
    _fire_close(top)
    assert calls == [1]
    assert not top.winfo_exists()  # auto-destroyed, no manual destroy() needed


def test_on_close_returns_callback_for_decorator_use(root):
    top = ttk.Toplevel(title="deco")
    cb = lambda: None
    assert top.on_close(cb) is cb
    top.destroy()


def test_on_close_veto_keeps_window_open(root):
    top = ttk.Toplevel(title="veto")
    calls = []

    def veto():
        calls.append(1)
        return False

    top.on_close(veto)
    _fire_close(top)
    assert calls == [1]
    assert top.winfo_exists()  # returning False cancels the close
    top.destroy()


def test_on_close_constructor_kwarg(root):
    calls = []
    top = ttk.Toplevel(title="kw", on_close=lambda: calls.append(1))
    _fire_close(top)
    assert calls == [1]
    assert not top.winfo_exists()


def test_on_close_tolerates_callback_self_destroy(root):
    top = ttk.Toplevel(title="selfdestruct")
    top.on_close(lambda: top.destroy())
    _fire_close(top)  # the auto-destroy must not raise on an already-dead window
    assert not top.winfo_exists()


def test_on_close_replaces_previous_handler(root):
    top = ttk.Toplevel(title="replace")
    order = []

    def first():
        order.append("first")
        return False  # veto so the window survives for the second handler

    top.on_close(first)
    _fire_close(top)
    assert order == ["first"] and top.winfo_exists()

    top.on_close(lambda: order.append("second"))
    _fire_close(top)
    assert order == ["first", "second"] and not top.winfo_exists()


def test_on_close_on_app_root_veto(root):
    # `root` is the shared App fixture, so only exercise the veto path (which
    # keeps it alive); this covers on_close on App as well as Toplevel.
    calls = []

    def veto():
        calls.append(1)
        return False

    root.on_close(veto)
    _fire_close(root)
    assert calls == [1] and root.winfo_exists()
    root.protocol("WM_DELETE_WINDOW", "")  # reset so the shared root is untouched


# --- monitor discovery -----------------------------------------------------
#
# Tk exposes no monitor enumeration on any platform, so the layout comes from
# screeninfo when installed and from X11's Xinerama extension otherwise. The
# ctypes query itself needs a real X server; these cover the chain around it.

def test_xinerama_query_is_skipped_off_x11(monkeypatch):
    # It must not try to load libX11 on Windows or macOS.
    import sys

    loaded = []
    monkeypatch.setattr(positioning, "_load_library", lambda name: loaded.append(name))
    for platform in ("win32", "darwin", "cygwin"):
        monkeypatch.setattr(positioning, "_XINERAMA_UNAVAILABLE", False)
        monkeypatch.setattr(sys, "platform", platform)
        assert positioning._xinerama_monitors() is None
    assert loaded == []


def test_monitors_falls_back_to_xinerama_without_screeninfo(monkeypatch):
    layout = [(0, 0, 1920, 1080), (1920, 0, 2560, 1440)]
    monkeypatch.setattr(positioning, "_HAS_SCREENINFO", False)
    monkeypatch.setattr(positioning, "_xinerama_monitors", lambda: layout)
    assert positioning._monitors() == layout
    # and a point resolves to the monitor that contains it, not the first one
    assert positioning._monitor_at_point(2000, 500) == (1920, 0, 2560, 1440)


def test_monitors_falls_back_when_screeninfo_raises(monkeypatch):
    layout = [(0, 0, 1920, 1080)]
    monkeypatch.setattr(positioning, "_HAS_SCREENINFO", True)
    monkeypatch.setattr(
        positioning, "get_monitors", lambda: (_ for _ in ()).throw(RuntimeError("no display")),
        raising=False,
    )
    monkeypatch.setattr(positioning, "_xinerama_monitors", lambda: layout)
    assert positioning._monitors() == layout


def test_monitor_at_point_returns_none_when_no_source_answers(monkeypatch):
    monkeypatch.setattr(positioning, "_HAS_SCREENINFO", False)
    monkeypatch.setattr(positioning, "_xinerama_monitors", lambda: None)
    assert positioning._monitor_at_point(10, 10) is None


def test_placement_stays_on_screen_when_no_layout_is_available(root, monkeypatch):
    # macOS without `screeninfo` has no monitor enumeration at all -- Xinerama is
    # X11-only -- so the layout is unknown and placement falls back to Tk's own
    # screen metrics. We cannot test multi-monitor aqua without the hardware, so
    # pin the property that makes the unknown safe: with no layout, a window still
    # lands fully inside the screen Tk describes. The worst case is then landing
    # on the wrong display, never straddling two or hanging off the edge.
    monkeypatch.setattr(positioning, "_HAS_SCREENINFO", False)
    monkeypatch.setattr(positioning, "_xinerama_monitors", lambda: None)
    assert positioning._monitors() is None

    win = ttk.Toplevel(master=root, size=(400, 200))
    win.withdraw()
    win.update_idletasks()
    size = (400, 200)

    # centering falls back to winfo_screenwidth/height, anchored at the origin
    x, y = positioning.center_on_screen(win, size=size)
    assert 0 <= x and x + size[0] <= win.winfo_screenwidth()
    assert 0 <= y and y + size[1] <= win.winfo_screenheight()

    # clamping falls back to the virtual root; a point hard against the right
    # edge is pulled back far enough for the whole window to fit
    right_edge = win.winfo_vrootx() + win.winfo_vrootwidth()
    cx, _ = positioning.ensure_on_screen(win, right_edge - 10, 0, size=size)
    assert cx + size[0] <= right_edge
    win.destroy()


def test_clamp_uses_the_monitor_under_the_point_not_the_whole_desktop(root, monkeypatch):
    # The case that motivated this: two monitors side by side, a window that
    # would straddle the join. Clamping against the combined desktop leaves it
    # straddling; clamping against the monitor pulls it fully onto one screen.
    monkeypatch.setattr(positioning, "_HAS_SCREENINFO", False)
    monkeypatch.setattr(
        positioning, "_xinerama_monitors", lambda: [(0, 0, 1920, 1080), (1920, 0, 1920, 1080)]
    )
    top = ttk.Toplevel(title="child", size=(400, 200))
    top.update_idletasks()
    # ask to sit across the seam at x=1920
    x, _ = positioning.ensure_on_screen(top, 1800, 300, size=(400, 200))
    assert x + 400 <= 1920, "the window should be pulled fully onto the left monitor"
    top.destroy()
