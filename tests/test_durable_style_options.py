"""Headless tests for the durable style-options layer (#1238 / #1161).

A user's ``style.configure("TEntry", padding=3)`` must survive both a bootstyle
variant build and a theme switch, and a base-class override must fan out to its
variants. Colors are deliberately NOT recorded (they stay theme-reactive), and
builder writes must never be captured as user overrides.

The registry (``Style._user_options``) lives on the process-wide singleton, so an
autouse fixture resets it and rebuilds the base styles these tests touch, keeping
the leak out of the rest of the suite.
"""
import ast
import warnings
from pathlib import Path

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style.engine import DURABLE_STYLE_OPTIONS


def _lookup(app, style, option):
    return app.tk.call("ttk::style", "lookup", style, "-" + option)


def _padding(app, style):
    """First padding component as an int (ttk returns a scalar or a 1-tuple)."""
    val = _lookup(app, style, "padding")
    if isinstance(val, (tuple, list)):
        val = val[0]
    return int(val)


def _padding_tuple(app, style):
    """Full padding as a tuple of ints (ttk returns "6 5" or (6, 5))."""
    val = _lookup(app, style, "padding")
    if isinstance(val, str):
        val = val.split()
    return tuple(int(p) for p in val)


@pytest.fixture(autouse=True)
def _isolate_user_options(root):
    """Reset durable overrides and rebuild touched base styles after each test."""
    yield
    style = root.style
    style.reset_style_options()
    builder = style._get_builder()
    for variant, family in (
        ("default", "entry"),
        ("default", "panedwindow"),
        ("default", "button"),
        ("default", "notebook"),
    ):
        builder.build_style(variant, family, "default")


# --- #1238: overrides survive variant builds and theme switches ------------

def test_padding_survives_variant_build(root):
    root.style.configure("TEntry", padding=3)
    ttk.Entry(root, bootstyle="danger")  # builds danger.TEntry from scratch
    assert _padding(root, "danger.TEntry") == 3


def test_padding_survives_theme_switch(root):
    root.style.configure("TEntry", padding=3)
    root.style.theme_use("bootstrap-dark")
    assert _padding(root, "TEntry") == 3


def test_override_fans_out_to_new_variant_after_switch(root):
    root.style.configure("TEntry", padding=3)
    root.style.theme_use("bootstrap-dark")
    ttk.Entry(root, bootstyle="info")
    assert _padding(root, "info.TEntry") == 3


def test_base_class_override_reaches_variant(root):
    # never touch the base style itself; the variant must still inherit it
    root.style.configure("TButton", focusthickness=7)
    ttk.Button(root, bootstyle="success")
    assert int(_lookup(root, "success.TButton", "focusthickness")) == 7


def test_override_after_variant_exists_is_retroactive(root):
    ttk.Entry(root, bootstyle="warning")        # build the variant first
    root.style.configure("TEntry", padding=3)   # override afterwards
    assert _padding(root, "warning.TEntry") == 3


def test_most_specific_wins(root):
    root.style.configure("TEntry", padding=3)
    root.style.configure("danger.TEntry", padding=9)
    ttk.Entry(root, bootstyle="danger")
    assert _padding(root, "danger.TEntry") == 9


# --- #1161: the global Sash element ----------------------------------------

def test_sash_configure_emits_no_warning(root):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        root.style.configure("Sash", sashthickness=9)
    assert [str(w.message) for w in caught] == []


def test_sash_survives_panedwindow_build(root):
    root.style.configure("Sash", sashthickness=9)
    ttk.Panedwindow(root, bootstyle="success")  # recipe clobbers global Sash
    assert int(_lookup(root, "Sash", "sashthickness")) == 9


def test_sash_survives_theme_switch(root):
    root.style.configure("Sash", sashthickness=9)
    root.style.theme_use("bootstrap-dark")
    ttk.Panedwindow(root, bootstyle="info")
    assert int(_lookup(root, "Sash", "sashthickness")) == 9


# --- colors stay theme-reactive (not recorded) -----------------------------

def test_color_not_recorded(root):
    root.style.configure("TEntry", background="#123456")
    assert "TEntry" not in root.style._user_options


def test_mixed_configure_records_only_geometry(root):
    root.style.configure("TEntry", padding=3, background="#123456")
    assert root.style._user_options.get("TEntry") == {"padding": 3}


# --- builder writes are never captured -------------------------------------

def test_builder_writes_not_captured(root):
    # Build a fresh crop of styles with no user configure at all.
    ttk.Button(root, bootstyle="warning")
    ttk.Entry(root, bootstyle="warning")
    ttk.Panedwindow(root, bootstyle="warning")
    assert root.style._user_options == {}


def test_internal_default_styles_not_captured(root):
    # symbol.Link.TButton / tooltip.TLabel are framework writes in
    # create_default_style; they must not appear as user overrides.
    root.style.theme_use("bootstrap-dark")  # rebuilds create_default_style
    assert "symbol.Link.TButton" not in root.style._user_options
    assert "tooltip.TLabel" not in root.style._user_options


