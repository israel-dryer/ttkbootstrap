"""Tests for the semantic-anchor `Theme` model and curated catalog (E, PR E2).

Covers the schema->16-key derivation, the curated built-in catalog, the legacy
16-key adapter, and the opt-in `install_legacy_themes()` migration path. The
`inputbg` hue-preservation check is the explicit regression guard for the fix
Workstream E was chartered to land (a themed dark field must not desaturate).
"""
import warnings

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style.theme import (
    Colors,
    Theme,
    _accent_on_color,
    _color_ramp,
    _color_to_hsl,
    _normalize_color,
    _SOLID_STOP,
)
from ttkbootstrap.themes.builtin import BOOTSTRAP, CURATED_THEMES
from ttkbootstrap.themes.legacy import theme_from_legacy_dict
from ttkbootstrap.themes.standard import STANDARD_THEMES


def sample_theme():
    return Theme(
        name="sample",
        primary="#0d6efd", success="#198754", info="#0dcaf0",
        warning="#ffc107", danger="#dc3545",
        light=dict(background="#ffffff", foreground="#212529"),
        dark=dict(background="#212529", foreground="#f8f9fa"),
    )


# --- Theme generation -------------------------------------------------------

def test_theme_generates_light_and_dark_definitions():
    defs = sample_theme().to_definitions()
    assert [d.name for d in defs] == ["sample-light", "sample-dark"]
    assert [d.type for d in defs] == ["light", "dark"]
    assert all(isinstance(d.colors, Colors) for d in defs)


def test_theme_with_one_block_yields_one_definition():
    t = Theme(
        name="lightonly",
        primary="#0d6efd", success="#198754", info="#0dcaf0",
        warning="#ffc107", danger="#dc3545",
        light=dict(background="#ffffff", foreground="#212529"),
    )
    defs = t.to_definitions()
    assert [d.name for d in defs] == ["lightonly-light"]


def test_theme_validates_missing_anchor_and_block():
    with pytest.raises(ValueError, match="accent anchor"):
        Theme(name="x", primary="#0d6efd",
              light=dict(background="#fff", foreground="#000")).to_definitions()
    with pytest.raises(ValueError, match="background.*foreground"):
        Theme(name="x", primary="#0d6efd", success="#1", info="#1",
              warning="#1", danger="#1",
              light=dict(background="#fff")).to_definitions()


# --- Derivation (schema -> 16 Colors) ---------------------------------------

def test_solids_use_per_mode_ramp_step():
    light = sample_theme()._definition("light").colors
    dark = sample_theme()._definition("dark").colors
    assert light.primary == _color_ramp("#0d6efd")[_SOLID_STOP["light"]["primary"]]
    assert dark.primary == _color_ramp("#0d6efd")[_SOLID_STOP["dark"]["primary"]]
    # warning/info stay at [500] on light
    assert light.warning == _color_ramp("#ffc107")[500]


def test_secondary_derives_from_neutral_unless_colored():
    uncolored = sample_theme()._definition("light").colors
    assert uncolored.secondary == _color_ramp("#adb5bd")[700]  # neutral, light stop

    colored = Theme(
        name="s", primary="#0d6efd", success="#198754", info="#0dcaf0",
        warning="#ffc107", danger="#dc3545", secondary="#8045e5",
        light=dict(background="#ffffff", foreground="#212529"),
    )._definition("light").colors
    assert colored.secondary == _color_ramp("#8045e5")[_SOLID_STOP["light"]["primary"]]


def test_light_and_dark_accents_come_from_neutral_ramp():
    colors = sample_theme()._definition("light").colors
    assert colors.light == _color_ramp("#adb5bd")[100]
    assert colors.dark == _color_ramp("#adb5bd")[800]


def test_selectbg_is_neutral_not_the_accent():
    # selectbg doubles as the neutral trough/dark-border base in the builders,
    # so it must stay neutral (never the primary accent).
    colors = sample_theme()._definition("light").colors
    assert colors.selectbg == _color_ramp("#adb5bd")[700]  # neutral, light stop
    assert colors.selectbg != colors.primary
    assert colors.selectfg == _accent_on_color(colors.selectbg)


def test_light_inputbg_equals_bg_dark_lifts_off_bg():
    light = sample_theme()._definition("light").colors
    dark = sample_theme()._definition("dark").colors
    assert light.inputbg == _normalize_color("#ffffff")  # light: field == surface
    assert dark.inputbg != dark.bg  # dark: field lifts off the surface


def test_dark_inputbg_preserves_theme_hue_and_saturation():
    """Regression guard for the deferred fix: a themed dark field must lift off
    the background WITHOUT desaturating toward gray/white."""
    t = Theme(
        name="vaporish", primary="#6e40c0", success="#3af180", info="#1da2f2",
        warning="#ffbd05", danger="#e34b54",
        dark=dict(background="#190831", foreground="#32fbe2"),
    )
    colors = t._definition("dark").colors
    bg_h, bg_s, bg_l = _color_to_hsl(colors.bg)
    in_h, in_s, in_l = _color_to_hsl(colors.inputbg)
    assert in_h == bg_h                 # identical hue
    assert in_s >= bg_s * 0.7           # saturation retained (not washed to gray)
    assert in_l > bg_l                  # genuinely lifted


