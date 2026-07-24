"""Value-token grammar + delivery tests.

A *value token* extends the two color-bearing slots of a bootstyle with raw hex
(`#rgb`/`#rrggbb`) and ramp-addressed roles (`role[stop]`). It is legal in the
color slot (`#2f2f2f`, `primary[300]`) and the surface slot (`@#ff0000`,
`@light[200]`); everything else in the grammar stays a closed vocabulary. Covers
the pure validators, tokenizer classification (both dialects), the loud-fail
contract on malformed tokens, resolution through `Colors.get`, the frozen-hex vs
theme-reactive-ramp behavior on a theme switch, and Tcl-safety of a style name
carrying brackets and hashes (build/map/layout/lookup/switch).
"""
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    canonical_value_token,
    is_hex_token,
    is_value_token,
    looks_like_value_token,
    normalize_hex_token,
    parse_ramp_token,
)
from ttkbootstrap.style._compat import set_bootstyle_strict
from ttkbootstrap.style.bootstyle import (
    _build_ttkstyle_name,
    _classify_style_name,
    _classify_tokens,
    _looks_like_style_name,
)


def _lookup(app, style_name, option):
    return app.tk.call("ttk::style", "lookup", style_name, f"-{option}")


def _other_theme(app):
    """A registered theme other than the default light/dark pair.

    Theme switching is session-global state, so these tests deliberately avoid
    the default `bootstrap-light`/`bootstrap-dark` pair other suites rely on and
    switch to an unrelated family whose primary anchor differs from the current
    one (enough to prove a ramp token re-resolves).
    """
    style = app.style
    current = style.colors.primary[400]
    for name in sorted(style.theme_names()):
        if name.startswith("bootstrap"):
            continue
        definition = style._theme_definitions.get(name)
        if definition and definition.colors.primary[400] != current:
            return name
    raise AssertionError("no alternate theme with a distinct primary found")


# --- pure validators ------------------------------------------------------- #

@pytest.mark.parametrize("token", ["#2f2f2f", "#FFF", "#f00", "#ABCDEF"])
def test_valid_hex_tokens(token):
    assert is_hex_token(token)
    assert is_value_token(token)


@pytest.mark.parametrize("token", ["#ff00zz", "#ff", "#fffff", "2f2f2f", "#12345g"])
def test_invalid_hex_tokens(token):
    assert not is_hex_token(token)


def test_hex_normalization_expands_and_lowercases():
    assert normalize_hex_token("#F00") == "#ff0000"
    assert normalize_hex_token("#AbCdEf") == "#abcdef"
    assert canonical_value_token("#F00") == "#ff0000"


@pytest.mark.parametrize(
    "token,expected",
    [
        ("primary[300]", ("primary", 300)),
        ("light[200]", ("light", 200)),
        ("background[200]", ("background", 200)),
        ("DANGER[950]", ("danger", 950)),
    ],
)
def test_valid_ramp_tokens(token, expected):
    assert parse_ramp_token(token) == expected
    assert is_value_token(token)


@pytest.mark.parametrize(
    "token",
    [
        "primary[123]",   # not a 50-step stop
        "primary[0]",     # below the ramp
        "primary[1000]",  # above the ramp
        "primaryy[300]",  # unknown role
        "neutral[300]",   # neutral is a policy, not a ramp anchor
        "primary[300",    # malformed
        "[300]",          # no role
        "primary[]",      # no stop
    ],
)
def test_invalid_ramp_tokens(token):
    assert parse_ramp_token(token) is None
    assert not is_value_token(token)


def test_looks_like_value_token_flags_attempts():
    # both valid and malformed attempts route to value-token validation
    assert looks_like_value_token("#ff00zz")
    assert looks_like_value_token("primary[123]")
    assert looks_like_value_token("primary[300")
    assert not looks_like_value_token("primary")
    assert not looks_like_value_token("outline")


# --- tokenizer classification --------------------------------------------- #

def test_classify_tokens_hex_accent():
    color, modifier, base, orient, surface = _classify_tokens("#2f2f2f")
    assert color == "#2f2f2f"


def test_classify_tokens_normalizes_short_hex():
    color, *_ = _classify_tokens("#f00")
    assert color == "#ff0000"


def test_classify_tokens_ramp_accent():
    color, *_ = _classify_tokens("primary[300]")
    assert color == "primary[300]"


def test_classify_tokens_value_surface_and_accent():
    color, modifier, base, orient, surface = _classify_tokens(
        "@#ff0000 #ffffff"
    )
    assert (color, surface) == ("#ffffff", "#ff0000")


def test_classify_tokens_ramp_surface_and_semantic_accent():
    color, modifier, base, orient, surface = _classify_tokens(
        "@background[200] danger"
    )
    assert (color, surface) == ("danger", "background[200]")


def test_value_tokens_are_position_free():
    for s in ("#ffffff @#ff0000", "@#ff0000 #ffffff"):
        color, _, _, _, surface = _classify_tokens(s)
        assert (color, surface) == ("#ffffff", "#ff0000"), s