# --- reset -----------------------------------------------------------------

def test_reset_one_style_returns_recipe_default(root):
    root.style.configure("TEntry", padding=3)
    root.style.reset_style_options("TEntry")
    # a freshly built variant no longer inherits the override
    ttk.Entry(root, bootstyle="secondary")
    assert _padding(root, "secondary.TEntry") != 3


def test_reset_all_clears_registry(root):
    root.style.configure("TEntry", padding=3)
    root.style.configure("Sash", sashthickness=9)
    root.style.reset_style_options()
    assert root.style._user_options == {}


# --- computed layout is not stretched by a base-class override -------------
# `icon_only` padding is derived to make the control square, so it must win over
# a fanned-out `TButton` padding -- while a plain text+icon button still follows
# that override (the fix must not be over-broad).

def test_icon_only_button_stays_square_under_base_override(root):
    root.style.configure("TButton", padding=(40, 2))
    btn = ttk.Button(root, icon="calendar-week", icon_only=True)
    btn.pack()
    root.update_idletasks()
    assert btn.winfo_reqwidth() == btn.winfo_reqheight()


def test_text_icon_button_still_follows_base_override(root):
    root.style.configure("TButton", padding=(40, 2))
    btn = ttk.Button(root, text="Save", icon="calendar-week")
    btn.pack()
    root.update_idletasks()
    assert _padding_tuple(root, btn.cget("style")) == (40, 2)


# --- an all-states map must not mask a user configure ----------------------

def test_notebook_tab_padding_override_takes_effect(root):
    """The recipe used to map padding for every state, masking `configure`."""
    ttk.Notebook(root)
    root.style.configure("TNotebook.Tab", padding=(30, 20))
    assert _padding_tuple(root, "TNotebook.Tab") == (30, 20)


def test_notebook_tab_defaults_unchanged(root):
    """Dropping the redundant map must not change the default look."""
    ttk.Notebook(root)
    assert _padding_tuple(root, "TNotebook.Tab") == (6, 5)
    # bordercolor moved from the map into configure; it must still be set
    assert _lookup(root, "TNotebook.Tab", "bordercolor") != ""


# --- _effective_style_option and falsy values ------------------------------

def test_effective_option_preserves_falsy_value(root):
    """A real 0 is a value, not an absence -- it must not fall through."""
    root.style._build_configure("Probe.TFrame", borderwidth=0)
    assert root.style._effective_style_option(
        "Probe.TFrame", "borderwidth", "FALLBACK"
    ) == 0


def test_effective_option_returns_default_when_unset(root):
    assert root.style._effective_style_option(
        "Probe.TFrame", "nosuchoption", "FALLBACK"
    ) == "FALLBACK"


def test_effective_option_prefers_override_over_lookup(root):
    root.style._build_configure("Probe2.TFrame", borderwidth=3)
    root.style.configure("Probe2.TFrame", borderwidth=9)
    assert root.style._effective_style_option("Probe2.TFrame", "borderwidth") == 9


# --- the allowlist covers every geometry option recipes write --------------

# Options recipes write that are theme-derived (colors) or asset-driven, and so
# are deliberately NOT durable. Any recipe option outside this set OR the
# allowlist trips the guard below, forcing a deliberate classification.
_NON_DURABLE_RECIPE_OPTIONS = frozenset({
    # colors
    "background", "foreground", "bordercolor", "darkcolor", "lightcolor",
    "troughcolor", "focuscolor", "insertcolor", "fieldbackground",
    "selectbackground", "selectforeground", "arrowcolor", "indicatorcolor",
    "bg", "fg", "selectbg", "selectfg", "fieldbg", "space",
    "upperbordercolor", "lowerbordercolor",
    # asset / non-geometry
    "image", "compound",
})


def _recipe_configure_options():
    """Every option name passed to a `.configure(...)` call in the builders pkg."""
    pkg = Path(ttk.__file__).parent / "style" / "builders"
    found = set()
    for path in pkg.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not isinstance(func, ast.Attribute):
                continue
            if func.attr not in ("configure", "_build_configure"):
                continue
            for kw in node.keywords:
                if kw.arg and kw.arg not in ("style", "query_opt"):
                    found.add(kw.arg)
    return found


def test_allowlist_covers_all_recipe_geometry_options():
    written = _recipe_configure_options()
    unclassified = written - DURABLE_STYLE_OPTIONS - _NON_DURABLE_RECIPE_OPTIONS
    assert not unclassified, (
        "recipe configure() options neither durable nor classified non-durable "
        f"(add to DURABLE_STYLE_OPTIONS or _NON_DURABLE_RECIPE_OPTIONS): "
        f"{sorted(unclassified)}"
    )