# --- Curated catalog --------------------------------------------------------

def test_curated_catalog_shape():
    assert len(CURATED_THEMES) == 15
    names = {t.name for t in CURATED_THEMES}
    assert {"bootstrap", "vapor", "minty", "pulse", "united", "sandstone"} <= names


def test_curated_catalog_registered_and_default_present(root):
    names = set(root.style.theme_names())
    for family in CURATED_THEMES:
        assert f"{family.name}-light" in names
        assert f"{family.name}-dark" in names
    assert "bootstrap-light" in names  # DEFAULT_THEME


def test_all_bootstyle_keywords_resolve_in_a_curated_theme(root):
    style = root.style
    style.theme_use("catppuccin-dark")
    colors = style.colors
    for keyword in ("primary", "secondary", "success", "info",
                    "warning", "danger", "light", "dark"):
        value = colors.get(keyword)
        assert value and value.startswith("#")


# --- Legacy adapter + install_legacy_themes ---------------------------------

def test_legacy_adapter_preserves_identity_regenerates_plumbing():
    spec = STANDARD_THEMES["darkly"]
    legacy = spec["colors"]
    d = theme_from_legacy_dict("darkly", spec)
    c = d.colors
    # authored identity preserved verbatim
    for key in ("primary", "secondary", "success", "info", "warning",
                "danger", "light", "dark", "bg", "fg", "selectbg",
                "selectfg", "inputfg"):
        assert c.get(key) == legacy[key], key
    # buggy plumbing regenerated off bg
    assert c.inputbg != legacy["inputbg"]
    assert c.border != legacy["border"]
    assert d.type == "dark"


def test_user_theme_spec_builds_and_registers(root):
    # A USER_THEME_SPECS-style anchor spec (what ttkcreator persists) builds a
    # Theme and registers usable light/dark variants -- the engine's user-theme
    # load path.
    style = root.style
    spec = {
        "primary": "#2780e3", "success": "#3fb618", "info": "#9954bb",
        "warning": "#ff7518", "danger": "#ff0039",
        "secondary": None, "neutral": "#7e8081",
        "light": {"background": "#ffffff", "foreground": "#373a3c"},
        "dark": {"background": "#222222", "foreground": "#f8f9fa"},
    }
    before = set(style._theme_names)
    try:
        for definition in Theme(name="spectest", **spec).to_definitions():
            style.register_theme(definition)
        assert {"spectest-light", "spectest-dark"} <= style._theme_names
        style.theme_use("spectest-dark")
        assert style.theme.name == "spectest-dark"
        assert style.colors.bg == "#222222"
    finally:
        for name in list(style._theme_names):
            if name not in before:
                style._theme_names.discard(name)
                style._theme_definitions.pop(name, None)
                style._theme_styles.pop(name, None)
                style._theme_objects.pop(name, None)
        style.theme_use("bootstrap-light")


def test_from_existing_overrides_and_rejects_unknown_tokens():
    derived = Theme.from_existing(BOOTSTRAP, name="acme", primary="#ff5722")
    assert derived.name == "acme"
    assert derived.primary == "#ff5722"
    assert derived.success == BOOTSTRAP.success  # inherited
    with pytest.raises(ValueError, match="Unknown Theme token"):
        Theme.from_existing(BOOTSTRAP, name="acme", bogus="x")


def test_legacy_theme_use_lazy_registers_then_bulk_opt_in(root):
    """Slice 1: theme_use on a legacy name lazily registers just that theme
    (warns once) instead of hard-stopping; install_legacy_themes() bulk-registers
    the rest."""
    style = root.style
    before = set(style._theme_names)
    assert "darkly" not in before
    try:
        # Slice 1: a legacy name via theme_use no longer hard-stops -- it
        # lazily adapts+registers that ONE theme and switches to it.
        with pytest.warns(DeprecationWarning, match="legacy"):
            style.theme_use("darkly")
        assert style.theme.name == "darkly"
        assert "darkly" in style._theme_names
        # only that one name was registered, not the whole legacy catalog
        assert "superhero" not in style._theme_names
        # bulk opt-in registers the rest
        with pytest.warns(DeprecationWarning):
            ttk.install_legacy_themes()
        # idempotent: a second call adds nothing new
        count = len(style._theme_names)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ttk.install_legacy_themes()
        assert len(style._theme_names) == count
        # every legacy name is now registered and usable
        assert set(STANDARD_THEMES) <= style._theme_names
        style.theme_use("superhero")
        assert style.theme.name == "superhero"
    finally:
        # restore the shared session registry for later tests
        for name in list(style._theme_names):
            if name not in before:
                style._theme_names.discard(name)
                style._theme_definitions.pop(name, None)
                style._theme_styles.pop(name, None)
                style._theme_objects.pop(name, None)
        style.theme_use("bootstrap-light")
