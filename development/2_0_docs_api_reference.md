# 2.0 Docs — API Reference workstream (handoff)

Self-contained handoff so this work can continue on any machine (the author's
`~/.claude` memory is machine-local and does NOT transfer; this repo doc does).
Part of Workstream H (docs). Created 2026-07-12; expanded 2026-07-12 (widget
reference done → whole-public-API reference).

## Goal

Ship **our own** API reference instead of depending on python.org, which
documents the classic tk widgets (`Text`/`Canvas`/`Listbox`/`Menu`) not at all
and is thin elsewhere, and which never covers the ttkbootstrap-authored API.
Cross-link python.org / Tcl-Tk **as supplementary** where they exist, never
instead of our own. Maintenance is expected to be low (tkinter rarely changes).

## Reference IA & scope (LOCKED with author, 2026-07-12)

The scope widened from "just widgets" to **the whole public API**. The Reference
layer (`docs/reference/`) is a **FLAT** set of top-level sections — author's rule:
*only group what needs grouping; no invented buckets* (`feedback_dont_overgroup_ia`):

    Widgets · Windows · Dialogs & overlays · Styling · Theming · Imaging ·
    Localization · Fonts · Validation · Utilities · Capabilities · Events · Cursors

Locked decisions:

- **"Widgets"** names BOTH the usage catalog (`docs/widgets/`, top-level band) and
  the reference section (`docs/reference/api/`). They coexist — different routes —
  as on bootstack.org. The reference "Widgets" index groups pages **by function**
  (Buttons & menus / Text & entry / Selection & toggles / Range & progress /
  Data views / Layout & containers / Display & drawing / Overlays), NOT by origin.
- **Hand-write** (like the tk widget pages — see Format rules): Widgets ✅,
  **Windows** (`Window`, `Toplevel`), **Dialogs & overlays** (the dialogs +
  `Toast`/`ToolTip` moved out of Widgets), and the `PhotoImage` part of **Imaging**.
- **Autodoc** (napoleon, from docstrings): **Styling** (`Style`, `Bootstyle`,
  toolkit `Assets`/`El`/`layout`/`StyleName`/`register_style`/`statespec`/
  `state_map`/`image_element`), **Theming** (`Theme`, `ThemeDefinition`, `Colors`,
  `install_legacy_themes`), **Localization** (`MessageCatalog`/`L`/`LocaleVar`/
  `set_locale`), **Fonts** (`Fonts`), **Validation** (`Validation`/`validator`/
  `ValidationEvent`), **Utilities** (`ttkbootstrap.utils` / `colorutils`), and the
  icon part of **Imaging**.
- **Imaging** = `PhotoImage` (hand) + `Icon`/`apply_icon`/`icon_element` (autodoc):
  the author placed `Icon` with **imaging** (an image you show on a widget), NOT
  with Styling. Styling & theming are **separate** sections (distinct concerns).
  Styling cross-links to `icon_element` for custom layouts.
- **No examples in docstrings** (author rule, `feedback_no_examples_in_docstrings`):
  examples live in the rST pages. Autodoc sections require a
  **strip-`Examples:`-from-docstrings sweep FIRST**, then author examples in the page.
- **Capabilities**: a **Bind** page (`bind`/`bind_all`/`bind_class`/`unbind`/
  `bindtags`) was added. `event_generate` stays in **Events** (its option
  vocabulary lives there), cross-linked from Bind.
- **Cursors** stays a flat top-level Reference entry; **Events** was promoted out
  of Capabilities to a flat top-level entry and retitled "Events".

## Structure (two layers)

**Tier 1 — Capabilities section** (`docs/reference/capabilities/`): the methods
every widget inherits, **one page per area, each mirroring the matching Tcl/Tk
8.6 manual page** so the two references line up (transferable knowledge). A
capability page is a **spec** (signatures/params/returns) — NOT a guide; the
Foundations guides teach the same areas by building, and the two cross-link.

