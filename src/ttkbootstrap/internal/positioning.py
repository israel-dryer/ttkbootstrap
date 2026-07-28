"""Window positioning helpers (private plumbing, no back-compat guarantee).

A small, ttkbootstrap-scoped subset of bootstack's ``WindowPositioning``
(``bootstack/src/bootstack/_runtime/window_utilities.py``) — just the three
mechanisms ``Window``/``Toplevel`` and the dialogs need: center-on-screen,
center-on-parent, and clamp-into-the-visible-monitor. Each is a pure geometry
calculation returning ``(x, y)``; the caller applies the geometry string.

Multi-monitor awareness comes from whichever source can answer, in order: the
third-party ``screeninfo`` package when it is installed, then X11's Xinerama
extension queried directly, then Tk's virtual-root dimensions (one logical
screen). No new hard dependency — Pillow stays the only required runtime dep.

Tk itself has no monitor enumeration on any platform: ``winfo screenwidth`` on
X11 reports the union of every display, and ``winfo vrootwidth`` falls back to
that same value unless a virtual-root window manager is running. The layout has
to come from the platform.
"""
from __future__ import annotations

import sys
import tkinter
from typing import List, Optional, Tuple

try:
    from screeninfo import get_monitors  # type: ignore
    _HAS_SCREENINFO = True
except Exception:  # pragma: no cover - screeninfo is an optional extra
    _HAS_SCREENINFO = False

Rect = Tuple[int, int, int, int]  # (x, y, width, height)

# set once a Xinerama query has proved impossible, so we don't reload libraries
# on every placement
_XINERAMA_UNAVAILABLE = False


def _load_library(name: str):  # pragma: no cover - X11 only
    """Load a shared library by short name, or return None."""
    import ctypes
    import ctypes.util

    candidates = (
        ctypes.util.find_library(name),
        f"lib{name}.so.6",
        f"lib{name}.so.1",
        f"lib{name}.so",
    )
    for candidate in candidates:
        if not candidate:
            continue
        try:
            return ctypes.CDLL(candidate)
        except OSError:
            continue
    return None


def _xinerama_monitors() -> Optional[List[Rect]]:  # pragma: no cover - X11 only
    """Monitor rects from X11's Xinerama extension, or None when unavailable.

    Asks the X server directly, the way ``screeninfo`` does, so multi-monitor
    placement works on a plain install. ctypes into a platform library is how
    the rest of the library reaches Windows' DPI and shell APIs.
    """
    global _XINERAMA_UNAVAILABLE
    if _XINERAMA_UNAVAILABLE or sys.platform in ("win32", "darwin", "cygwin"):
        return None
    try:
        import ctypes

        class _XineramaScreenInfo(ctypes.Structure):
            _fields_ = [
                ("screen_number", ctypes.c_int),
                ("x", ctypes.c_short),
                ("y", ctypes.c_short),
                ("width", ctypes.c_short),
                ("height", ctypes.c_short),
            ]

        xlib = _load_library("X11")
        xinerama = _load_library("Xinerama")
        if xlib is None or xinerama is None:
            _XINERAMA_UNAVAILABLE = True
            return None

        xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
        xlib.XOpenDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
        xlib.XFree.argtypes = [ctypes.c_void_p]
        xlib.XFree.restype = None

        display = xlib.XOpenDisplay(b"")
        if not display:
            _XINERAMA_UNAVAILABLE = True
            return None
        try:
            if not xinerama.XineramaIsActive(display):
                # a single-head server answers no query; Tk's screen metrics are
                # already correct there
                _XINERAMA_UNAVAILABLE = True
                return None
            count = ctypes.c_int()
            xinerama.XineramaQueryScreens.restype = ctypes.POINTER(_XineramaScreenInfo)
            infos = xinerama.XineramaQueryScreens(display, ctypes.byref(count))
            if not infos or count.value <= 0:
                return None
            try:
                screens = ctypes.cast(
                    infos, ctypes.POINTER(_XineramaScreenInfo * count.value)
                ).contents
                return [(s.x, s.y, s.width, s.height) for s in screens]
            finally:
                xlib.XFree(infos)
        finally:
            xlib.XCloseDisplay(display)
    except Exception:
        _XINERAMA_UNAVAILABLE = True
        return None


