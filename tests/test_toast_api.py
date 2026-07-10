"""API tests for the ToastNotification normalization (widget review PR 7).

Headless (uses the shared ``root`` fixture from conftest). Covers the
self-deprecation fix, the font-glyph icon, the timer/fade lifecycle, and the
concurrent-toast stack manager. Actual on-screen fade/animation is only
structurally checked here.
"""
import re
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.widgets.toast import ToastNotification, _TOAST_STACK, _DEFAULT_ICON


@pytest.fixture(scope="module", autouse=True)
def _clear_image_cache_after_module():
    """The glyph icons these toasts render populate the process-global
    ``Style._image_cache``; clear it on teardown so this module imposes no
    test-order dependency on ``widget_styles/test_image_cache``.
    """
    yield
    try:
        Style.get_instance().clear_image_cache()
    except Exception:
        pass


@pytest.fixture(autouse=True)
def _reset_stack():
    """Keep each test's toasts from leaking into the shared corner registry."""
    _TOAST_STACK._corners.clear()
    yield
    _TOAST_STACK._corners.clear()


def _ypos(toast):
    """The absolute y coordinate from a toast's geometry string (e.g.
    '300x75+2255+1315')."""
    m = re.search(r"([+-]\d+)([+-]\d+)$", toast.toplevel.geometry())
    return int(m.group(2))


# --------------------------------------------------------------------------- #
# construction / options
# --------------------------------------------------------------------------- #

def test_show_toast_returns_handle(root):
    t = ToastNotification("T", "M", position=(5, 50, "se"))
    handle = t.show_toast()
    root.update_idletasks()
    assert handle is t
    t.hide()


def test_show_emits_no_deprecation_warning(root):
    """show_toast() used to inject legacy `overrideredirect` -> a warning/show."""
    t = ToastNotification("T", "M", position=(5, 50, "se"))
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        t.show_toast()
        root.update_idletasks()
    assert t.kwargs.get("override_redirect") is True
    assert "overrideredirect" not in t.kwargs
    t.hide()


def test_legacy_iconfont_warns_and_is_ignored(root):
    with pytest.warns(DeprecationWarning):
        t = ToastNotification("T", "M", iconfont="Segoe UI Symbol", position=(5, 50, "se"))
    assert "iconfont" not in t.kwargs  # not forwarded to the Toplevel
    t.show_toast()
    root.update_idletasks()
    t.hide()


def test_bad_position_anchor_raises(root):
    with pytest.raises(ValueError):
        ToastNotification("T", "M", position=(5, 50, "middle"))


def test_bad_position_length_raises(root):
    with pytest.raises(ValueError):
        ToastNotification("T", "M", position=(5, 50))


# --------------------------------------------------------------------------- #
# icon (font glyph, not a PUA char)
# --------------------------------------------------------------------------- #

def test_icon_renders_via_font_engine(root):
    t = ToastNotification("T", "M", bootstyle="info", position=(5, 50, "se"))
    t.show_toast()
    root.update_idletasks()
    icon_lbl = t.container.winfo_children()[0]
    # apply_icon augments the widget with a derived "Icon..." style; the glyph is
    # in the style's image element, and there is no PUA text on the label.
    assert "Icon" in str(icon_lbl.cget("style"))
    assert icon_lbl.cget("text") == ""
    assert t.icon == _DEFAULT_ICON
    t.hide()


def test_empty_icon_suppressed(root):
    t = ToastNotification("T", "M", icon="", position=(5, 50, "se"))
    t.show_toast()
    root.update_idletasks()
    icon_lbl = t.container.winfo_children()[0]
    assert "Icon" not in str(icon_lbl.cget("style"))
    t.hide()


# --------------------------------------------------------------------------- #
# lifecycle: timers, idempotent hide
# --------------------------------------------------------------------------- #

def test_hide_cancels_duration_timer(root):
    t = ToastNotification("T", "M", duration=10000, position=(5, 50, "se"))
    t.show_toast()
    root.update_idletasks()
    assert t._duration_id is not None
    t.hide()
    assert t._hidden is True
    assert t._duration_id is None  # cancelled