def test_classify_style_name_recovers_value_tokens():
    color, modifier, base, orient, surface = _classify_style_name(
        "@#ff0000.#ffffff.TButton"
    )
    assert (color, surface, base) == ("#ffffff", "#ff0000", "button")


def test_classify_style_name_recovers_ramp_tokens():
    color, modifier, base, orient, surface = _classify_style_name(
        "@background[200].primary[300].TLabel"
    )
    assert (color, surface, base) == ("primary[300]", "background[200]", "label")


def test_value_token_name_round_trips_through_classify():
    name = _build_ttkstyle_name("#ffffff", "", "", "button", "#ff0000")
    assert name == "@#ff0000.#ffffff.TButton"
    color, modifier, base, orient, surface = _classify_style_name(name)
    assert _build_ttkstyle_name(color, modifier, orient, "button", surface) == name


def test_dotless_value_token_bootstyle_is_not_a_style_name():
    # a #hex / bracket bootstyle with no class segment stays on the loud path
    assert not _looks_like_style_name("#2f2f2f")
    assert not _looks_like_style_name("primary[300]")
    assert not _looks_like_style_name("@light[200]")
    # a built name (dotted) is still recognized as a style name
    assert _looks_like_style_name("#2f2f2f.TButton")


# --- loud-fail contract ---------------------------------------------------- #

def test_malformed_value_token_warns(root):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ttk.Button(root, text="x", bootstyle="#ff00zz")
    assert any("ff00zz" in str(w.message) for w in caught)


def test_malformed_ramp_stop_warns(root):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ttk.Button(root, text="y", bootstyle="primary[123]")
    assert any("123" in str(w.message) for w in caught)


def test_strict_mode_raises_on_malformed_value_token(root):
    set_bootstyle_strict(True)
    try:
        with pytest.raises(Exception):
            ttk.Button(root, text="z", bootstyle="#ff00zz")
    finally:
        set_bootstyle_strict(False)


# --- resolution through Colors.get ---------------------------------------- #

def test_colors_get_resolves_hex(root):
    colors = root.style.colors
    assert colors.get("#2f2f2f") == "#2f2f2f"
    assert colors.get("#f00") == "#ff0000"


def test_colors_get_resolves_ramp(root):
    colors = root.style.colors
    assert colors.get("primary[500]") == colors.primary[500]
    assert colors.get("primary[300]") == colors.primary[300]
    assert colors.get("background[200]") == colors.bg[200]


def test_colors_get_unknown_still_none(root):
    assert root.style.colors.get("not_a_role") is None


# --- delivery: build / lookup --------------------------------------------- #

def test_hex_accent_button_builds_and_paints(root):
    btn = ttk.Button(root, text="hex", bootstyle="#2f2f2f")
    style_name = btn.cget("style")
    assert style_name == "#2f2f2f.TButton"
    assert _lookup(root, style_name, "background") == "#2f2f2f"


def test_ramp_accent_button_builds_and_paints(root):
    btn = ttk.Button(root, text="ramp", bootstyle="primary[300]")
    style_name = btn.cget("style")
    assert style_name == "primary[300].TButton"
    assert _lookup(root, style_name, "background") == root.style.colors.primary[300]


def test_value_surface_and_accent_deliver(root):
    btn = ttk.Button(root, text="both", bootstyle="@#ff0000 #ffffff")
    style_name = btn.cget("style")
    assert style_name == "@#ff0000.#ffffff.TButton"
    assert _lookup(root, style_name, "background") == "#ffffff"


# --- theme-switch behavior ------------------------------------------------- #

def test_ramp_is_theme_reactive_hex_is_frozen(root):
    style = root.style
    hex_btn = ttk.Button(root, text="hex", bootstyle="#2f2f2f")
    ramp_btn = ttk.Button(root, text="ramp", bootstyle="primary[400]")
    hex_name, ramp_name = hex_btn.cget("style"), ramp_btn.cget("style")

    ramp_before = _lookup(root, ramp_name, "background")
    style.theme_use(_other_theme(root))
    root.update_idletasks()

    # ramp re-resolves against the new theme's primary anchor
    assert _lookup(root, ramp_name, "background") != ramp_before
    assert _lookup(root, ramp_name, "background") == style.colors.primary[400]
    # hex stays frozen
    assert _lookup(root, hex_name, "background") == "#2f2f2f"


# --- Tcl safety: brackets + hashes survive every engine path -------------- #

def test_bracketed_hashed_style_name_is_tcl_safe(root):
    style = root.style
    btn = ttk.Button(root, text="tcl", bootstyle="@light[200] #abcdef")
    name = btn.cget("style")
    assert name == "@light[200].#abcdef.TButton"

    # configure / map lookups (already exercised at build); layout + element
    # enumeration must also accept the bracketed/hashed name without a TclError.
    layout = root.tk.call("ttk::style", "layout", name)
    assert layout  # non-empty layout returned
    assert _lookup(root, name, "background") == "#abcdef"

    # theme switch repaints the mounted widget through the same name
    style.theme_use(_other_theme(root))
    root.update_idletasks()
    assert btn.cget("style") == name
    assert _lookup(root, name, "background") == "#abcdef"