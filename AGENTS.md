# AGENTS.md — orientation for AI coding agents (Codex et al.)

This file is the entry point for an AI agent picking up work in this repo. It is
checked into git, so it travels with the repo across machines. Read it first,
then the docs it points to.

> A parallel `CLAUDE.md` exists with the same project facts. This file adds the
> cross-machine handoff and a condensed set of working notes that otherwise live
> only in a per-user memory store (which does **not** travel between machines).

## What this project is

ttkbootstrap is a **theming extension for tkinter/ttk** — it generates modern,
flat, Bootstrap-inspired themes on demand and adds a `bootstyle=` keyword API to
ttk widgets. Pure Python; the only runtime dependency is **Pillow** (image-based
widget assets). Public entry point: `src/ttkbootstrap/__init__.py`, imported as
`import ttkbootstrap as ttk`. src layout, `requires-python >= 3.10`.

ttkbootstrap stays a **styling extension for vanilla tkinter** — NOT a widget
library. The forward-looking widget framework is a **separate** project,
**bootstack** (www.bootstack.org). Several 2.0 mechanisms are *ported from*
bootstack (the asset render pipeline, the icon renderer) — port the mechanism,
not bootstack's API.

## The active initiative: the 2.0 cleanup

**2.0 is a cleanup/consolidation release — no new features.** Goals: remove
cruft, normalize the API (breaking is OK when meaningful, with a migration
path), fix memory leaks + theme-switch perf, make user-defined custom styles
easy, overhaul docs. Target: **end of July 2026**.

Read these, in order, before any 2.0 work:

1. **`development/2_0_handoff.md`** — the living session handoff. Current state,
   what's merged, what's next. **Start here.**
2. **`development/2_0_plan.md`** — the durable worklist (locked decisions +
   workstreams A–I).
3. The per-workstream design docs, as relevant:
   - `development/2_0_engine_design.md` — repaint engine + image cache (Workstream A).
   - `development/2_0_style_split_design.md` — the `style/` package split (G).
   - `development/2_0_toolkit_design.md` — the public style-construction toolkit (I).
   - `development/2_0_icons_design.md` — the Bootstrap-Icons glyph renderer (I).
   - `development/2_0_recolor_assets_design.md` — **recolorable raster widget
     assets** (merged in #1081).
   - `development/2_0_builder_split_design.md` — modular `StyleBuilderTTK`
     recipe registry (approved, implemented, and visually approved).

### Where things stand (snapshot — confirm against the handoff, it's authoritative)

Integration branch is **`2.0`** (cut all 2.0 PRs against it, NOT `master`).
Merged into `2.0`: engine repaint + content-addressed image cache (PRs 1–2),
mixin API replacing the import-time monkey-patch (PR 3), the `style/` package
split (PR 4), the public asset/layout toolkit (PR 5), the icon engine (PR 6a),
the glyph-builder migration (PR 6b), and recolorable raster widget assets
(#1081). The modular `StyleBuilderTTK` branch raises the expected suite to
**147 passed** and is headless-clean apart from the documented local Tcl
catalog defect. Its human light↔dark smoke gate passed. Workstream E
(theme/anchor model) and D
(bootstyle canonical grammar) remain later candidates and each needs its own
design pass first.

## Current task this handoff: modularize `StyleBuilderTTK`

Branch: **`refactor/2.0-builder-modules`**, cut from `2.0` after the recolorable
raster-assets PR merged as **#1081**. The 2,689-line
`style/builders_ttk.py` recipe monolith is now a 161-line coordinator plus a
private frozen decorator registry and 22 widget-family modules.

The approved design and exact verification results are in
**`development/2_0_builder_split_design.md`**. Headless, structural, and human
light↔dark smoke gates pass. Preserve the existing
bootstyle grammar, generated style names, lazy per-theme behavior, and visuals.

## How to work here

### Build / test / run
- Headless test suite: `python -m pytest -q` (config in `pyproject.toml`,
  `testpaths = ["tests"]`). This is the CI-runnable gate; keep it green.
- A virtualenv with an editable install lives at `.venv/`. The package is also
  importable with `PYTHONPATH=src`.
- `tests/` is **headless pytest only**. Interactive `mainloop()` demos live in
  `examples/` and are NOT collected by pytest. Put any visual/manual check there.
- Docs: `mkdocs serve` (deps in `requirements.txt`). Docs are **MkDocs, not
  Sphinx** — write docstrings in **plain Markdown**; do NOT use reST roles or
  directives (`:func:`, `:param:`, `.. note::` …).

### Branch + PR model
- 2.0 cleanup work → branch off **`2.0`**, PR into **`2.0`**.
- Maintenance/bugfixes → branch off **`master`**, PR into `master`.
- One change per branch/PR. Imperative commit subjects; reference issues
  (`fixes #NNNN`) where applicable. Do not exceed a PR's designed scope without
  revisiting its design doc.

### Hard rules / gotchas (these have bitten before)
- **Do not start style-engine work as ad-hoc coding.** New public surface or
  engine changes get a **design pass first** (a design doc + user sign-off),
  like the engine/split/toolkit/icons did. The recolor strand follows this.
- **`Style` is a process-wide singleton tied to the first Tk root.** Creating +
  destroying separate roots in one process mis-binds it and later theming
  silently no-ops. Tests must take the shared **`root` fixture** from
  `tests/conftest.py` — never create their own `ttk.Window`.
- **`import ttkbootstrap` must stay warning-free.** Deprecation shims warn only
  when an old path is actually used. Private plumbing lives in
  `src/ttkbootstrap/internal/` (the name is `internal`, no underscore) with no
  back-compat guarantee; old public paths get warn-and-reexport shims removed in
  3.0.
- **Styles build lazily, on demand** (not all up front) — see CLAUDE.md "Lazy
  style building". A widget the app never instantiates can fall back to the bare
  clam look; the fix is to build the base style eagerly in
  `create_default_style()`.
- **Python 3.14 / PEP 649**: lazy annotations can mask a missing
  annotation-only import. An "does it import?" check is insufficient — run an
  annotation force-evaluation sweep when moving code (pattern noted in the PR 4
  design doc).
- **Don't kill blocking modal dialogs externally to test them.** Tk modal
  `show()` calls closed via threads/`after` produce misleading errors. Read the
  code or ask the user instead.

### Repo map (essentials)
```
src/ttkbootstrap/
  __init__.py        # public exports; concrete BootMixin/AutoStyleMixin widget subclasses
  style/             # THE CORE engine package (split from style.py in 2.0):
    theme.py         #   Colors, ThemeDefinition
    builders_tk.py   #   StyleBuilderTK (legacy tk.* widgets)
    builders_ttk.py  #   StyleBuilderTTK (the bulk — create_*_style / create_*_assets)
    engine.py        #   Style singleton: theme walk, _image_cache, _get_or_create_image
    bootstyle.py     #   Keywords, Bootstyle resolver, BootMixin/AutoStyleMixin
    assets.py        #   PUBLIC toolkit: Assets (circle/rect/rounded_rect/icon/image)
    layout.py        #   PUBLIC toolkit: El/layout, image_element, statespec/state_map, register_style
    icons.py         #   IconRenderer + Icon atom + icon_element (Bootstrap Icons glyphs)
  assets/icons/      # vendored Bootstrap Icons font + glyphmap + metrics (package data)
  widgets/, dialogs/, themes/, internal/, localization/
tests/               # headless pytest only
examples/            # interactive demos
development/         # 2.0 plan + per-workstream design docs + the living handoff
```
