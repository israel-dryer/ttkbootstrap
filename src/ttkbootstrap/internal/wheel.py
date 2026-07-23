"""Scroll-gesture normalization across Tk 8.6 and Tk 9.

Tk 9 changed the scroll-event contract in two ways that break code written
against Tk 8.6:

* A precise-delta device -- every Apple trackpad, Magic Mouse and Magic
  Trackpad -- now fires `<TouchpadScroll>` and **never** `<MouseWheel>`.
  Binding only the wheel leaves those devices completely dead.
* Wheel deltas are normalized to multiples of 120 on every windowing system.
  On aqua a notch used to report 1; it now reports 120.

On X11, `<Button-4>`/`<Button-5>` are no longer delivered to scripts at all
-- Tk translates them to `<MouseWheel>` internally (TIP 474).

This module hides all of that behind one vocabulary: callers ask for the
sequences to bind, then convert an incoming event to either wheel *notches*
or precise *pixels*.

Sign convention (matching Tk's own bindings): a positive value means the
wheel rolled away from the user, i.e. the view should move toward the
*start* of the content. Callers negate to get a scroll amount.
"""

import tkinter

from ttkbootstrap.utils import windowing_system

TOUCHPAD_SCROLL = "<TouchpadScroll>"
"""Sequence for precise-delta scroll gestures. Tk 8.7+ only."""

_WHEEL_UNITS = 120.0
"""Delta reported for one wheel notch on a normalized (Tk 8.7+) build."""

_TOUCHPAD_TK = 8.7
"""First Tk release generating `<TouchpadScroll>` and normalized deltas."""


def has_touchpad_scroll() -> bool:
    """Return whether the running Tk generates `<TouchpadScroll>` events."""
    return tkinter.TkVersion >= _TOUCHPAD_TK


def uses_x11_buttons(widget) -> bool:
    """Return whether wheel input arrives as `<Button-4>`/`<Button-5>` here.

    True only on legacy X11 builds: Tk 8.7+ translates those buttons to
    `<MouseWheel>` and stops delivering them to scripts.
    """
    return not has_touchpad_scroll() and windowing_system(widget) == "x11"


def wheel_sequences(widget, shift: bool = False):
    """Return the event sequences carrying wheel notches for `widget`.

    Parameters:

        widget (Misc):
            Any widget; used to resolve the windowing system.

        shift (bool):
            Request the horizontal (Shift-modified) sequences.

    Returns:

        Tuple[str, ...]:
            The sequences to bind.
    """
    if uses_x11_buttons(widget):
        if shift:
            return ("<Shift-Button-4>", "<Shift-Button-5>")
        return ("<Button-4>", "<Button-5>")
    return ("<Shift-MouseWheel>",) if shift else ("<MouseWheel>",)


def wheel_notches(widget, event) -> float:
    """Return the signed notch count for a wheel event.

    One physical notch is 1.0 on every platform and Tk version. The value is
    positive when the wheel rolled away from the user.
    """
    num = getattr(event, "num", None)
    if num in (4, 6):
        return 1.0
    if num in (5, 7):
        return -1.0

    try:
        delta = float(event.delta)
    except (AttributeError, TypeError, ValueError):
        return 0.0
    if not delta:
        return 0.0

    # Tk 8.6 on aqua reported one notch as 1; everything else uses 120.
    if not has_touchpad_scroll() and windowing_system(widget) == "aqua":
        return delta
    return delta / _WHEEL_UNITS


def precise_deltas(event):
    """Unpack a `<TouchpadScroll>` event into `(dx, dy)` pixels.

    Tk packs both axes into the delta field as two signed 16-bit values;
    this mirrors Tcl's `::tk::PreciseScrollDeltas`.
    """
    try:
        packed = int(event.delta)
    except (AttributeError, TypeError, ValueError):
        return (0, 0)
    dx = packed >> 16
    low = packed & 0xFFFF
    dy = low if low < 0x8000 else low - 0x10000
    return (dx, dy)


def scale_num(widget, value) -> int:
    """Scale a pixel amount for display density, like `::tk::ScaleNum`."""
    try:
        scaling = float(widget.tk.call("tk", "scaling"))
    except (tkinter.TclError, TypeError, ValueError):
        scaling = 1.0
    return round(value * scaling * 0.75)


class PixelAccumulator:
    """Converts precise pixel deltas into whole discrete scroll steps.

    A touchpad reports small deltas roughly sixty times a second. Widgets
    that scroll by rows or canvas units cannot act on each one, so the
    fractional remainder is carried forward until it adds up to a step.
    """

    __slots__ = ("_x", "_y")

    def __init__(self) -> None:
        self._x = 0.0
        self._y = 0.0

    def add(self, dx, dy, step_x, step_y):
        """Add a delta and return the whole `(x, y)` steps it completes."""
        step_x = step_x if step_x and step_x > 0 else 1.0
        step_y = step_y if step_y and step_y > 0 else 1.0
        self._x += dx
        self._y += dy
        out_x = int(self._x / step_x)
        out_y = int(self._y / step_y)
        self._x -= out_x * step_x
        self._y -= out_y * step_y
        return (out_x, out_y)

    def reset(self) -> None:
        """Drop any carried remainder."""
        self._x = 0.0
        self._y = 0.0