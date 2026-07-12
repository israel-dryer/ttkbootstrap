# 2.0 Docs — Widget API Reference workstream (handoff)

Self-contained handoff so this work can continue on any machine (the author's
`~/.claude` memory is machine-local and does NOT transfer; this repo doc does).
Part of Workstream H (docs). Created 2026-07-12.

## Goal

Ship **our own** widget API reference instead of depending on python.org, which
documents the classic tk widgets (`Text`/`Canvas`/`Listbox`/`Menu`) not at all
and is thin elsewhere. Cross-link python.org / Tcl-Tk **as supplementary** where
they exist, never instead of our own. Maintenance is expected to be low (tkinter
rarely changes).

## Scope (LOCKED with author)

Two buckets, nothing else:

1. **Blessed tk widgets:** `Text`, `Canvas`, `Listbox`, `Menu`, plus the trivial
   containers `Tk`, `TkFrame`, `TkLabel`, `LabelFrame`. (Listbox was newly
   blessed — see PR #1186.)
2. **Native ttk widgets:** Button, Entry, Combobox, Spinbox, Checkbutton,
   Radiobutton, Menubutton, OptionMenu, Frame, Labelframe, Notebook, Panedwindow,
   Label, Progressbar, Scale, Scrollbar, Separator, Sizegrip, Treeview.

NOT in scope: the **shipped** ttkbootstrap widgets (Meter/Floodgauge/DateEntry/
Tableview/…) — they already get **autodoc** pages from their docstrings
(`reference/api/widgets.rst`). Not any tkinter widget we don't touch.

## Structure (two layers)

**Tier 1 — Capabilities section** (`docs/reference/capabilities/`): the methods
every widget inherits, **one page per area, each mirroring the matching Tcl/Tk
8.6 manual page** so the two references line up (transferable knowledge). A
capability page is a **spec** (signatures/params/returns) — NOT a guide; the
Foundations guides teach the same areas by building, and the two cross-link.

**Tier 2 — per-widget API pages** (`docs/reference/api/<widget>.rst`): the
widget's OWN options (as value tables) + its widget-specific methods (as full
specs). Each page ends with a "Shared capabilities" section linking to the
Capabilities index. Options section opens with a `ttkbootstrap` rubric
documenting the added constructor keyword — **`autostyle`** for tk widgets,
**`bootstyle`** for ttk widgets (construction-only; does NOT appear in
`configure()`, so a naive option dump misses it — always add it by hand).

## Format rules (approved)

- **Methods = `.. py:method::` directives** with `:noindex:`, an authored
  signature, and `:param:` / `:returns:` / `:rtype:` / `:raises:`. Grouped under
  `~~~~` subsection headings. See `docs/reference/api/text.rst` and
  `docs/reference/capabilities/focus.rst` as the canonical templates.
- **Options = two-column `.. list-table::`** (name | description), grouped under
  `.. rubric::` headings. Fold aliases into one row (`borderwidth` (`bd`)).
- **Left-column multi-method cells:** stack with rST line blocks (`| a` / `| b`),
  never slash-separated (hard to read when wrapped). (Mostly obsolete now that
  methods are individual `py:method` entries.)
- **`:noindex:`** avoids cross-ref-target collisions (every widget has `insert`).
  If we later want summary tables to link into the specs, wrap each widget's
  methods in `.. py:class:: tkinter.<Widget>` so targets qualify
  (`tkinter.Text.insert`) and don't collide. Not done yet — not needed so far.