def test_hide_is_idempotent(root):
    t = ToastNotification("T", "M", position=(5, 50, "se"))
    t.show_toast()
    root.update_idletasks()
    t.hide()
    t.hide()  # must not raise
    assert t._hidden is True


def test_hide_before_show_is_safe(root):
    t = ToastNotification("T", "M", position=(5, 50, "se"))
    t.hide()  # never shown -> no raise
    assert t._hidden is True


# --------------------------------------------------------------------------- #
# stack manager
# --------------------------------------------------------------------------- #

def test_two_toasts_stack_without_overlap(root):
    t1 = ToastNotification("One", "first", position=(5, 50, "se"))
    t2 = ToastNotification("Two", "second", position=(5, 50, "se"))
    t1.show_toast()
    t2.show_toast()
    root.update_idletasks()

    y1, y2 = _ypos(t1), _ypos(t2)
    assert y1 != y2  # non-overlapping
    # The offset basis must be the height the toast actually OCCUPIES on screen,
    # which is floored to its minsize -- not the (smaller) requested height.
    # Regression: using winfo_reqheight() alone undershot the floor and the
    # stacked toasts overlapped by the minsize/reqheight gap.
    assert t1._height >= t1.toplevel.minsize()[1]
    assert t1._height == max(t1.toplevel.winfo_reqheight(), t1.toplevel.minsize()[1])
    # t2 is offset from t1 by its full occupied height + the gap, so the two
    # windows are exactly one gap apart (no overlap). Geometry is now absolute
    # positive coords and the SE stack grows upward (y decreases), so compare the
    # magnitude of the gap between the two.
    expected = t1._height + t1._scaled_gap()
    assert abs(abs(y2 - y1) - expected) <= 2
    assert len(_TOAST_STACK._corners["se"]) == 2
    t1.hide()
    t2.hide()


def test_horizontal_anchor_toasts_still_stack(root):
    # 'e'/'w' anchors are vertically centered; concurrent ones must still get the
    # stack offset (regression: the absolute-geometry rewrite applied the offset
    # only in the n/s branches, so e/w toasts overlapped).
    t1 = ToastNotification("A", "a", position=(5, 0, "e"))
    t2 = ToastNotification("B", "b", position=(5, 0, "e"))
    t1.show_toast()
    t2.show_toast()
    root.update_idletasks()
    assert _ypos(t1) != _ypos(t2)  # not overlapping
    expected = t1._height + t1._scaled_gap()
    assert abs(abs(_ypos(t2) - _ypos(t1)) - expected) <= 2
    t1.hide()
    t2.hide()


def test_dismiss_reflows_remaining(root):
    t1 = ToastNotification("One", "first", position=(5, 50, "se"))
    t2 = ToastNotification("Two", "second", position=(5, 50, "se"))
    t1.show_toast()
    t2.show_toast()
    root.update_idletasks()
    base = _ypos(t1)

    t1.hide()  # removes t1 + reflows the corner
    root.update_idletasks()
    # t2 slides up into t1's (base) slot
    assert abs(abs(_ypos(t2)) - abs(base)) <= 2
    assert len(_TOAST_STACK._corners["se"]) == 1
    t2.hide()


def test_toast_leaves_registry_on_hide(root):
    t = ToastNotification("T", "M", position=(5, 50, "se"))
    t.show_toast()
    root.update_idletasks()
    assert t in _TOAST_STACK._corners["se"]
    t.hide()
    assert t not in _TOAST_STACK._corners.get("se", [])


def test_separate_corners_are_independent(root):
    t1 = ToastNotification("A", "a", position=(5, 50, "se"))
    t2 = ToastNotification("B", "b", position=(5, 50, "ne"))
    t1.show_toast()
    t2.show_toast()
    root.update_idletasks()
    # each is the sole (unoffset) toast in its own corner
    assert len(_TOAST_STACK._corners["se"]) == 1
    assert len(_TOAST_STACK._corners["ne"]) == 1
    assert _TOAST_STACK.offset_for(t1) == 0
    assert _TOAST_STACK.offset_for(t2) == 0
    t1.hide()
    t2.hide()