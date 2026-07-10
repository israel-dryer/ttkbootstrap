"""Grammar tests for the canonical bootstyle vocabulary (2.0 Workstream D, D1).

These lock the D1 contract: a single closed vocabulary, a real tokenizer that
classifies each token into a fixed slot, loud failure (warn by default, raise in
strict mode) on unknown/duplicate tokens, tuple normalization, and a round-trip
proving every registered builder key is expressible in the grammar.
"""
from typing import get_args

import importlib.util
import pathlib
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap import constants as C
from ttkbootstrap.style import _compat
from ttkbootstrap.style.bootstyle import (
    _classify_tokens,
    _infer_family,
    _build_ttkstyle_name,
)
from ttkbootstrap.style.builders import load_builders
from ttkbootstrap.style.builders.registry import builder_keys, DEFAULT_VARIANT


@pytest.fixture(autouse=True)
def _reset_strict():
    """Keep strict-mode changes from leaking across tests."""
    before = _compat.is_bootstyle_strict()
    yield
    _compat.set_bootstyle_strict(before)


# --------------------------------------------------------------------------- #
# Single source of truth: Literals mirror the runtime vocab tuples
# --------------------------------------------------------------------------- #
def test_literals_match_vocab_tuples():
    assert set(get_args(C.BootColor)) == set(C.BOOTSTYLE_COLORS)
    assert set(get_args(C.BootType)) == set(C.BOOTSTYLE_MODIFIERS)
    assert set(get_args(C.BootBase)) == set(C.BOOTSTYLE_BASES)


def test_reclassification_fixed_the_audit():
    # `round` is now a modifier (was buildable but missing from BootType)...
    assert "round" in C.BOOTSTYLE_MODIFIERS
    # ...and toggle/toolbutton are base-types, not modifiers.
    assert "toggle" not in C.BOOTSTYLE_MODIFIERS
    assert "toolbutton" not in C.BOOTSTYLE_MODIFIERS
    assert set(C.BOOTSTYLE_BASES) == {"toggle", "toolbutton"}
    # the dead keywords are gone from every slot
    for slot in (
        C.BOOTSTYLE_COLORS, C.BOOTSTYLE_MODIFIERS,
        C.BOOTSTYLE_INTERNAL_MODIFIERS, C.BOOTSTYLE_FAMILIES,
    ):
        assert "focus" not in slot
        assert "input" not in slot


# --------------------------------------------------------------------------- #
# Tokenizer / classification
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "text, expected",
    [
        # (color, modifier, base, orient, surface)
        ("primary-outline", ("primary", "outline", "", "", "")),
        ("success-round-toggle", ("success", "round", "toggle", "", "")),
        ("info-striped", ("info", "striped", "", "", "")),
        ("primary", ("primary", "", "", "", "")),
        ("outline", ("", "outline", "", "", "")),
        ("toolbutton", ("", "", "toolbutton", "", "")),
        ("horizontal", ("", "", "", "horizontal", "")),
        ("danger-inverse", ("danger", "inverse", "", "", "")),
        # order-free input still classifies to the same slots
        ("outline-primary", ("primary", "outline", "", "", "")),
        # whitespace separator is accepted alongside the dash
        ("primary outline", ("primary", "outline", "", "", "")),
        # internal composite modifiers are valid tokens
        ("primary-meter", ("primary", "meter", "", "", "")),
        # a @surface token (2.0 surface-color), position-free
        ("@primary success ghost", ("success", "ghost", "", "", "primary")),
        ("success ghost @primary", ("success", "ghost", "", "", "primary")),
        ("@card ghost", ("", "ghost", "", "", "card")),
    ],
)
def test_classify_slots(text, expected):
    assert _classify_tokens(text) == expected


def test_sentinels_classify_to_nothing():
    assert _classify_tokens("default") == ("", "", "", "", "")
    assert _classify_tokens("") == ("", "", "", "", "")
    assert _classify_tokens("-primary-") == ("primary", "", "", "", "")


# --------------------------------------------------------------------------- #
# Loud failure: warn by default, raise in strict mode
# --------------------------------------------------------------------------- #
def test_unknown_token_is_silent_without_warn_flag():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert _classify_tokens("primaryy") == ("", "", "", "", "")


def test_unknown_token_warns():
    with pytest.warns(UserWarning, match="primaryy"):
        _classify_tokens("primaryy", warn=True)


def test_unknown_token_suggests_nearest():
    with pytest.warns(UserWarning, match="did you mean 'primary'"):
        _classify_tokens("primaryy", warn=True)


