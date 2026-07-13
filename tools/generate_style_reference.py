#!/usr/bin/env python
"""Generate the Style Reference: one rST page per ttk-styled widget family.

The Style Reference is the deep, hand-styling surface the Widgets catalog links
to for native ttk widgets. Rather than hand-write it (and drift), this tool
derives it from the live ttk style engine:

- the **bootstyle -> ttk style name** mapping comes from the builder registry
  (`ttkbootstrap.style.builders.registry`) + the name assembler in
  `ttkbootstrap.style.bootstyle` -- the same sources the `bootstyle` reference
  generator uses;
- the **layout**, **configurable options**, and **supported states** come from
  live `ttk.Style` introspection (`layout`, `element_options`, `map`) of a
  representative built style.

Because the introspected values vary by Tcl/Tk version and OS, this is an
**offline** step (it needs a Tk display) that emits *committed* rST; RTD builds
the docs from the committed pages, never running this tool. The sync test
(`tests/test_bootstyle_grammar.py`) is deliberately *structural* -- it checks the
family set and the index, not the byte content -- so a Tk point-release can never
break CI.

Run it after changing the vocabulary, adding/removing a builder, or a recipe's
layout:

    python tools/generate_style_reference.py

It rewrites `docs/reference/style-reference/index.rst` and one
`docs/reference/style-reference/<family>.rst` per family.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from ttkbootstrap.constants import (  # noqa: E402
    BOOTSTYLE_BASES,
    BOOTSTYLE_COLORS,
    BOOTSTYLE_INTERNAL_MODIFIERS,
    NEUTRAL,
    NEUTRAL_FAMILIES,
)
from ttkbootstrap.style import bootstyle as _bs  # noqa: E402
from ttkbootstrap.style.builders import load_builders  # noqa: E402
from ttkbootstrap.style.builders.registry import (  # noqa: E402
    builder_keys,
    DEFAULT_VARIANT,
)

_OUT = _ROOT / "docs" / "reference" / "style-reference"
# Includable per-widget styling partials, pulled into each widget's API page
# under its "Styling options" section via ``.. include::``.
_PARTIAL_OUT = _ROOT / "docs" / "reference" / "api" / "_style"

# Families whose ttk style name carries an orientation segment; the reference
# documents the horizontal form (a note points at the vertical twin).
_ORIENT_FAMILIES = {"scale", "progressbar", "separator", "panedwindow", "floodgauge"}

# Families ttkbootstrap draws from pre-rendered image elements (keyed to the
# bootstyle color) rather than clam's drawing primitives. For these, most
# `style.configure` color/relief options are inert on the image parts, so the
# Configurable-options section carries a caveat. Value = (image-part phrase,
# has-a-text-label).
_IMAGE_FAMILIES = {
    "checkbutton": ("check indicator", True),
    "radiobutton": ("radio indicator", True),
    "toggle": ("toggle", True),
    "scale": ("trough and slider", False),
    "scrollbar": ("trough and thumb", False),
    "progressbar": ("bar", False),
}

# ttk widgets that accept a `-text` option, so the hand-styling example can add
# `text="Custom"` (the rest -- Scale, Frame, Treeview, ... -- reject it and would
# raise `unknown option "-text"` if the snippet were copied verbatim).
_TEXT_BEARING = {
    "button", "checkbutton", "radiobutton", "label", "labelframe",
    "menubutton", "toggle", "toolbutton",
}

# The single source of family metadata: family -> (blurb, group, example widget).
#   group -- "native" (a real ttk widget you construct directly) or "variant"
#     (chameleon variants + shipped-widget ttk styles); drives the index split.
#   example widget -- the ttk class the hand-styling snippet builds, or `None`
#     for a style that backs an internal/shipped widget (no direct constructor).
# Every family the registry produces must appear here (checked by _check_families).
_FAMILIES = {
    "button": ("A clickable action trigger.", "native", "Button"),
    "checkbutton": ("A labeled on/off checkbox.", "native", "Checkbutton"),
    "radiobutton": ("A labeled exclusive choice.", "native", "Radiobutton"),
    "combobox": ("A text entry with a drop-down list.", "native", "Combobox"),
    "entry": ("A single-line text input.", "native", "Entry"),
    "spinbox": ("A numeric entry with step arrows.", "native", "Spinbox"),
    "scale": ("A draggable value slider.", "native", "Scale"),
    "progressbar": ("A determinate or indeterminate progress bar.", "native", "Progressbar"),
    "scrollbar": ("A content scrollbar.", "native", "Scrollbar"),
    "separator": ("A thin dividing rule.", "native", "Separator"),
    "sizegrip": ("The resize handle in a window corner.", "native", "Sizegrip"),
    "label": ("A static text or image label.", "native", "Label"),
    "labelframe": ("A titled, bordered container.", "native", "Labelframe"),
    "frame": ("A plain container surface.", "native", "Frame"),
    "notebook": ("A tabbed-pane container.", "native", "Notebook"),
    "panedwindow": ("A split, draggable multi-pane container.", "native", "Panedwindow"),
    "treeview": ("A multi-column tree and table view.", "native", "Treeview"),
    "menubutton": ("A button that drops a menu.", "native", "Menubutton"),
    "toggle": ("A switch-style checkbutton (round or square).", "variant", "Checkbutton"),
    "toolbutton": ("A pressed/selected-state button for toolbars.", "variant", "Button"),
    "calendar": ("The date-picker calendar styling (used by DateEntry).", "variant", None),
    "floodgauge": ("The ttk progressbar style behind the legacy Floodgauge.", "variant", None),
}

_INDEX_INTRO = """\
Style Reference
===============

