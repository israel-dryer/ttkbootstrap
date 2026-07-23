"""Headless tests for the Tk 8.6 / Tk 9 scroll-event contract (issue #1290).

Tk 9 normalizes wheel deltas to multiples of 120 on every platform, stops
delivering `<Button-4>`/`<Button-5>` to scripts on X11, and routes every
precise-delta device (any Apple trackpad or Magic Mouse) through
`<TouchpadScroll>` instead of `<MouseWheel>`. These pin the normalization
helpers and the ScrolledFrame bindings that consume them.

The touchpad cases only run on a Tk that generates the event; the rest are
version-independent. Uses the shared `root` fixture from conftest.
"""
import tkinter

import pytest

from ttkbootstrap.internal import wheel
from ttkbootstrap.widgets.scrolled import ScrolledFrame

requires_touchpad = pytest.mark.skipif(
    not wheel.has_touchpad_scroll(),
    reason="Tk 8.6 generates no <TouchpadScroll> events",
)


def _notch_event(widget, down=True):
    """A wheel event carrying exactly one notch on the running Tk.

    Tk 8.6 on aqua reported a notch as 1; every other build uses 120, so the
    raw delta a real device sends is not the same number everywhere.
    """
    event = tkinter.Event()
    event.num = "??"
    unit = 1 if wheel.wheel_notches(widget, _delta_event(1)) == 1.0 else 120
    event.delta = -unit if down else unit
    return event


def _delta_event(delta):
    event = tkinter.Event()
    event.num = "??"
    event.delta = delta
    return event


def _tall_frame(root, rows=80):
    """A realized ScrolledFrame whose content overflows the viewport."""
    sf = ScrolledFrame(root, auto_hide=False, height=200, width=300)
    sf.pack(fill="both", expand=True)
    for i in range(rows):
        tkinter.Label(sf, text=f"row {i}").pack(anchor="w")
    for _ in range(3):
        root.update_idletasks()
        root.update()
    return sf


# --------------------------------------------------------------------------- #
# normalization helpers
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(
    not wheel.has_touchpad_scroll(), reason="Tk 8.6 aqua reports a notch as 1"
)
def test_one_notch_is_one_unit(root):
    """A normalized (Tk 8.7+) 120-delta event is one notch, not 120."""
    assert wheel.wheel_notches(root, _delta_event(-120)) == pytest.approx(-1.0)
    assert wheel.wheel_notches(root, _delta_event(240)) == pytest.approx(2.0)


def test_x11_buttons_report_a_notch_each_way(root):
    up, down = tkinter.Event(), tkinter.Event()
    up.num, down.num = 4, 5
    assert wheel.wheel_notches(root, up) == 1.0
    assert wheel.wheel_notches(root, down) == -1.0


def test_precise_deltas_unpack_both_signed_axes():
    """`%D` packs dx in the high word and a signed dy in the low word."""
    event = tkinter.Event()
    event.delta = (3 << 16) | (0x10000 - 7)  # dx=3, dy=-7
    assert wheel.precise_deltas(event) == (3, -7)

    event.delta = (-2 << 16) | 5
    assert wheel.precise_deltas(event) == (-2, 5)


def test_pixel_accumulator_carries_the_remainder():
    acc = wheel.PixelAccumulator()
    assert acc.add(0, 9, 1, 10)[1] == 0       # not a whole step yet
    assert acc.add(0, 9, 1, 10)[1] == 1       # 18px -> one step, 8px carried
    acc.reset()
    assert acc.add(0, 9, 1, 10)[1] == 0       # remainder dropped


def test_x11_buttons_only_on_legacy_tk(root):
    """Tk 8.7+ translates Button-4/5 internally, so they must not be bound."""
    if wheel.has_touchpad_scroll():
        assert not wheel.uses_x11_buttons(root)
        assert wheel.wheel_sequences(root) == ("<MouseWheel>",)


# --------------------------------------------------------------------------- #
# ScrolledFrame
# --------------------------------------------------------------------------- #
def test_wheel_is_bound_on_every_platform(root):
    """The wheel tag always carries a sequence Tk actually delivers here."""
    sf = _tall_frame(root)
    bound = set(root.tk.call("bind", sf._wheel_tag))
    assert set(wheel.wheel_sequences(sf)) <= bound
    sf.destroy()


@requires_touchpad
def test_touchpad_scroll_is_bound(root):
    sf = _tall_frame(root)
    assert wheel.TOUCHPAD_SCROLL in root.tk.call("bind", sf._wheel_tag)
    sf.destroy()


def test_one_notch_scrolls_one_unit_not_to_the_end(root):
    """The Tk 9 regression: one notch jumped the view to the bottom."""
    sf = _tall_frame(root)
    canvas = sf._canvas
    sf._on_mousewheel(_notch_event(sf))
    root.update_idletasks()
    first, _ = canvas.yview()
    assert 0.0 < first < 0.5, f"one notch moved to {first}"
    sf.destroy()


def test_wheel_does_not_scroll_content_that_fits(root):
    sf = _tall_frame(root, rows=1)
    sf._on_mousewheel(_notch_event(sf))
    root.update_idletasks()
    assert sf._canvas.yview()[0] == 0.0
    sf.destroy()


@requires_touchpad
def test_touchpad_gesture_scrolls_the_canvas(root):
    """A run of precise deltas moves the view instead of doing nothing."""
    sf = _tall_frame(root)
    canvas = sf._canvas
    event = tkinter.Event()
    event.delta = 0x10000 - 12  # dy = -12 px, one gesture tick
    for _ in range(20):
        sf._on_touchpad_scroll(event)
    root.update_idletasks()
    first, _ = canvas.yview()
    assert first > 0.0, "trackpad gesture did not scroll"
    sf.destroy()


def test_destroy_unbinds_the_wheel_tag(root):
    sf = _tall_frame(root)
    tag = sf._wheel_tag
    sf.destroy()
    root.update_idletasks()
    assert root.tk.call("bind", tag) == ""