**Tier 2 — per-widget API pages** (`docs/reference/api/<widget>.rst`): the
widget's OWN options (as flat typed tables) + its widget-specific methods (as full
`py:method` specs) + a "Styling options" section (ttk widgets) that `.. include::`s
a generated partial + a "Shared capabilities" section linking to the Capabilities
index. Options include the ttkbootstrap constructor keywords by hand —
**`autostyle`** (tk widgets), **`bootstyle`**/`icon`/`icon_size`/`icon_only` (ttk) —
which are construction-only and do NOT appear in `configure()`.

## Format rules (approved)

- **Flat typed option tables:** `.. list-table::` with `Option | Type |
  Description`, **one row per option**, plain Python types (`int`/`float`/`str`/
  `bool`/`callable`/`Variable`/`PhotoImage`/`Menu`/`Widget`/`list`/`tuple`/
  `str | Font`/`int | tuple`/`any`), `bootstyle` first, true aliases folded
  (`borderwidth` (`bd`)). Tkinter is the Python wrapper on Tcl/Tk — use Python
  types, not an invented color/font/callback vocabulary.
- **Methods = `.. py:method::`** with `:noindex:`, an authored signature, and
  `:param:`/`:returns:`/`:rtype:`/`:raises:`, grouped under `~~~~` subsections.
  Templates: `docs/reference/api/text.rst`, `docs/reference/capabilities/focus.rst`,
  `docs/reference/capabilities/bind.rst`.
