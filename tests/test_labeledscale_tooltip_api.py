"""API tests for the LabeledScale + ToolTip normalization (widget review PR 6).

Headless (uses the shared ``root`` fixture from conftest). Covers the
LabeledScale double-init/compound/idle-leak fixes + DoubleVar backing, and the
ToolTip binding-lifecycle + self-release + configure/cget surface. Popup-visual
behavior (actual placement) is only structurally checked here.
"""
import tkinter

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.widgets.labeledscale import LabeledScale
from ttkbootstrap.widgets.tooltip import ToolTip


@pytest.fixture(scope="module", autouse=True)
def _clear_image_cache_after_module():
    """Release the scale-thumb images these tests add to the process-global
    ``Style._image_cache``.

    LabeledScale creates a Scale whose (default -> primary) thumb populates the
    same cache key that ``widget_styles/test_image_cache`` asserts is freshly
    rendered; clearing on teardown keeps this module from imposing a test-order
    dependency on that suite.
    """
    yield
    try:
        Style.get_instance().clear_image_cache()
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# LabeledScale
# --------------------------------------------------------------------------- #

def test_compound_bottom_constructs(root):
    """`compound` was dead-on-arrival (forwarded to Frame -> TclError)."""
    ls = LabeledScale(root, from_=0, to=10, compound="bottom")
    ls.pack()
    root.update_idletasks()
    assert ls._label_top is False


def test_compound_top_default(root):
    ls = LabeledScale(root, from_=0, to=10)
    assert ls._label_top is True


def test_single_frame_init_children(root):
    """One Frame init -> exactly the scale, value label, and height dummy."""
    ls = LabeledScale(root, from_=0, to=10)
    ls.pack()
    root.update_idletasks()
    # label + scale + dummy label
    assert len(ls.winfo_children()) == 3


def test_value_roundtrip(root):
    ls = LabeledScale(root, from_=0, to=10)
    ls.value = 7
    assert ls.value == 7


def test_doublevar_fractional_and_label_format(root):
    """DoubleVar honors fractions; the label renders cleanly (`:g`)."""
    ls = LabeledScale(root, from_=0, to=10)
    ls.pack()
    ls.value = 3.5
    root.update_idletasks()
    assert ls.value == 3.5
    assert ls.label["text"] == "3.5"      # fractional shown
    ls.value = 4.0
    root.update_idletasks()
    assert ls.label["text"] == "4"        # whole value has no ".0"


def test_explicit_variable_respected(root):
    var = ttk.DoubleVar(value=2)
    ls = LabeledScale(root, from_=0, to=10, variable=var)
    assert ls.value == 0  # ctor sets the var to from_
    ls.value = 5
    assert var.get() == 5


def test_destroy_with_pending_idle_is_safe(root):
    """A queued after_idle(adjust_label) must not fire into a dead widget."""
    ls = LabeledScale(root, from_=0, to=10)
    ls.pack()
    ls._adjust()            # schedules an after_idle
    ls.destroy()            # must cancel it
    root.update_idletasks()  # flush idle queue -> would raise if not cancelled
    assert ls.scale is None


# --------------------------------------------------------------------------- #
# ToolTip
# --------------------------------------------------------------------------- #

def test_binding_does_not_clobber_existing_handler(root):
    """add='+' binds: a pre-existing <Enter> handler still fires."""
    btn = ttk.Button(root, text="x")
    btn.pack()
    hits = []
    btn.bind("<Enter>", lambda e: hits.append(1), add="+")
    ToolTip(btn, text="tip")
    btn.event_generate("<Enter>")
    root.update_idletasks()
    assert hits == [1]


def test_two_tooltips_coexist(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    t1 = ToolTip(btn, text="one")
    t2 = ToolTip(btn, text="two")
    assert t1._funcids and t2._funcids
    assert t1._funcids != t2._funcids


def test_destroy_is_idempotent_and_unbinds(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    tip = ToolTip(btn, text="tip")
    tip.destroy()
    assert tip._funcids == {}
    tip.destroy()  # idempotent -- must not raise


def test_self_release_on_widget_destroy(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    tip = ToolTip(btn, text="tip")
    btn.destroy()            # <Destroy> -> tip.destroy()
    root.update_idletasks()
    assert tip._funcids == {}


def test_invalid_position_raises(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    with pytest.raises(ValueError):
        ToolTip(btn, position="sideways")


def test_configure_invalid_position_raises(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    tip = ToolTip(btn, text="tip")
    with pytest.raises(ValueError):
        tip.configure(position="nope")


def test_configure_cget_roundtrip(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    tip = ToolTip(btn, text="one")
    tip.configure(text="two", delay=500)
    assert tip.cget("text") == "two"
    assert tip["delay"] == 500
    tip["text"] = "three"
    assert tip["text"] == "three"


def test_cget_unknown_option_raises(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    tip = ToolTip(btn, text="tip")
    with pytest.raises(ValueError):
        tip.cget("nonsense")


def test_show_tip_after_widget_destroyed_is_noop(root):
    btn = ttk.Button(root, text="x")
    btn.pack()
    tip = ToolTip(btn, text="tip")
    # simulate an orphaned timer: drop the popup guard, kill the widget
    btn.destroy()
    tip.show_tip()           # must be a no-op, not an error
    assert tip.toplevel is None


def test_configure_reconfigures_live_popup(root):
    """A visible popup's label updates in place on configure()."""
    btn = ttk.Button(root, text="x")
    btn.pack()
    root.update_idletasks()
    tip = ToolTip(btn, text="one")
    try:
        tip.show_tip()
        root.update_idletasks()
    except tkinter.TclError:
        pytest.skip("cannot realize a tooltip Toplevel headlessly here")
    if tip._label is None:
        pytest.skip("tooltip popup not realized headlessly")
    tip.configure(text="updated")
    assert tip._label.cget("text") == "updated"
    tip.hide_tip()
    assert tip.toplevel is None