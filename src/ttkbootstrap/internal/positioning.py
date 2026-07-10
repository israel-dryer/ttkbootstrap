"""Window positioning helpers (private plumbing, no back-compat guarantee).

A small, ttkbootstrap-scoped subset of bootstack's ``WindowPositioning``
(``bootstack/src/bootstack/_runtime/window_utilities.py``) — just the three
mechanisms ``Window``/``Toplevel`` and the dialogs need: center-on-screen,
center-on-parent, and clamp-into-the-visible-monitor. Each is a pure geometry
calculation returning ``(x, y)``; the caller applies the geometry string.

Multi-monitor awareness is optional: if the third-party ``screeninfo`` package
is importable we resolve the monitor under a point, otherwise we fall back to
Tk's virtual-root dimensions (single logical screen). No new hard dependency —
Pillow stays the only required runtime dep.
"""
from __future__ import annotations

import tkinter
from typing import Optional, Tuple

try:
    from screeninfo import get_monitors  # type: ignore
    _HAS_SCREENINFO = True
except Exception:  # pragma: no cover - screeninfo is an optional extra
    _HAS_SCREENINFO = False

Rect = Tuple[int, int, int, int]  # (x, y, width, height)


def _monitor_at_point(x: int, y: int) -> Optional[Rect]:
    """Return the ``(x, y, w, h)`` bounds of the monitor containing a point.

    Returns ``None`` when ``screeninfo`` is unavailable so callers fall back to
    Tk's screen/virtual-root metrics. When ``screeninfo`` is present but the
    point is on no monitor, the first monitor is returned as a sane default.
    """
    if not _HAS_SCREENINFO:
        return None
    try:
        monitors = get_monitors()
        for m in monitors:
            if m.x <= x < m.x + m.width and m.y <= y < m.y + m.height:
                return (m.x, m.y, m.width, m.height)
        if monitors:
            m = monitors[0]
            return (m.x, m.y, m.width, m.height)
    except Exception:
        pass
    return None


def _window_size(window: tkinter.Misc) -> Tuple[int, int]:
    """Best-available (width, height): the realized (mapped) size, else the
    requested size before the window has been mapped.

    ``winfo_width``/``winfo_height`` return ``1`` until the window is mapped, so
    fall back to the request only then. Do NOT ``max()`` the two: once mapped, a
    window whose content wants more than its actual size reports a larger
    ``reqheight`` than it occupies, and using that inflated value mis-centers the
    window (e.g. pinning it to the top of a small screen instead of centering)."""
    width = window.winfo_width()
    height = window.winfo_height()
    if width <= 1:
        width = window.winfo_reqwidth()
    if height <= 1:
        height = window.winfo_reqheight()
    return width, height


def center_on_screen(window: tkinter.Misc) -> Tuple[int, int]:
    """Coordinates that center ``window`` on the screen.

    With ``screeninfo`` installed, centers on the monitor under the mouse
    cursor (the display the user is most likely looking at); otherwise centers
    on Tk's single reported screen. The result is clamped so the window stays
    fully within that monitor — on a multi-monitor layout the target display can
    have a negative origin (e.g. a screen to the left of the primary), and a
    window larger than the monitor is pinned to its top-left rather than
    overflowing. Call ``update_idletasks()`` first for an accurate size — this
    method does so as well.
    """
    window.update_idletasks()
    w_width, w_height = _window_size(window)
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


def center_on_parent(window: tkinter.Misc, parent: tkinter.Misc) -> Tuple[int, int]:
    """Coordinates (in screen space) that center ``window`` over ``parent``."""
    window.update_idletasks()
    parent.update_idletasks()
    w_width, w_height = _window_size(window)
    p_x = parent.winfo_rootx()
    p_y = parent.winfo_rooty()
    p_width = max(parent.winfo_width(), parent.winfo_reqwidth())
    p_height = max(parent.winfo_height(), parent.winfo_reqheight())
    x = p_x + max(0, (p_width - w_width) // 2)
    y = p_y + max(0, (p_height - w_height) // 2)
    return int(x), int(y)


def below_widget(
        window: tkinter.Misc,
        target: tkinter.Misc,
        padding: int = 20,
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
    """
    window.update_idletasks()
    target.update_idletasks()
    _, w_height = _window_size(window)
    tx = target.winfo_rootx()
    ty = target.winfo_rooty()
    t_height = max(target.winfo_height(), target.winfo_reqheight())

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
) -> Tuple[int, int]:
    """Clamp ``(x, y)`` so the window stays fully visible on its monitor.

    ``titlebar_height`` reserves extra room at the top for window-manager
    decorations that ``winfo_height`` does not include, keeping the titlebar
    on-screen. Uses the ``screeninfo`` monitor under the proposed point when
    available (so a window that legitimately belongs on a secondary monitor is
    not yanked back to the primary), else Tk's virtual-root bounds.
    """
    window.update_idletasks()
    w_width, w_height = _window_size(window)

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