- Shared ttk `state`/`instate`/`identify` and universal methods go to
  **Capabilities**, not per-page (each page's "Shared capabilities" links there).
- **No meta/rationale prose, no jargon, no impl-detail asides** — state the
  user-facing fact, cross-reference, move on. Intro paragraphs must NOT re-link the
  catalog/usage page (it's already in "See also").
- Reference the **Tcl/Tk 8.6** man pages (`tcl8.6/TkCmd/…`) as canonical upstream;
  do NOT link Shipman (tkdocs.com/shipman).

## Grounding discipline (non-negotiable)

Every option/method is verified against the LIVE widget before writing —
`configure().keys()` for options (then ADD the construction-only `bootstyle`/`icon*`
by hand), filtered `dir()` for widget-specific methods (subtract
`Widget|Misc|Pack|Grid|Place`), `inspect.signature(...)` for each. Never invent an
entry. Note methods filtered as "universal" that a widget actually owns
(`Canvas.bbox`, `Listbox.size`) and add them by hand.

## Build / environment

- **macOS box (current):** repo **`.venv`** works — `.venv/bin/python`; Sphinx
  9.1.0 + `sphinx-autobuild`. Live preview:
  `.venv/bin/sphinx-autobuild docs /tmp/ttkdocs-live --open-browser`.
- **Windows box:** Python + Sphinx live in **`.venv-home`** (the repo `.venv` is
  broken there): `.venv-home/Scripts/python.exe`.
- Build gate (must be exit 0): `python -m sphinx -b html -W -q -E docs <outdir>`
  (`-W` warnings-as-errors; `-E` forces a fresh non-incremental build so autodoc
  warnings can't hide). Use a throwaway outdir (e.g. `/tmp/ttkdocs-b`).

## DONE

The earlier api-reference stack (`docs/2.0-api-reference-text-stacked`) and its
bases are **MERGED** into `2.0` as **#1184/#1185/#1186/#1187**. This session's
work is on **`docs/2.0-widget-api-reference`** off `2.0`:

- **All ~34 widget reference pages** complete (`docs/reference/api/*.rst`): the tk
  set (Text/Canvas/Listbox/Menu + Tk/TkFrame/TkLabel/tklabelframe), the 19 native
  ttk pages, AND the 7 shipped widgets **hand-authored** (Meter/Floodgauge/
  LabeledScale/DateEntry/Tableview/ToastNotification/ToolTip) — the original
  "shipped = autodoc" plan was **reversed** so every widget page shares one flat
  typed-table + `py:method`-spec shape.
- **Styling folded into the widget pages**: each ttk page has a "Styling options"
  section that `.. include::`s a generated partial (`docs/reference/api/_style/
  <family>.rst`). The **standalone Style Reference section was retired**;
  `tools/generate_style_reference.py` now emits only the partials; the sync test
  `tests/test_style_reference.py` enforces that every family has a partial AND
  every partial is included by an API page. Orphan families folded in:
  toggle→Checkbutton, toolbutton→Button, calendar→DateEntry, floodgauge→Floodgauge.
- **Reference IA reshaped** (commit `4a7bc57f`): api index "API Reference"→
  **"Widgets"** + regrouped **by function**; **Events** promoted to top-level +
  retitled; **Bind** capability page added.
- **Capabilities** complete: configuration/pack/grid/place/stacking/**bind**/focus/
  grab/after/lifecycle/clipboard/selection (+ folded winfo). Events is now
  top-level (not folded here). Cursors top-level.

## REMAINING (the non-widget reference sections — next big batch)

DONE so far: **Windows** (#1189), **Dialogs & overlays** (#1190), and the first
**autodoc** slice — **Validation**, **Fonts**, **Localization** (in progress on
`docs/2.0-reference-autodoc`).

Still to author:

1. **Imaging**: `PhotoImage` (hand) + `Icon`/`apply_icon`/`icon_element` (autodoc).
2. **Autodoc sections**: **Styling**, **Theming**, **Utilities** — Styling
   (`style/layout.py` ×6, `engine.py` ×1) and Theming (`theme.py` ×3) still need
   the `Examples:` strip first; the others have none.
3. Add each new section's card + toctree to `docs/reference/index.rst`.

### Notes carried from the autodoc slice (READ before continuing autodoc)

- **Docstring inline-rST issue (systemic).** ttkbootstrap docstrings are
  Markdown-authored (single backticks, occasional `*args`/trailing-letter
  markup). autodoc renders them as rST, so single-backtick spans become
  title-refs (wrong, not fatal) and *unclosed* markup (`` `LocaleVar`s ``,
  `*args` in prose) is a hard `-W` error. The `conf.py` fence shim only handles
  ```` ```python ```` blocks, not inline. **Decision still needed** before the
  Styling/Theming/Utilities autodoc pages: set `default_role = "code"` (fixes
  rendering of valid single backticks globally) and fix unclosed cases as found,
  vs a docstring sweep. For the Localization slice only the two unclosed cases
  were fixed in source (`localization/api.py`, `msgcat.py`).
- **`Examples:` in docstrings** must be stripped for Styling/Theming (the
  `feedback_no_examples_in_docstrings` rule) — examples belong in the guides.
- **Fonts re-export (done this slice):** `Font`, `font_families`, `nametofont`
  are re-exported at top level (`ttk.Font`, …) so the Fonts page documents the
  full font surface (the `Fonts` manager + the tk `Font` object's
  `measure`/`metrics`/`actual` + family listing). `font_names` was dropped — it
  overlapped confusingly with `Fonts.names()`, which returns the curated managed
  set, not every named font. **FOLLOW-UP:** expand the **Typography usage guide**
  with examples for these where appropriate (`measure`, `font_families`, building
  a `Font`).

## Deferred ideas (later review)

- Mine the Tcl/Tk man pages for **conceptual** sections (Pack.htm "Expansion" /
  "Geometry Propagation") to enrich the **Foundations/feature guides** (not specs).
- Optional: qualify method targets via `.. py:class::` if summary-table→spec links
  are ever wanted (currently `:noindex:` to avoid `insert`-style target collisions).
- `conf.py` still lists a stale `shared` in `exclude_patterns` (the dir is gone) —
  harmless; remove on cleanup.