def _monitors() -> Optional[List[Rect]]:
    """Every monitor's bounds, or None when the layout can't be determined."""
    if _HAS_SCREENINFO:
        try:
            monitors = [(m.x, m.y, m.width, m.height) for m in get_monitors()]
            if monitors:
                return monitors
        except Exception:
            pass  # fall through to Xinerama rather than give up
    return _xinerama_monitors()


def _monitor_at_point(x: int, y: int) -> Optional[Rect]:
    """Return the ``(x, y, w, h)`` bounds of the monitor containing a point.

    Returns ``None`` when no source can describe the layout, so callers fall
    back to Tk's screen/virtual-root metrics. When the layout is known but the
    point is on no monitor, the first monitor is returned as a sane default.
    """
    monitors = _monitors()
    if not monitors:
        return None
    for rect in monitors:
        mx, my, mw, mh = rect
        if mx <= x < mx + mw and my <= y < my + mh:
            return rect
    return monitors[0]


def _window_size(window: tkinter.Misc) -> Tuple[int, int]:
    """The size a widget actually occupies: its realized (mapped) size, else its
    requested size before it has been mapped. Also used for drop targets/parents.

    Use ``winfo_ismapped()`` (not a ``winfo_width <= 1`` sniff, which a genuinely
    1px window -- e.g. the datepicker's ``minsize=(226, 1)`` -- would trip): a
    mapped widget's realized size IS its footprint. Do NOT ``max()`` it with the
    request -- once mapped, content that wants more than its box reports a larger
    ``reqheight``/``reqwidth`` than it occupies, and that inflated value
    mis-centers/mis-anchors (e.g. pinning a window to the top of a small screen).
    A withdrawn/unmapped widget has no realized size, so its request is best."""
    if window.winfo_ismapped():
        return window.winfo_width(), window.winfo_height()
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_on_screen(
        window: tkinter.Misc,
        size: Optional[Tuple[int, int]] = None,
) -> Tuple[int, int]:
    """Coordinates that center ``window`` on the screen.

    With ``screeninfo`` installed, centers on the monitor under the mouse
    cursor (the display the user is most likely looking at); otherwise centers
    on Tk's single reported screen. The result is clamped so the window stays
    fully within that monitor — on a multi-monitor layout the target display can
    have a negative origin (e.g. a screen to the left of the primary), and a
    window larger than the monitor is pinned to its top-left rather than
    overflowing. Call ``update_idletasks()`` first for an accurate size — this
    method does so as well. ``size`` overrides the measured size for a window
    that is not mapped yet (see :func:`center_on_parent`).
    """
    window.update_idletasks()
    w_width, w_height = size if size is not None else _window_size(window)
    monitor = _monitor_at_point(window.winfo_pointerx(), window.winfo_pointery())
    if monitor:
        mx, my, mw, mh = monitor
    else:
        mx, my = 0, 0
        mw, mh = window.winfo_screenwidth(), window.winfo_screenheight()
    x = mx + (mw - w_width) // 2
    y = my + (mh - w_height) // 2
    # Keep the window inside the monitor: never let a large window overflow past
    # the monitor's own origin (which may itself be negative on a secondary
    # display), and never off its far edge.
    x = max(mx, min(x, mx + mw - w_width))
    y = max(my, min(y, my + mh - w_height))
    return int(x), int(y)


