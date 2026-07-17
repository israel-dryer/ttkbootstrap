#!/usr/bin/env python
"""Generate the canonical bootstyle reference from the vocabulary + registry.

The bootstyle grammar (2.0 Workstream D) has a single closed vocabulary
(`ttkbootstrap.constants`) and a frozen builder registry
(`ttkbootstrap.style.builders.registry`) that together define exactly which
canonical bootstyle strings resolve to a real ttk style. Rather than hand-list
them (and drift), this tool derives them:

- `canonical_bootstyles()` -> the sorted set of canonical strings a user can
  type. It backs the `BootStyle` `Literal` in `constants.py` (regenerate the
  block below and paste it in) and the `test_bootstyle_grammar` sync test.
- `reference_table_rst()` -> the human reference grouped by widget family,
  written to `docs/_generated/bootstyle_reference.rst` and folded into the
  Workstream-H flagship guide (`docs/user-guide/concepts/bootstyle-grammar.rst`)
  via `.. include::`.

Run it after changing the vocabulary or adding/removing a builder:

    python tools/generate_bootstyle_reference.py

It rewrites the rST include and prints the `BootStyle = Literal[...]` block to
stdout for pasting into `constants.py`. The sync test fails until both are
regenerated, so the reference can never silently drift from the code.
"""
from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from ttkbootstrap.constants import (  # noqa: E402
    BOOTSTYLE_COLORS,
    BOOTSTYLE_BASES,
    BOOTSTYLE_INTERNAL_MODIFIERS,
    BOOTSTYLE_DEPRECATED_MODIFIERS,
    BOOTSTYLE_SURFACES,
    DEFAULT_SURFACE,
    NEUTRAL,
    NEUTRAL_FAMILIES,
)
from ttkbootstrap.style.builders import load_builders  # noqa: E402
from ttkbootstrap.style.builders.registry import (  # noqa: E402
    builder_keys,
    DEFAULT_VARIANT,
)

_REFERENCE_RST = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "_generated"
    / "bootstyle_reference.rst"
)


def _public_keys():
    """Return the registered (variant, family) keys that are user-facing.

    The internal composite variants (`meter`/`metersubtxt`/`date`/`table`) are
    plumbing for Meter/DateEntry/Tableview -- never typed by a user -- so they
    are excluded from the public reference. Deprecated variants (`inverse`) still
    resolve for back-compat but are no longer advertised, so they are excluded too.
    """
    load_builders()
    hidden = set(BOOTSTYLE_INTERNAL_MODIFIERS) | set(BOOTSTYLE_DEPRECATED_MODIFIERS)
    return sorted(
        (variant, family)
        for variant, family in builder_keys()
        if variant not in hidden
    )


def _strings_for_key(variant, family):
    """Yield the canonical bootstyle strings a user types for one key.

    The base-type is spelled only for the "chameleon" families (`toggle`,
    `toolbutton`); for every other family it is inferred from the widget, so it
    is omitted. Slots are emitted in canonical order: color, modifier, base.
    """
    modifier = None if variant == DEFAULT_VARIANT else variant
    base = family if family in BOOTSTYLE_BASES else None
    for color in (None, *BOOTSTYLE_COLORS):
        # `neutral` is a derived, no-accent color that only renders for a curated
        # set of families (NEUTRAL_FAMILIES) -- don't advertise it elsewhere even
        # though the tokenizer would parse it.
        if color == NEUTRAL and family not in NEUTRAL_FAMILIES:
            continue
        parts = [p for p in (color, modifier, base) if p]
        if parts:
            # spaces are the recommended separator (the tokenizer also accepts
            # dashes); the reference + the BootStyle autocomplete Literal both
            # advertise the space form.
            yield " ".join(parts)


def canonical_bootstyles():
    """Return the sorted set of all canonical bootstyle strings."""
    strings = set()
    for variant, family in _public_keys():
        strings.update(_strings_for_key(variant, family))
    return sorted(strings)


def bootstyle_literal_source():
    """Return the `BootStyle = Literal[...]` source block for constants.py."""
    entries = ",\n    ".join(repr(s) for s in canonical_bootstyles())
    return f"BootStyle = Literal[\n    {entries},\n]\n"


def reference_table_rst():
    """Return the canonical bootstyle reference as an rST include partial.

    Emitted as a partial (no page title) so it can be folded into the flagship
    `bootstyle-grammar.rst` via `.. include::`. Its section headings use the
    ``----`` (H2) underline so they nest under that page's ``====`` title.
    """
    colors = ", ".join(f"``{c}``" for c in BOOTSTYLE_COLORS)
    # Surfaces: the non-default surface tokens a `@<surface>` slot accepts --
    # `card` plus every accent color (`background` is the implicit default).
    surface_tokens = [s for s in BOOTSTYLE_SURFACES if s != DEFAULT_SURFACE]
    surface_tokens += [c for c in BOOTSTYLE_COLORS if c != NEUTRAL]
    surfaces = ", ".join(f"``@{s}``" for s in surface_tokens)
    lines = [
        ".. Generated by tools/generate_bootstyle_reference.py -- do not edit by",
        ".. hand. Regenerate after any vocabulary/builder change; the",
        ".. test_bootstyle_grammar sync test fails until this file is current.",
        "",
        "Colors",
        "------",
        "",
        f"The color slot accepts any of the semantic colors: {colors}.",
        "",
        "Surfaces",
        "--------",
        "",
        "The optional ``@<surface>`` slot names the surface a control sits on so "
        "it can blend on a card or an accent bar. It accepts:",
        "",
        surfaces + ".",
        "",
        "Widget families and variants",
        "----------------------------",
        "",
        "Every registered widget family and its variants. The **base-type** is",
        "normally inferred from the widget and only spelled for the chameleon",
        "families ``toggle`` / ``toolbutton``.",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 30 25 45",
        "",
        "   * - Widget family",
        "     - Variant",
        "     - Example",
    ]
    for variant, family in _public_keys():
        example = _example_for_key(variant, family)
        variant_label = "default" if variant == DEFAULT_VARIANT else variant
        lines.append(f"   * - ``{family}``")
        lines.append(f"     - {variant_label}")
        lines.append(f"     - ``{example}``")
    lines.append("")
    return "\n".join(lines)


def _example_for_key(variant, family):
    """A single representative canonical string for the reference table."""
    modifier = None if variant == DEFAULT_VARIANT else variant
    base = family if family in BOOTSTYLE_BASES else None
    parts = [p for p in ("primary", modifier, base) if p]
    return " ".join(parts)


def main():
    _REFERENCE_RST.parent.mkdir(parents=True, exist_ok=True)
    _REFERENCE_RST.write_text(reference_table_rst() + "\n", encoding="utf-8")
    print(f"wrote {_REFERENCE_RST}")
    print()
    print("# paste this BootStyle block into src/ttkbootstrap/constants.py:")
    print(bootstyle_literal_source())


if __name__ == "__main__":
    main()
