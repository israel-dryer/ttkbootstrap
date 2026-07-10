"""Surface-color grammar + delivery tests (2.0 surface-color, PR 2).

Surface rides INSIDE the bootstyle string as an `@<surface>` token (spaces are
the recommended separator: `"@primary success ghost"`), producing a leading
`@<surface>.` segment on the style name. Covers the token round-trip, the
default-surface no-regression invariant, the family gate, case-normalization,
the lenient handling of a custom `@` style name on the theme walk, the
accent-vs-card foreground rule, and end-to-end delivery on the button family.
"""
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK
from ttkbootstrap.style.bootstyle import (
    Bootstyle,
    _build_ttkstyle_name,
    _classify_style_name,
    _classify_tokens,
)


def _lookup(app, style_name, option):
    return app.tk.call("ttk::style", "lookup", style_name, f"-{option}")


# --- grammar units -------------------------------------------------------- #

def test_classify_tokens_extracts_surface():
    color, modifier, base, orient, surface = _classify_tokens(
        "@primary success ghost"
    )
    assert (color, modifier, surface) == ("success", "ghost", "primary")


def test_surface_token_is_position_free():
    # classified by content, so the @token may appear anywhere
    for s in ("@primary success ghost", "success ghost @primary",
              "success @primary ghost"):
        c, m, b, o, surf = _classify_tokens(s)
        assert (c, m, surf) == ("success", "ghost", "primary"), s


def test_build_name_prefixes_non_default_surface():
    assert (
        _build_ttkstyle_name("info", "ghost", "", "button", "primary")
        == "@primary.info.Ghost.TButton"
    )


def test_build_name_default_surface_is_unchanged():
    base = _build_ttkstyle_name("info", "ghost", "", "button")
    assert base == "info.Ghost.TButton"
    assert _build_ttkstyle_name("info", "ghost", "", "button", "") == base
    assert _build_ttkstyle_name("info", "ghost", "", "button", "background") == base


def test_classify_style_name_extracts_surface():
    color, modifier, base, orient, surface = _classify_style_name(
        "@primary.info.Ghost.TButton"
    )
    assert (color, modifier, base, orient, surface) == (
        "info", "ghost", "button", "", "primary"
    )


def test_name_round_trips_through_classify():
    name = _build_ttkstyle_name("success", "link", "", "button", "card")
    color, modifier, base, orient, surface = _classify_style_name(name)
    assert _build_ttkstyle_name(color, modifier, orient, base, surface) == name


# --- end-to-end delivery (surface as a bootstyle @token) ------------------ #

def test_default_surface_names_unchanged(root):
    """No @surface token -> exactly the pre-surface style names."""
    assert ttk.Button(root, bootstyle="ghost").cget("style") == "Ghost.TButton"
    assert (
        ttk.Button(root, bootstyle="info ghost").cget("style")
        == "info.Ghost.TButton"
    )
    assert (
        ttk.Button(root, bootstyle="primary outline").cget("style")
        == "primary.Outline.TButton"
    )


def test_ghost_ghosts_on_accent_surface(root):
    """`@primary ghost` paints the accent, not the app background."""
    style = Style.get_instance()
    btn = ttk.Button(root, bootstyle="@primary ghost")
    assert btn.cget("style") == "@primary.Ghost.TButton"
    assert _lookup(root, btn.cget("style"), "background") == style.colors.primary


def test_accent_surface_flips_foreground(root):
    """On an accent surface the default ghost text flips to the contrast color."""
    b = StyleBuilderTTK(build=False)
    btn = ttk.Button(root, bootstyle="@primary ghost")
    assert _lookup(root, btn.cget("style"), "foreground") == b.on_color(
        b.colors.primary
    )