The deep hand-styling surface for the native ttk widgets ttkbootstrap themes.
For each widget family it documents the exact ``bootstyle`` -> ttk style-name
mapping, the element layout the widget is drawn from, the configurable options,
and the supported states -- everything you need to hand-tune a style with
``style.configure(...)`` and apply it with ``Widget(style=...)``.

.. note::

   These pages are **generated** from live ttk introspection by an offline
   ``tools/generate_style_reference.py`` step and committed as rST. Regenerate
   them after changing a widget recipe. This is the deep reference the
   :doc:`Widgets catalog </widgets/index>` links to for native widgets.
"""


# --------------------------------------------------------------------------- #
# Registry-derived family set (deterministic; no Tk root needed)
# --------------------------------------------------------------------------- #
def style_reference_families():
    """Return the sorted families that have a real ttk style recipe.

    This is the set of pages the Style Reference documents: every family with a
    registered builder (internal-only composite variants such as `meter`/`table`
    never introduce a new *family*, so no filtering is needed here -- each such
    family also carries a public `default` builder).
    """
    load_builders()
    return sorted({family for _variant, family in builder_keys()})


def _public_variants(family):
    """Sorted public variants registered for a family (`default` first)."""
    load_builders()
    variants = {
        variant
        for variant, fam in builder_keys()
        if fam == family and variant not in BOOTSTYLE_INTERNAL_MODIFIERS
    }
    ordered = [DEFAULT_VARIANT] if DEFAULT_VARIANT in variants else []
    ordered += sorted(variants - {DEFAULT_VARIANT})
    return ordered


def _orient_for(family):
    return "horizontal" if family in _ORIENT_FAMILIES else ""


def _bootstyle_and_name(color, variant, family):
    """Return the (canonical bootstyle string, ttk style name) for one key.

    The base-type is spelled only for the chameleon families (`toggle`/
    `toolbutton`); everywhere else it is inferred from the widget and omitted.
    """
    modifier = "" if variant == DEFAULT_VARIANT else variant
    base = family if family in BOOTSTYLE_BASES else ""
    orient = _orient_for(family)
    parts = [p for p in (color, modifier, base) if p]
    # spaces are the recommended bootstyle separator (dashes still parse).
    bootstyle = " ".join(parts)
    name = _bs._build_ttkstyle_name(color, modifier, orient, family)
    return bootstyle, name


def _class_token(family):
    """The ttk style-class suffix for a family, e.g. `TButton`, `Horizontal.TScale`.

    Derived from the representative resolved name by stripping the leading color
    segment, so it always tracks whatever the recipe actually emits.
    """
    _bootstyle, name = _bootstyle_and_name("primary", DEFAULT_VARIANT, family)
    prefix = "primary."
    return name[len(prefix):] if name.startswith(prefix) else name


# --------------------------------------------------------------------------- #
# Live ttk introspection (Tk root required; offline only)
# --------------------------------------------------------------------------- #
def _walk_layout(layout, depth=0):
    """Flatten a ttk layout into `(depth, element_name)` pairs, in tree order."""
    rows = []
    for element, opts in layout:
        rows.append((depth, element))
        if isinstance(opts, dict) and opts.get("children"):
            rows.extend(_walk_layout(opts["children"], depth + 1))
    return rows


def _build_representative(style, family):
    """Force the representative style (`primary`, default variant) to build.

    Styles are built lazily, so `style.map()` returns nothing until the recipe
    has run; introspecting an unbuilt name yields only the inherited layout with
    an empty state map. Build it first so options/states are real.
    """
    try:
        style._get_builder().build_style(DEFAULT_VARIANT, family, "primary")
    except Exception:
        pass


def _introspect(style, name):
    """Return (layout_rows, options, states) for a built style, best-effort.

    Any Tcl hiccup on one family degrades that section to empty rather than
    aborting the whole run.
    """
    try:
        layout = style.layout(name)
        layout_rows = _walk_layout(layout)
    except Exception:
        layout_rows = []

    options = set()
    for _depth, element in layout_rows:
        try:
            options.update(style.element_options(element))
        except Exception:
            pass

    states = set()
    try:
        mapping = style.map(name)
    except Exception:
        mapping = {}
    for option, specs in mapping.items():
        options.add(option)
        for spec in specs:
            # a statespec is (state..., value); every item but the last is a
            # state token (which may be negated, e.g. "!disabled").
            for token in spec[:-1]:
                states.update(str(token).split())

    return layout_rows, sorted(options), sorted(states)


# --------------------------------------------------------------------------- #
# rST rendering
# --------------------------------------------------------------------------- #
def _title(family):
    # match the ttk convention: `Treeview`, not `TTreeview`; title-case otherwise
    return family[:1].upper() + family[1:]


def _rule(text, char):
    return f"{text}\n{char * len(text)}"


def _bootstyle_table_rst(family):
    lines = [
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 50 50",
        "",
        "   * - ``bootstyle``",
        "     - ttk style name",
    ]
    for variant in _public_variants(family):
        bootstyle, name = _bootstyle_and_name("primary", variant, family)
        lines.append(f"   * - ``{bootstyle}``")
        lines.append(f"     - ``{name}``")
    return "\n".join(lines)


def _layout_rst(layout_rows):
    if not layout_rows:
        return "*(no ttk layout introspected)*"
    body = ["   " + "  " * depth + element for depth, element in layout_rows]
    return ".. code-block:: text\n\n" + "\n".join(body)


def _inline_list(items):
    return ", ".join(f"``{it}``" for it in items) if items else "*(none)*"


def _example_rst(family):
    widget = _FAMILIES[family][2]
    cls = _class_token(family)
    custom = f"my.{cls}"
    lines = [
        ".. code-block:: python",
        "",
        "   import ttkbootstrap as ttk",
        "",
        "   app = ttk.App()",
        "   style = app.style",
        "",
        f'   style.configure("{custom}", background="#3498db", foreground="white")',
    ]
    if widget is not None:
        # only text-bearing widgets accept `-text`; adding it to a Scale/Frame/
        # Treeview/... would raise `unknown option "-text"` when copied.
        text = 'text="Custom", ' if family in _TEXT_BEARING else ""
        lines.append(f'   ttk.{widget}(app, {text}style="{custom}").pack(padx=8, pady=8)')
        lines += ["", "   app.mainloop()"]
    else:
        lines += [
            "",
            "   # This style backs an internal/shipped widget rather than a",
            "   # directly-constructed ttk widget; configure the style class above.",
        ]
    return "\n".join(lines)


def _style_body_parts(style, family, uc):
    """Return the styling subsections for one family, ruled with underline `uc`.

    Shared by the standalone Style Reference page (``uc="-"``) and the includable
    per-widget partial (``uc="~"``) so their wording can never drift.
    """
    _bootstyle, rep_name = _bootstyle_and_name("primary", DEFAULT_VARIANT, family)
    _build_representative(style, family)
    layout_rows, options, states = _introspect(style, rep_name)

    # count is not spelled out (it is derived from BOOTSTYLE_COLORS and the list
    # follows immediately) so the prose can never drift from the vocabulary.
    colors = ", ".join(f"``{c}``" for c in BOOTSTYLE_COLORS if c != NEUTRAL)
    neutral_note = (
        f" ``{NEUTRAL}`` also applies here."
        if family in NEUTRAL_FAMILIES
        else f" ``{NEUTRAL}`` does not apply to this family."
    )
    orient_note = ""
    if family in _ORIENT_FAMILIES:
        orient_note = (
            "\n\nA vertical widget resolves to the ``Vertical.`` twin of each "
            "style name above.\n"
        )

    # An empty state map is common for image-driven families (scale, progressbar,
    # ...) whose state art lives in image element specs, not `style.map` -- say
    # that rather than a bare "(none)" that reads as "no interactive states".
    if states:
        states_line = (
            "The states you can target with ``style.map(...)`` to vary appearance "
            "by interaction:"
        )
        states_body = _inline_list(states)
    else:
        states_line = (
            "This style declares no ``style.map(...)`` overrides; any "
            "state-dependent appearance is drawn from its image elements."
        )
        states_body = ""

    # For image-drawn families, warn that `style.configure` does not reach the
    # image parts, and point at the custom-image-layout path for real changes.
    config_note = []
    if family in _IMAGE_FAMILIES:
        part, has_label = _IMAGE_FAMILIES[family]
        plural = " and " in part
        verb = "are" if plural else "is"
        obj = "them" if plural else "it"
        poss = "their" if plural else "its"
        non_image = "the focus ring and text label" if has_label else "the focus ring"
        config_note = [
            ".. note::",
            "",
            f"   The {part} {verb} drawn from a pre-rendered image keyed to the "
            f"``bootstyle`` color; ``style.configure(...)`` does not reach {obj}. "
            f"The options listed here style only the widget's non-image parts "
            f"(such as {non_image}). To recolor the {part}, choose a "
            f"``bootstyle`` color; to change {poss} shape or artwork, build a "
            f"custom image-based layout -- see "
            f":doc:`Custom styles </user-guide/feature-guides/custom-styles>`.",
            "",
        ]

    return [
        _rule("Bootstyle mapping", uc),
        "",
        f"Any of the accent colors -- {colors} -- substitutes for "
        f"``primary`` below.{neutral_note}"
        + orient_note,
        "",
        _bootstyle_table_rst(family),
        "",
        _rule("Layout (elements)", uc),
        "",
        "The widget is drawn from these nested parts. Each is an *element* you "
        "can target by name in a custom layout:",
        "",
        _layout_rst(layout_rows),
        "",
        _rule("Configurable style options", uc),
        "",
        *config_note,
        "Options you can set with ``style.configure(...)`` / ``style.map(...)``:",
        "",
        _inline_list(options),
        "",
        _rule("Supported states", uc),
        "",
        states_line,
        "",
        states_body,
        "",
        _rule("Hand-styling example", uc),
        "",
        _example_rst(family),
        "",
    ]


def render_family_page(style, family):
    """Return the full standalone Style Reference page for one widget family."""
    blurb = _FAMILIES[family][0]
    parts = [
        ".. Generated by tools/generate_style_reference.py -- do not edit by hand.",
        "",
        _rule(_title(family), "="),
        "",
        blurb,
        "",
    ] + _style_body_parts(style, family, "-")
    return "\n".join(parts)


def render_style_partial(style, family):
    """Return the includable styling partial (subsections only) for one family."""
    parts = [
        ".. Generated by tools/generate_style_reference.py -- do not edit by hand.",
        "",
    ] + _style_body_parts(style, family, "~")
    return "\n".join(parts)


def _index_grid(families):
    lines = [".. grid:: 1 2 2 2", "   :gutter: 3", ""]
    for family in families:
        blurb = _FAMILIES[family][0]
        lines.append(f"   .. grid-item-card:: {_title(family)}")
        lines.append(f"      :link: {family}")
        lines.append("      :link-type: doc")
        lines.append("")
        lines.append(f"      {blurb}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _toctree(caption, families):
    lines = [".. toctree::", "   :hidden:", f"   :caption: {caption}", ""]
    lines += [f"   {family}" for family in families]
    return "\n".join(lines)


def _check_families():
    """Fail loudly if the registry and the `_FAMILIES` metadata have diverged.

    Guards both directions -- a registered family missing its metadata (which
    would otherwise `KeyError` deep in rendering) and a stale `_FAMILIES` entry
    for a family the registry no longer produces.
    """
    registry = set(style_reference_families())
    described = set(_FAMILIES)
    missing = registry - described
    if missing:
        raise SystemExit(
            f"generate_style_reference: registered families {sorted(missing)} have "
            "no _FAMILIES entry; add (blurb, group, example-widget) for each."
        )
    stale = described - registry
    if stale:
        raise SystemExit(
            f"generate_style_reference: _FAMILIES lists {sorted(stale)} which the "
            "registry no longer produces; remove them."
        )


def render_index_page():
    """Return the Style Reference index (intro + card grids + hidden toctrees)."""
    _check_families()
    families = style_reference_families()
    native = [f for f in families if _FAMILIES[f][1] == "native"]
    other = [f for f in families if _FAMILIES[f][1] == "variant"]
    return "\n".join([
        ".. Generated by tools/generate_style_reference.py -- do not edit by hand.",
        "",
        _INDEX_INTRO,
        _rule("Styling ttk widgets", "-"),
        "",
        _index_grid(native),
        "",
        _rule("Variant & shipped styles", "-"),
        "",
        _index_grid(other),
        "",
        _toctree("Styling ttk widgets", native),
        "",
        _toctree("Variant & shipped styles", other),
        "",
    ])


def main():
    import tkinter as tk

    from ttkbootstrap.style import Style

    _check_families()

    root = tk.Tk()
    root.withdraw()
    style = Style(theme="bootstrap-light")

    _OUT.mkdir(parents=True, exist_ok=True)
    families = style_reference_families()

    (_OUT / "index.rst").write_text(render_index_page(), encoding="utf-8")
    print(f"wrote {_OUT / 'index.rst'}")
    for family in families:
        page = render_family_page(style, family)
        path = _OUT / f"{family}.rst"
        path.write_text(page, encoding="utf-8")
        print(f"wrote {path}")

    _PARTIAL_OUT.mkdir(parents=True, exist_ok=True)
    for family in families:
        partial = render_style_partial(style, family)
        ppath = _PARTIAL_OUT / f"{family}.rst"
        ppath.write_text(partial, encoding="utf-8")
        print(f"wrote {ppath}")

    root.destroy()


if __name__ == "__main__":
    main()
