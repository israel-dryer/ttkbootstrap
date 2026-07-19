"""Tests for the `neutral` bootstyle color (2.0).

`neutral` is a derived, no-accent button color: a mode-aware raise of the surface
(bootstack's `elevate`) with a derived border and normal text. It is scoped to the
Button family (`NEUTRAL_FAMILIES`); the reference generator advertises it only
there. See `development/2_0_neutral_color_design.md`.
"""
import typing
import warnings

import ttkbootstrap as ttk
from ttkbootstrap.constants import BootStyle, NEUTRAL_FAMILIES


def _lookup(app, style, option):
    return str(app.tk.call("ttk::style", "lookup", style, f"-{option}")).lower()


def _brightness(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b


def test_neutral_solid_button_is_a_bordered_raised_surface(root):
    """`neutral` builds a filled, bordered button distinct from bg and any accent."""
    style = root.style
    ttk.Button(root, bootstyle="neutral")
    bg = _lookup(root, "neutral.TButton", "background")
    assert bg, "neutral button must configure a background"
    # it is a *raised surface*, not the raw page bg and not the primary accent
    assert bg != str(style.colors.bg).lower()
    assert bg != str(style.colors.primary).lower()
    # a distinct 1px border derived from the fill; at rest the clam dark/light
    # regions track the fill (the face), so bordercolor is the only edge color
    band = _lookup(root, "neutral.TButton", "bordercolor")
    assert band and band != bg, "neutral must have a distinct border"
    assert _lookup(root, "neutral.TButton", "darkcolor") == bg
    assert _lookup(root, "neutral.TButton", "lightcolor") == bg


def test_neutral_outline_button_sits_on_the_surface(root):
    """`neutral-outline` is flush with the surface: bg == theme bg, text == fg."""
    style = root.style
    ttk.Button(root, bootstyle="neutral-outline")
    assert _lookup(root, "neutral.Outline.TButton", "background") == str(style.colors.bg).lower()
    assert _lookup(root, "neutral.Outline.TButton", "foreground") == str(style.colors.fg).lower()
    assert _lookup(root, "neutral.Outline.TButton", "bordercolor")


def test_neutral_fill_elevates_in_the_right_direction(root):
    """The solid neutral fill darkens the surface in light themes, lightens in dark."""
    style = root.style

    style.theme_use("bootstrap-light")
    ttk.Button(root, bootstyle="neutral")
    light_fill = _brightness(_lookup(root, "neutral.TButton", "background"))
    assert light_fill < _brightness(str(style.colors.bg)), "light neutral should be darker than bg"

    style.theme_use("bootstrap-dark")
    dark_fill = _brightness(_lookup(root, "neutral.TButton", "background"))
    assert dark_fill > _brightness(str(style.colors.bg)), "dark neutral should be lighter than bg"


def test_neutral_resolves_without_warning(root):
    """`neutral` is a known token -- the loud tokenizer must not warn on it."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ttk.Button(root, bootstyle="neutral")
        ttk.Button(root, bootstyle="neutral-outline")


def test_bare_solid_toolbutton_is_neutral(root):
    """A bare `toolbutton` renders neutral -- its ON (selected) fill is the
    neutral raise, identical to `neutral toolbutton`, not the primary accent.

    This is the last button-family bare default to switch off primary (2.0):
    plain buttons and the outline toolbutton were already neutral by default.
    """
    style = root.style
    ttk.Checkbutton(root, text="x", bootstyle="toolbutton")
    ttk.Checkbutton(root, text="x", bootstyle="neutral toolbutton")

    def selected_fill(name):
        return {
            tuple(item[:-1]): str(item[-1]).lower()
            for item in style.map(name, "background")
        }[("selected", "!disabled")]

    bare = selected_fill("Toolbutton")
    assert bare == selected_fill("neutral.Toolbutton"), \
        "bare solid toolbutton must fill like `neutral toolbutton` when ON"
    assert bare != str(style.colors.primary).lower(), \
        "bare toolbutton ON must be the neutral raise, not the primary accent"


def test_neutral_scope_matches_neutral_families():
    """neutral is advertised only for the neutral families (button-family)."""
    assert NEUTRAL_FAMILIES == ("button", "menubutton", "toolbutton")
    canonical = set(typing.get_args(BootStyle))
    assert "neutral" in canonical
    assert "neutral outline" in canonical
    # toolbutton spells its chameleon base, so "neutral toolbutton" is advertised
    assert "neutral toolbutton" in canonical
    assert "neutral outline toolbutton" in canonical
    # but the base is not spelled for menubutton (you type "neutral" on a
    # Menubutton), and neutral is not a family for toggles
    for absent in ("neutral menubutton", "neutral round toggle"):
        assert absent not in canonical