def test_card_surface_keeps_soft_foreground(root):
    """A near-background `card` surface keeps the theme's soft fg (no hardening)."""
    b = StyleBuilderTTK(build=False)
    btn = ttk.Button(root, bootstyle="@card ghost")
    assert btn.cget("style") == "@card.Ghost.TButton"
    assert _lookup(root, btn.cget("style"), "foreground") == str(b.colors.fg)
    assert _lookup(root, btn.cget("style"), "background") == b.card_surface()


def test_link_and_outline_track_the_surface(root):
    style = Style.get_instance()
    lk = ttk.Button(root, bootstyle="@success link")
    assert lk.cget("style") == "@success.Link.TButton"
    assert _lookup(root, lk.cget("style"), "background") == style.colors.success

    ol = ttk.Button(root, bootstyle="@success primary outline")
    assert ol.cget("style") == "@success.primary.Outline.TButton"
    assert _lookup(root, ol.cget("style"), "background") == style.colors.success


def test_surface_token_is_case_normalized(root):
    assert (
        ttk.Button(root, bootstyle="@Primary ghost").cget("style")
        == "@primary.Ghost.TButton"
    )


def test_frame_ignores_surface_family_gate(root):
    """Frames are surface producers -- an @surface token is gated out."""
    frm = ttk.Frame(root, bootstyle="@card primary")
    assert "@" not in frm.cget("style")


def test_unknown_surface_warns(root):
    with pytest.warns(UserWarning):
        btn = ttk.Button(root, bootstyle="@bogus ghost")
    assert btn.cget("style") == "Ghost.TButton"


def test_bare_at_token_is_silent(root):
    """A stray bare '@' carries no surface and must not warn."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")   # any warning fails
        btn = ttk.Button(root, bootstyle="@primary @ ghost")
    assert btn.cget("style") == "@primary.Ghost.TButton"


def test_capitalized_surface_only_typo_warns(root):
    """A leading-@ typo with no other token stays on the loud bootstyle path."""
    with pytest.warns(UserWarning):
        btn = ttk.Button(root, bootstyle="@Primaryy")
    assert btn.cget("style") == "TButton"


def test_custom_at_style_name_is_lenient_on_theme_walk(root):
    """A custom `@`-prefixed style name must NOT warn/raise on re-resolve."""
    from ttkbootstrap.style._compat import (
        is_bootstyle_strict,
        set_bootstyle_strict,
    )
    lbl = ttk.Label(root)
    lbl.configure(style="@brand.TLabel")   # custom style name carrying '@'
    with warnings.catch_warnings():
        warnings.simplefilter("error")     # any warning becomes an error
        Bootstyle.update_ttk_widget_style(lbl)   # simulate theme-walk repaint
    # ... and strict mode must not raise on the lenient style-name dialect
    prior = is_bootstyle_strict()
    set_bootstyle_strict(True)
    try:
        Bootstyle.update_ttk_widget_style(lbl)  # no exception
    finally:
        set_bootstyle_strict(prior)


def test_surface_style_is_theme_reactive(root):
    style = Style.get_instance()
    style.theme_use("bootstrap-light")
    btn = ttk.Button(root, bootstyle="@primary ghost")
    light_bg = _lookup(root, btn.cget("style"), "background")

    style.theme_use("bootstrap-dark")
    dark_bg = _lookup(root, btn.cget("style"), "background")

    assert btn.cget("style") == "@primary.Ghost.TButton"  # name stable
    assert light_bg != dark_bg  # repainted for the new theme's primary


# --- configure-time (the bootstyle string is authoritative) --------------- #

def test_configure_bootstyle_sets_and_clears_surface(root):
    btn = ttk.Button(root, bootstyle="@card ghost")
    assert btn.cget("style") == "@card.Ghost.TButton"
    # a bootstyle without an @token clears the surface (string is authoritative)
    btn.configure(bootstyle="ghost")
    assert btn.cget("style") == "Ghost.TButton"
    # and can move it to another surface
    btn.configure(bootstyle="@primary success ghost")
    assert btn.cget("style") == "@primary.success.Ghost.TButton"
