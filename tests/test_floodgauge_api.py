"""Headless API tests for the normalized Floodgauge widget (2.0 PR 4).

Covers the ConfigureDelegationMixin adoption (5-tuple specs + cget parity),
DoubleVar value backing, live mode/orient, the maximum=0 zero-range guard, the
value-vs-display split (cget("text") no longer returns the mask output), the
value property, and the start() signature realignment. Nothing here runs an
animation loop for long -- start() is immediately stopped.
"""
import warnings

import pytest

from ttkbootstrap import IntVar
from ttkbootstrap.widgets.floodgauge import Floodgauge


# --- configure/cget parity via the mixin -----------------------------------

def test_configure_query_returns_5_tuple(root):
    fg = Floodgauge(root)
    for name in ("value", "maximum", "mode", "orient", "mask", "text",
                 "font", "bootstyle", "length", "thickness",
                 "variable", "textvariable"):
        spec = fg.configure(name)
        assert isinstance(spec, tuple)
        assert len(spec) == 5, f"{name} spec not a 5-tuple: {spec}"
        assert spec[0] == name


def test_cget_parity_for_every_option(root):
    fg = Floodgauge(root, maximum=50, value=10, bootstyle="info",
                    length=180, thickness=30)
    assert fg.cget("maximum") == 50
    assert fg.cget("value") == 10
    assert fg.cget("bootstyle") == "info"
    assert fg.cget("length") == 180
    assert fg.cget("thickness") == 30
    assert fg.cget("mode") == "determinate"
    assert fg.cget("orient") == "horizontal"
    # variable/textvariable render as their Tcl names
    assert fg.cget("variable") == str(fg.variable)
    assert fg.cget("textvariable") == str(fg.textvariable)


def test_mode_and_orient_in_keys(root):
    fg = Floodgauge(root)
    keys = fg.keys()
    for name in ("value", "maximum", "mode", "orient", "mask",
                 "length", "thickness"):
        assert name in keys


# --- DoubleVar value backing -----------------------------------------------

def test_value_is_float_and_not_truncated(root):
    fg = Floodgauge(root, maximum=100)
    fg.configure(value=33.3)
    assert fg.cget("value") == pytest.approx(33.3)
    assert fg.value == pytest.approx(33.3)


def test_value_property_get_set(root):
    fg = Floodgauge(root, maximum=100)
    fg.value = 42.5
    assert fg.value == pytest.approx(42.5)
    assert fg.cget("value") == pytest.approx(42.5)


def test_external_intvar_still_binds(root):
    iv = IntVar(value=5)
    fg = Floodgauge(root, variable=iv, maximum=10)
    assert fg.cget("value") == 5
    iv.set(7)
    assert fg.value == 7


# --- live mode / orient ----------------------------------------------------

def test_mode_is_live(root):
    fg = Floodgauge(root, mode="determinate")
    fg.configure(mode="indeterminate")
    assert fg.cget("mode") == "indeterminate"


def test_orient_swaps_width_height(root):
    fg = Floodgauge(root, orient="horizontal", length=200, thickness=40)
    fg.pack()
    root.update_idletasks()
    fg.configure(orient="vertical")
    root.update_idletasks()
    assert fg.cget("orient") == "vertical"
    # vertical: width=thickness, height=length
    assert fg.winfo_reqwidth() == 40
    assert fg.winfo_reqheight() == 200


# --- zero-range guard ------------------------------------------------------

def test_maximum_zero_does_not_crash(root):
    fg = Floodgauge(root, maximum=0, value=0)
    fg.pack()
    root.update_idletasks()  # forces a _draw with maximum == 0
    # reconfigure to 0 at runtime + a step must not raise
    fg.configure(value=5)
    fg.configure(maximum=0)
    fg.step()
    root.update_idletasks()


# --- value-vs-display split (the cget("text") fix) -------------------------

def test_mask_does_not_clobber_text(root):
    fg = Floodgauge(root, maximum=100, mask="{}%", text="Loading", value=25)
    fg.pack()
    root.update_idletasks()
    # A mask formats the *display* only; the user's text is untouched.
    assert fg.cget("text") == "Loading"
    fg.configure(value=60)
    root.update_idletasks()
    assert fg.cget("text") == "Loading"


def test_text_roundtrips_without_mask(root):
    fg = Floodgauge(root, maximum=100)
    fg.configure(text="Done")
    assert fg.cget("text") == "Done"


# --- start() realignment ---------------------------------------------------

def test_start_new_interval_form(root):
    fg = Floodgauge(root, mode="indeterminate")
    fg.pack()
    root.update_idletasks()
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # new form must NOT warn
        fg.start(30)
    assert fg._running is True
    fg.stop()
    assert fg._running is False


def test_start_legacy_form_warns_and_runs(root):
    fg = Floodgauge(root, mode="indeterminate")
    fg.pack()
    root.update_idletasks()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fg.start(8, 20)
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert fg._running is True
    assert fg._step_size == 8
    fg.stop()


def test_start_legacy_keyword_warns(root):
    fg = Floodgauge(root, mode="determinate")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fg.start(step_size=3, interval=40)
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert fg._step_size == 3
    fg.stop()


def test_start_unknown_keyword_raises(root):
    fg = Floodgauge(root)
    with pytest.raises(TypeError):
        fg.start(bogus=1)
    fg.stop()

# --- property/accessor consistency (2.0 property-consistency pass) ----------

def test_options_backed_privately_and_read_via_cget(root):
    """The option backing fields are private; the canonical read is cget."""
    fg = Floodgauge(root, maximum=100)
    for opt in ("maximum", "mode", "orient", "mask", "font", "length", "thickness"):
        assert opt not in vars(fg), f"{opt!r} is still a bare public instance attr"
        assert hasattr(fg, f"_{opt}")  # private backing field
        fg.cget(opt)                   # round-trips through configure/cget
    # The value handle and Variable handles remain public by design.
    assert isinstance(fg.value, float)
    assert fg.variable is not None and fg.textvariable is not None


def test_legacy_bare_option_attrs_are_deprecated_not_removed(root):
    """Pre-2.0 bare-attribute read/write still works but warns (non-breaking)."""
    fg = Floodgauge(root, maximum=100)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert fg.maximum == 100                 # deprecated read
        fg.maximum = 50                          # deprecated write -> configure
    cats = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert len(cats) >= 2                         # one for the read, one for the write
    assert fg.cget("maximum") == 50              # the write actually took effect