def test_unknown_token_strict_raises():
    _compat.set_bootstyle_strict(True)
    with pytest.raises(ValueError, match="primaryy"):
        _classify_tokens("primaryy", warn=True)


def test_duplicate_slot_warns():
    with pytest.warns(UserWarning, match="color"):
        _classify_tokens("primary-info", warn=True)


def test_strict_toggle_and_default():
    assert _compat.is_bootstyle_strict() is False
    _compat.set_bootstyle_strict(True)
    assert _compat.is_bootstyle_strict() is True
    _compat.set_bootstyle_strict(False)
    assert _compat.is_bootstyle_strict() is False


# --------------------------------------------------------------------------- #
# Name assembly (exact pre-2.0 casing preserved)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "args, expected",
    [
        (("primary", "outline", "", "button"), "primary.Outline.TButton"),
        (("success", "", "", "button"), "success.TButton"),
        (("", "", "", "treeview"), "Treeview"),
        (("", "striped", "horizontal", "progressbar"),
         "Striped.Horizontal.TProgressbar"),
        (("", "round", "", "toggle"), "Round.Toggle"),
        (("", "", "", "toplevel"), "Toplevel"),
    ],
)
def test_build_name(args, expected):
    assert _build_ttkstyle_name(*args) == expected


# --------------------------------------------------------------------------- #
# _compat.normalize_bootstyle
# --------------------------------------------------------------------------- #
def test_normalize_is_quiet_unless_warn_requested():
    # warn is opt-in per call; the resolver passes warn=True (D2), but a bare
    # normalize_bootstyle() call stays quiet.
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert _compat.normalize_bootstyle(("primary", "outline")) == \
            "primary-outline"
        assert _compat.normalize_bootstyle(["danger", "inverse"]) == \
            "danger-inverse"
        assert _compat.normalize_bootstyle("primary-outline") == \
            "primary-outline"
        assert _compat.normalize_bootstyle(None) == ""


def test_normalize_tuple_warns_when_asked():
    # D2 will flip the resolver's default to warn=True; the machinery is here.
    with pytest.warns(DeprecationWarning, match="tuple/list bootstyle"):
        assert _compat.normalize_bootstyle(
            ("primary", "outline"), warn=True
        ) == "primary-outline"


# --------------------------------------------------------------------------- #
# Registry round-trip: every built-in (variant, family) is expressible
# --------------------------------------------------------------------------- #
def test_every_registry_key_roundtrips():
    load_builders()
    keys = builder_keys()
    assert keys, "registry should be populated after load_builders()"
    for variant, family in keys:
        # family is a real vocabulary token...
        assert family in C.BOOTSTYLE_FAMILIES, (variant, family)
        # ...and the variant is either the default or a known modifier
        known_modifiers = set(C.BOOTSTYLE_MODIFIERS) | set(
            C.BOOTSTYLE_INTERNAL_MODIFIERS
        )
        assert variant == DEFAULT_VARIANT or variant in known_modifiers, (
            variant, family,
        )

        tokens = ["primary"]
        if variant != DEFAULT_VARIANT:
            tokens.append(variant)
        tokens.append(family)
        color, modifier, base, _, _ = _classify_tokens("-".join(tokens))
        assert color == "primary"
        assert base == family
        assert (modifier or DEFAULT_VARIANT) == variant


# --------------------------------------------------------------------------- #
# End-to-end: canonical strings resolve to real, existing ttk styles
# --------------------------------------------------------------------------- #
def test_infer_family_from_widget(root):
    btn = ttk.Button(root)
    assert _infer_family(btn) == "button"
    lf = ttk.Labelframe(root)
    assert _infer_family(lf) == "labelframe"  # not the "label" substring


@pytest.mark.parametrize(
    "factory, bootstyle, expected_name",
    [
        (ttk.Button, "primary-outline", "primary.Outline.TButton"),
        (ttk.Button, "success", "success.TButton"),
        (ttk.Checkbutton, "round-toggle", "Round.Toggle"),
        (ttk.Checkbutton, "toolbutton", "Toolbutton"),
        (ttk.Progressbar, "info-striped", None),
        (ttk.Label, "inverse", None),
        (ttk.Scrollbar, "primary", None),
    ],
)
def test_canonical_bootstyle_resolves_to_real_style(
    root, factory, bootstyle, expected_name
):
    widget = factory(root, bootstyle=bootstyle)
    applied = widget.cget("style")
    if expected_name is not None:
        assert applied == expected_name
    assert root.style.style_exists_in_theme(applied)


