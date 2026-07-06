"""Tests for the resolved-view `Colors` and `RampColor` ramp addressing (E, PR E1).

`Colors` stores each color as a `RampColor` -- a `str` subclass that behaves
exactly like the plain hex string everywhere it is used today, and additionally
addresses its own 50-950 tint/shade ramp (`c.primary[300]`). These tests pin
both the drop-in-`str` behavior and the new ramp addressing, with no catalog or
visual change.
"""
import pytest

from ttkbootstrap.style.theme import (
    Colors,
    RampColor,
    _color_ramp,
    _normalize_color,
)


RAMP_STOPS = tuple(range(50, 1000, 50))

# The 16 constructor colors, in signature order.
SAMPLE = (
    "#2780e3",  # primary
    "#7E8081",  # secondary
    "#3fb618",  # success
    "#9954bb",  # info
    "#ff7518",  # warning
    "#ff0039",  # danger
    "#F8F9FA",  # light
    "#373A3C",  # dark
    "#ffffff",  # bg
    "#373a3c",  # fg
    "#7e8081",  # selectbg
    "#ffffff",  # selectfg
    "#ced4da",  # border
    "#373a3c",  # inputfg
    "#fdfdfe",  # inputbg
    "#efefef",  # active
)


def make_colors():
    return Colors(*SAMPLE)


def test_rampcolor_is_a_drop_in_str():
    c = RampColor("#2780e3")
    assert isinstance(c, str)
    assert c == "#2780e3"
    assert c.upper() == "#2780E3"
    # ordinary str indexing/slicing is untouched (char indices, slices)
    assert c[0] == "#"
    assert c[1:] == "2780e3"
    assert list(c[:3]) == ["#", "2", "7"]


def test_rampcolor_addresses_its_ramp():
    c = RampColor("#0d6efd")
    ramp = _color_ramp("#0d6efd")
    assert c[500] == ramp[500] == "#0d6efd"
    assert c[300] == ramp[300]
    assert c[700] == ramp[700]
    # every valid stop resolves to the same value the ramp holds
    assert all(c[stop] == ramp[stop] for stop in RAMP_STOPS)


def test_rampcolor_anchor_is_500_normalized():
    # a short/named color still anchors correctly and normalizes on lookup
    assert RampColor("#abc")[500] == _normalize_color("#abc")
    assert RampColor("white")[500] == "#ffffff"


def test_non_ramp_int_index_falls_through_to_str():
    c = RampColor("#2780e3")
    # 6 is a normal char index, not a ramp stop
    assert c[6] == "3"
    # an out-of-range non-stop int raises like a plain str would
    with pytest.raises(IndexError):
        _ = c[42]


def test_colors_wraps_every_field_as_rampcolor():
    c = make_colors()
    for label in Colors.label_iter():
        value = c.get(label)
        assert isinstance(value, RampColor), label
        # equality with the authored string is preserved byte-for-byte
    assert c.primary == "#2780e3"
    assert c.inputbg == "#fdfdfe"


def test_colors_attr_and_get_are_ramp_addressable():
    c = make_colors()
    assert c.primary[500] == _normalize_color("#2780e3")
    assert c.primary[300] == _color_ramp("#2780e3")[300]
    assert c.get("info")[700] == _color_ramp("#9954bb")[700]


def test_colors_ramp_returns_full_mapping():
    c = make_colors()
    ramp = c.ramp("primary")
    assert tuple(ramp) == RAMP_STOPS
    assert ramp == _color_ramp("#2780e3")
    # the mapping is immutable
    with pytest.raises(TypeError):
        ramp[500] = "#000000"


def test_colors_set_wraps_and_addresses():
    c = make_colors()
    c.set("custom", "#0d6efd")
    assert isinstance(c.get("custom"), RampColor)
    assert c.get("custom")[300] == _color_ramp("#0d6efd")[300]


def test_colors_still_usable_as_plain_strings():
    # the values must remain interchangeable with str in every legacy use
    c = make_colors()
    assert f"bg is {c.bg}" == "bg is #ffffff"
    assert c.fg.lstrip("#") == "373a3c"
    assert {c.primary, c.secondary} == {"#2780e3", "#7E8081"}


def test_live_theme_colors_are_ramp_addressable(root):
    # integration: the active theme's Colors resolves ramp stops end-to-end
    colors = root.style.colors
    assert colors.primary[300] == _color_ramp(colors.primary)[300]
    assert colors.primary == str(colors.primary)