- **No meta/rationale prose in the docs** ("documented once here rather than
  repeated…"): state the user-facing fact, cross-reference, move on.
- **Don't tag rubric headings with the method prefix** — "Introspection", not
  "Introspection (winfo)".
- Reference the **Tcl/Tk 8.6** man pages (`tcl8.6/TkCmd/…`, the version Python
  ships) as the canonical upstream; do NOT link Shipman (tkdocs.com/shipman).

## Grounding discipline (non-negotiable)

Every option/method is verified against the LIVE widget before writing —
`configure().keys()` for options, filtered `dir()` for widget-specific methods
(subtract `Widget|Misc|Pack|Grid|Place`), `inspect.signature(...)` for each.
Never invent an entry. Note methods filtered out as "universal" that a widget
actually owns (e.g. `Canvas.bbox`, `Listbox.size`) and add them by hand.

## Build / environment

- Python + Sphinx live in **`.venv-home`** (the repo `.venv` is broken on the
  author's box). Run: `.venv-home/Scripts/python.exe` (Git-Bash path
  `/d/Development/ttkbootstrap/.venv-home/Scripts/python.exe`).
- Build gate (must be exit 0): `python -m sphinx -b html -W -q docs <outdir>`.
  Use a throwaway outdir (e.g. `/tmp/ttkdocs-b`) and `-E` for a fresh
  (non-incremental) build when in doubt — incremental builds can hide autodoc
  warnings.
- `docs/reference/capabilities/` pages that are folded-in (events/winfo) are
  linked from `capabilities/index.rst`'s toctree via absolute paths
  (`/reference/events/index`), leaving the files physically where they are.

## DONE (branch `docs/2.0-api-reference-text-stacked`, stacked on #1185)

- **Capabilities section** complete: `configuration`, `pack`, `grid`, `place`,
  `stacking`, `focus`, `grab`, `after`, `lifecycle`, `clipboard`, `selection`
  (+ `capabilities/index.rst`). Existing **Events** (`reference/events/`) and
  **Widget & screen info** (`reference/winfo`) are folded in via the index
  toctree. **Cursors** is NOT a capability — it stays a standalone Reference-band
  card (`reference/cursors`).
- **Per-widget API pages (tk set):** `text.rst`, `canvas.rst`, `listbox.rst`,
  `menu.rst` — all complete (options tables + all widget-specific methods as
  `py:method`). Menu includes the ttkbootstrap macOS additions
  (`add_application_menu`/`window`/`help`, `on_preferences`/`on_quit`).
- Reference band (`reference/index.rst`) now shows: Style Reference, API
  Reference, Capabilities, Cursors.
- The interim monolithic `reference/api/shared-capabilities.rst` +
  `docs/shared/` partial were created then **retired** (replaced by the
  Capabilities section). `conf.py` still lists `shared` in `exclude_patterns` —
  harmless (dir is gone); can be removed on cleanup.

## REMAINING

1. **Trivial tk containers:** `Tk` (root — the `wm_*`/window-manager surface;
   note `Window`/`Toplevel` already wrap most of this), `TkFrame`, `TkLabel`,
   `LabelFrame`. Small.
2. **The ~19 native ttk pages** — the large mechanical batch. Same Tier-2 shape;
   their `bootstyle` row replaces the tk `autostyle` row; they CAN also link
   python.org `tkinter.ttk` as supplementary (it exists for ttk). Consider
   whether each needs a full method spec or can lean on the shared/`ttk`-specific
   methods (`state`/`instate`) — a `ttk` capability partial for `state`/`instate`
   was noted but not yet authored.
3. Wire each new API page's catalog counterpart to cross-link it (as
   `text.rst`/`widgets/text` do), once those catalog pages exist.

## PR / merge state (IMPORTANT for continuation)

- This work is on **`docs/2.0-api-reference-text-stacked`**, which is **stacked on
  `docs/2.0-widgets-text` (PR #1185, the Text *catalog* page)** — that base is
  NOT yet in `2.0`. The API-reference PR is therefore targeted at
  `docs/2.0-widgets-text` so its diff is only the API-reference work.
- **Pending stack to merge (in order):** **#1184** (Treeview catalog),
  **#1185** (Text catalog — this branch's base), **#1186** (bless `ttk.Listbox`,
  needed for the Listbox page's widget to be real). After #1185 merges to `2.0`,
  **retarget this PR to `2.0`** (it will rebase clean).

## Deferred ideas (later review)

- Mine the Tcl/Tk man pages for **conceptual** sections (e.g. Pack.htm's
  "Expansion" and "Geometry Propagation") to enrich the **Foundations/feature
  guides** (not the spec pages).
- Optional: qualify method targets via `.. py:class::` if summary-table→spec
  links are ever wanted.
- The broader Widgets **catalog** track (separate from this API-reference track)
  still has Canvas/Listbox/Scrolled catalog pages + the coverage sync test
  outstanding — see the main docs design doc.