def test_invalid_pair_warns_for_our_widget(root):
    # `thin` is a real modifier, `button` a real family, but (thin, button) is
    # not a registered builder -> loud failure, not silent fallthrough. (A
    # Button is used rather than a Scale so this does not pre-populate the
    # session-global image cache the order-sensitive image-cache test checks.)
    with pytest.warns(UserWarning, match="thin-button"):
        ttk.Button(root, bootstyle="thin")


@pytest.mark.parametrize(
    "factory",
    [ttk.Label, ttk.Entry, ttk.Checkbutton, ttk.Radiobutton, ttk.Progressbar,
     ttk.Scale, ttk.Scrollbar, ttk.Combobox, ttk.Spinbox, ttk.Frame],
)
def test_neutral_on_non_button_family_falls_back_not_crashes(root, factory):
    # `neutral` is a real color but only the button-family recipes implement it
    # (constants.NEUTRAL_FAMILIES); on any other family it used to resolve to
    # Colors.get("neutral") -> None and crash the recipe mid-build. It must now
    # loud-fail and fall back to the family default, never crash construction.
    with pytest.warns(UserWarning, match="neutral-"):
        widget = factory(root, bootstyle="neutral")
    applied = widget.cget("style")
    assert applied  # a real, built default style, not an unusable fragment
    assert root.style.style_exists_in_theme(applied)


@pytest.mark.parametrize(
    "factory, bootstyle, expected_name",
    [
        (ttk.Button, "neutral", "neutral.TButton"),
        (ttk.Button, "neutral-outline", "neutral.Outline.TButton"),
        (ttk.Button, "neutral-toolbutton", "neutral.Toolbutton"),
        (ttk.Menubutton, "neutral", "neutral.TMenubutton"),
    ],
)
def test_neutral_still_builds_for_button_family(root, factory, bootstyle, expected_name):
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # button-family neutral must be warning-free
        widget = factory(root, bootstyle=bootstyle)
    assert widget.cget("style") == expected_name
    assert root.style.style_exists_in_theme(expected_name)


def test_valid_widget_construction_is_warning_free(root):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ttk.Button(root, bootstyle="primary")
        ttk.Checkbutton(root, bootstyle="success-round-toggle")
        ttk.Progressbar(root, bootstyle="info-striped")
        ttk.Label(root, bootstyle="inverse")


def test_composite_widgets_construct_without_tuple_warning(root):
    # Meter/DateEntry used the internal tuple form for their composite
    # sub-styles; D2 migrated them to canonical strings, so building them must
    # not trip the tuple DeprecationWarning.
    from ttkbootstrap.widgets import Meter, DateEntry
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        Meter(root, bootstyle="info", subtext_style="secondary").pack()
        DateEntry(root, bootstyle="primary").pack()
        root.update_idletasks()


def test_external_tuple_bootstyle_warns_and_resolves(root):
    # A genuine external tuple bootstyle still resolves, but now warns.
    with pytest.warns(DeprecationWarning, match="tuple/list bootstyle"):
        b = ttk.Button(root, bootstyle=("primary", "outline"))
    assert b.cget("style") == "primary.Outline.TButton"


# --------------------------------------------------------------------------- #
# D3: generated reference (BootStyle Literal + markdown) stays in sync
# --------------------------------------------------------------------------- #
def _load_reference_generator():
    path = (
        pathlib.Path(__file__).resolve().parents[1]
        / "tools"
        / "generate_bootstyle_reference.py"
    )
    spec = importlib.util.spec_from_file_location("_bootstyle_ref_gen", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bootstyle_literal_matches_registry():
    # The committed BootStyle Literal must equal the set derived live from the
    # vocabulary x registry, so adding a builder without regenerating fails.
    gen = _load_reference_generator()
    assert set(get_args(C.BootStyle)) == set(gen.canonical_bootstyles())


def test_bootstyle_reference_markdown_is_current():
    gen = _load_reference_generator()
    path = (
        pathlib.Path(__file__).resolve().parents[1]
        / "development"
        / "2_0_bootstyle_reference.md"
    )
    current = path.read_text(encoding="utf-8")
    expected = gen.reference_table_markdown() + "\n"
    assert current == expected, (
        "development/2_0_bootstyle_reference.md is stale; regenerate with "
        "`python tools/generate_bootstyle_reference.py`"
    )


def test_every_canonical_string_is_in_vocab():
    # Every generated canonical string classifies with no unknown-token warning,
    # i.e. it is composed entirely of closed-vocabulary tokens.
    gen = _load_reference_generator()
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        for s in gen.canonical_bootstyles():
            _classify_tokens(s, warn=True)
