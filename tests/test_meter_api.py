"""Headless tests for the 2.0 Meter API normalization (widget review PR 2).

Covers the snake_case option names, the configure-delegation round-trip
(including options that used to be construction-only or non-gettable), the
`DoubleVar` float backing + `value` property, single-seam scaling (no
double-scale on round-trip), and the legacy-kwarg / legacy-attribute
deprecation shims.
"""
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.widgets.meter import Meter


def _make(root, **kw):
    return Meter(root, **kw)


# --------------------------------------------------------------------------
# construction + basic round-trip
# --------------------------------------------------------------------------

def test_construct_with_snake_case_names(root):
    m = _make(
        root, amount_used=25, amount_total=200, meter_type="semi",
        subtext="cpu", meter_size=180, meter_thickness=12,
    )
    assert m.cget("amount_used") == 25
    assert m.cget("amount_total") == 200
    assert m.cget("meter_type") == "semi"
    assert m.cget("subtext") == "cpu"


def test_cget_and_configure_round_trip(root):
    m = _make(root)
    m.configure(amount_used=40, wedge_size=5, step_size=2)
    assert m.cget("amount_used") == 40
    assert m.cget("wedge_size") == 5
    assert m.cget("step_size") == 2
    assert m["amount_used"] == 40  # item access agrees


def test_amount_format_is_reconfigurable(root):
    # amount_format used to be construction-only (no configure/cget branch).
    m = _make(root, amount_format="{:.0f}")
    assert m.cget("amount_format") == "{:.0f}"
    m.configure(amount_format="{:.2f}")
    assert m.cget("amount_format") == "{:.2f}"


def test_configure_query_returns_five_tuple(root):
    m = _make(root, meter_size=200)
    spec = m.configure("meter_size")
    assert len(spec) == 5
    assert spec[0] == "meter_size"
    assert spec[4] == 200  # logical value


# --------------------------------------------------------------------------
# value property + float backing
# --------------------------------------------------------------------------

def test_value_property_get_and_set(root):
    m = _make(root, amount_used=10)
    assert m.value == 10
    m.value = 33
    assert m.value == 33
    assert m.cget("amount_used") == 33


def test_double_var_keeps_fractional_value(root):
    m = _make(root, amount_used=2.5, amount_format="{:.1f}")
    assert m.value == 2.5
    assert m.amount_used_display_var.get() == "2.5"


# --------------------------------------------------------------------------
# single-seam scaling: no double-scale on round-trip
# --------------------------------------------------------------------------

def test_meter_size_does_not_double_scale_on_round_trip(root):
    m = _make(root, meter_size=200)
    logical = m.cget("meter_size")
    assert logical == 200
    m.configure(meter_size=logical)
    assert m.cget("meter_size") == 200  # stable, no growth
    m.configure(meter_size=m.cget("meter_size"))
    assert m.cget("meter_size") == 200


def test_meter_thickness_round_trips_logical(root):
    m = _make(root, meter_thickness=10)
    assert m.cget("meter_thickness") == 10
    m.configure(meter_thickness=m.cget("meter_thickness"))
    assert m.cget("meter_thickness") == 10


# --------------------------------------------------------------------------
# legacy deprecation shims
# --------------------------------------------------------------------------

def test_legacy_kwarg_works_and_warns(root):
    with pytest.warns(DeprecationWarning):
        m = Meter(root, amountused=15, metertype="semi")
    assert m.cget("amount_used") == 15
    assert m.cget("meter_type") == "semi"


def test_legacy_configure_option_works_and_warns(root):
    m = _make(root)
    with pytest.warns(DeprecationWarning):
        m.configure(amountused=55)
    assert m.cget("amount_used") == 55


def test_legacy_attribute_works_and_warns(root):
    m = _make(root, amount_used=7)
    with pytest.warns(DeprecationWarning):
        var = m.amountusedvar
    assert var is m.amount_used_var
    assert var.get() == 7


def test_unknown_attribute_still_raises(root):
    m = _make(root)
    with pytest.raises(AttributeError):
        _ = m.definitely_not_a_meter_attribute


# --------------------------------------------------------------------------
# import stays warning-free
# --------------------------------------------------------------------------

def test_import_is_warning_free():
    import importlib
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        importlib.import_module("ttkbootstrap")
        importlib.import_module("ttkbootstrap.widgets.meter")


# --------------------------------------------------------------------------
# label handles: clean *_label names + deprecated old spellings
# (property-consistency pass)
# --------------------------------------------------------------------------

def test_label_handles_have_clean_names(root):
    """The subtext/text-position Label handles use collision-free *_label names."""
    m = _make(root, subtext="hi", text_left="L", text_right="R")
    for attr in ("subtext_label", "text_left_label",
                 "text_right_label", "text_center_label"):
        assert isinstance(getattr(m, attr), ttk.Label)
    # the option and the handle are now distinct: cget -> string, attr -> Label
    assert m.cget("subtext") == "hi"
    assert isinstance(m.subtext_label, ttk.Label)


def test_legacy_label_attrs_are_deprecated(root):
    """Old handle spellings still resolve (to the renamed Label) but warn."""
    m = _make(root, subtext="hi")
    for old, new in (("subtext", "subtext_label"),
                     ("textleft", "text_left_label"),
                     ("textright", "text_right_label"),
                     ("textcenter", "text_center_label")):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            got = getattr(m, old)
        assert got is getattr(m, new)
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)