def center_on_parent(
        window: tkinter.Misc,
        parent: tkinter.Misc,
        size: Optional[Tuple[int, int]] = None,
) -> Tuple[int, int]:
    """Coordinates (in screen space) that center ``window`` over ``parent``.

    Pass ``size`` when the caller has just sized a window that is not mapped yet:
    a floor applied through ``wm geometry`` or ``wm minsize`` does not reach
    ``winfo_reqwidth``, so :func:`_window_size` would measure a smaller window
    than the one the user ends up seeing.
    """
    window.update_idletasks()
    parent.update_idletasks()
    w_width, w_height = size if size is not None else _window_size(window)
    p_x = parent.winfo_rootx()
    p_y = parent.winfo_rooty()
    # actual occupied size, not the inflated content request (see _window_size)
    p_width, p_height = _window_size(parent)
    x = p_x + max(0, (p_width - w_width) // 2)
    y = p_y + max(0, (p_height - w_height) // 2)
    return int(x), int(y)


def below_widget(
        window: tkinter.Misc,
        target: tkinter.Misc,
        padding: int = 0,
        gap: int = 3,
) -> Tuple[int, int]:
    """Coordinates that drop ``window`` directly below ``target``, left-aligned.

    Standard dropdown placement: the window's top-left sits at the target's
    bottom-left, plus a small ``gap`` so the two don't touch. When there is not
    enough room below the target on its monitor (the window would run off the
    bottom), it is flipped to sit *above* the target instead — its bottom-left a
    ``gap`` above the target's top-left — provided there is room there. The result
    is passed through :func:`ensure_on_screen` so it never overflows horizontally
    or off the opposite edge.

    ``padding`` defaults to 0 for the same reason ``titlebar_height`` does below:
    a dropdown is anchored to a widget, not placed freely, so the breathing room
    :func:`ensure_on_screen` keeps around a floating window would break the
    alignment that matters here. With the default 20 a target within 20px of the
    screen edge had its dropdown pushed inward — visibly off its own widget —
    while still being nowhere near leaving the screen.
    """
    window.update_idletasks()
    target.update_idletasks()
    _, w_height = _window_size(window)
    tx = target.winfo_rootx()
    ty = target.winfo_rooty()
    # actual occupied height, not the inflated content request (see _window_size)
    _, t_height = _window_size(target)

    monitor = _monitor_at_point(tx, ty)
    if monitor:
        _, screen_y0, _, screen_h = monitor
    else:
        screen_y0 = window.winfo_vrooty()
        screen_h = window.winfo_vrootheight()
    screen_y1 = screen_y0 + screen_h

    x = tx
    y = ty + t_height + gap
    # Flip above only when the drop would overflow the bottom AND there is room
    # above; otherwise stay below and let ensure_on_screen clamp the edge.
    if y + w_height > screen_y1:
        y_above = ty - w_height - gap
        if y_above >= screen_y0:
            y = y_above
    # titlebar_height=0: a dropdown is frameless, so no decoration to reserve.
    return ensure_on_screen(window, x, y, padding=padding, titlebar_height=0)


def ensure_on_screen(
        window: tkinter.Misc,
        x: int,
        y: int,
        padding: int = 20,
        titlebar_height: int = 60,
        size: Optional[Tuple[int, int]] = None,
) -> Tuple[int, int]:
    """Clamp ``(x, y)`` so the window stays fully visible on its monitor.

    ``titlebar_height`` reserves extra room at the top for window-manager
    decorations that ``winfo_height`` does not include, keeping the titlebar
    on-screen. Uses the ``screeninfo`` monitor under the proposed point when
    available (so a window that legitimately belongs on a secondary monitor is
    not yanked back to the primary), else Tk's virtual-root bounds.

    ``size`` overrides the measured size, for a window that is not mapped yet --
    see :func:`center_on_parent`. Clamping against too small a size
    under-corrects and leaves the window's far edge off-screen.
    """
    window.update_idletasks()
    w_width, w_height = size if size is not None else _window_size(window)

    monitor = _monitor_at_point(x, y)
    if monitor:
        screen_x0, screen_y0, screen_width, screen_height = monitor
    else:
        screen_x0 = window.winfo_vrootx()
        screen_y0 = window.winfo_vrooty()
        screen_width = window.winfo_vrootwidth()
        screen_height = window.winfo_vrootheight()

    screen_x1 = screen_x0 + screen_width
    screen_y1 = screen_y0 + screen_height

    x = max(screen_x0 + padding, min(x, screen_x1 - w_width - padding))
    y = max(screen_y0 + padding, min(y, screen_y1 - w_height - titlebar_height))
    return int(x), int(y)
