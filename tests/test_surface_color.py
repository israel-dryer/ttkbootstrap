"""Surface-color resolver tests (2.0 surface-color, PR 1).

Covers `StyleBuilderTTK.resolve_surface` / `card_surface`: the named-neutral +
accent surface dialects, the default = application background, mode-aware `card`
derivation, theme-reactivity, and the unknown-token warn-and-fallback. Raw-hex
surfaces are deferred to a later PR and are expected to warn here.
"""
import pytest

from ttkbootstrap.style.builders_ttk import StyleBuilderTTK
from ttkbootstrap.style.builders.utils import neutral_fill


def _builder():
    """A non-building builder bound to the current theme (introspection only)."""
    return StyleBuilderTTK(build=False)


def test_default_surface_is_background(root):
    b = _builder()
    assert b.resolve_surface() == b.colors.bg
    assert b.resolve_surface(None) == b.colors.bg
    assert b.resolve_surface("") == b.colors.bg
    assert b.resolve_surface("background") == b.colors.bg


def test_card_surface_differs_from_background(root):
    b = _builder()
    card = b.resolve_surface("card")
    assert card != b.colors.bg
    assert card == b.card_surface()


def test_chrome_surface_sits_between_background_and_card(root):
    """The elevation scale is background < chrome < card: chrome is a distinct,
    subtler step than card (both mode-aware raises of the background)."""
    b = _builder()
    chrome = b.resolve_surface("chrome")
    assert chrome == b.chrome_surface()
    assert chrome != b.colors.bg          # distinct from the base
    assert chrome != b.resolve_surface("card")   # a different rung than card


def test_accent_surface_resolves_to_color(root):
    b = _builder()
    assert b.resolve_surface("primary") == b.colors.primary
    assert b.resolve_surface("danger") == b.colors.danger
    assert b.resolve_surface("light") == b.colors.light
    assert b.resolve_surface("dark") == b.colors.dark


def test_neutral_surface_is_the_neutral_fill(root):
    b = _builder()
    assert b.resolve_surface("neutral") == neutral_fill(b)


def test_unknown_surface_warns_and_falls_back(root):
    b = _builder()
    with pytest.warns(UserWarning):
        value = b.resolve_surface("bogus-surface")
    assert value == b.colors.bg


def test_unknown_surface_raises_in_strict_mode(root):
    """Strict mode turns the unknown-surface warning into a hard error, matching
    how the resolver treats an unknown bootstyle token."""
    from ttkbootstrap.style._compat import (
        is_bootstyle_strict,
        set_bootstyle_strict,
    )

    b = _builder()
    prior = is_bootstyle_strict()
    set_bootstyle_strict(True)
    try:
        with pytest.raises(ValueError):
            b.resolve_surface("bogus-surface")
    finally:
        set_bootstyle_strict(prior)


def test_raw_hex_surface_is_deferred(root):
    """A raw hex is not yet a valid surface -- it warns and falls back."""
    b = _builder()
    with pytest.warns(UserWarning):
        value = b.resolve_surface("#123456")
    assert value == b.colors.bg


def test_card_surface_is_theme_reactive(root):
    """`card` re-resolves off the new background on a theme switch."""
    style = root.style
    style.theme_use("bootstrap-light")
    light_card = _builder().resolve_surface("card")

    style.theme_use("bootstrap-dark")
    dark_card = _builder().resolve_surface("card")

    # different backgrounds -> different card surfaces (the fixture restores the
    # original theme on teardown).
    assert light_card != dark_card
