# Repo overview

ttkbootstrap is a themed widget framework and application toolkit built
on top of Tk. The library lives under `src/ttkbootstrap/` and ships
widgets, dialogs, a styling engine, data sources, an i18n stack, and an
application runtime.

The public API surface is the union of:

- `src/ttkbootstrap/__init__.py` — top-level lazy re-exports.
- `src/ttkbootstrap/api/*.py` — grouped public exports (app, widgets,
  style, dialogs, data, i18n, utils, menu, localization).

Anything not surfaced through those modules is internal.

---

## Active work: docs review and cleanup

A multi-phase documentation overhaul is in progress on branch
`docs/review-and-cleanup`. The source of truth is:

- `analysis/docs-review-and-plan.md`

Read that first when picking up any docs work. It captures:

- the documentation model (user-guide pages vs API-spec pages),
- the docstring template (Google style, plain Markdown),
- the conventions (no `bootstyle` in narrative, examples off by default,
  "spec, not user guide" — mechanical not editorial),
- the per-symbol status of the priority API surface,
- the phased plan and the decisions log.

Do not re-derive any of those from scratch — propose updates to the
plan doc instead so they survive across sessions.

### Current handoff (2026-04-30)

Phases 1–7, 9A–9D are complete. **Phase 6 (screenshot pipeline) is partially
complete; 6F not started. Pass 2 (editorial review) is the active work.**

Phase 6 status (for reference):

- **6A–6E — DONE.** Image policy locked, renderer scaffold built, CLI wired,
  image-check tool added, in-frame shots rendered for all visible widget pages
  (13 batches). Shots are macOS placeholders; re-render on Windows for canonical
  assets (`python -m docs_scripts.render` on a Windows host overwrites every asset).
- **6F — NOT STARTED.** Popup and animated widgets need capture tooling beyond
  the in-frame model. See `analysis/docs-review-and-plan.md` § Phase 6F for the
  full list and the renderer mode needed.

Phase 9 (drift sweep) — DONE:

- `tools/check_doc_snippets.py` validates all 833 `python` blocks across 107
  docs files (compile check always; runtime check with `--run`). Currently 0
  failures. Run this before and after any docs edit to guard against regression.
- 22 doc files were fixed in Pass 1 (wrong class names, constructor kwargs,
  option names, theme names). See plan doc § Phase 9 for the full list.
- `OptionMenu(command=)` and `DropdownButton(command=)` now work (9C).
- `ttk.ListView` is now a public export (9D).

Open items from earlier phases (do not lose track):

- **8B** — `ListView.badge` field silently dropped in `update_data`
  (`listitem.py:725`). Code fix: add `"badge": self._update_badge` to the
  dispatch map.
- **8C** — Rendered docstring review for 22 priority symbols (needs display).

### Now: Pass 2 — Editorial review (Opus, one guide per session)

Pass 1 is done; every snippet is known to match the current API. Pass 2 is
the active work. Goal: each guide is best-in-class for its content type.

**All 14 guides in `docs/guides/` are done** (2026-04-30). Widget pages
in progress; platform/capabilities pages still to come.

**Widget pages — actions** (`docs/widgets/actions/`, 5 pages):

- [x] `button.md` (2026-04-30, commit `99fc744`) — first widget page reviewed.
      Establishes the template-conformant pattern other action pages should
      follow: `Framework integration` overview, `Basic usage` (not `Quick start`),
      merged `Localization & reactivity`. Use this as the canonical reference
      when reviewing the remaining four.
- [x] `buttongroup.md` (2026-04-30) — added `Framework integration`, `Behavior`,
      and `Localization & reactivity`; renamed `Quick start` → `Basic usage`;
      documented `orient`, `density`, key-based lookup
      (`item`/`configure_item`/`remove`), iteration/`len`/`in`, and group-level
      `state`. Removed two `SegmentedButton` links — that widget doesn't exist.
- [x] `contextmenu.md` (2026-04-30) — added `Framework integration`,
      `Appearance`, expanded `Examples & patterns`; renamed `Quick start`
      → `Basic usage`; documented `trigger=`, `target=` defaulting to
      master, `density`, `minwidth`/`width`, key-based lookup
      (`item`/`configure_item`/`remove_item`/`move_item`/`insert_item`/`keys`),
      `disabled=`/`shortcut=` on `add_command`, `on_item_click` payload
      shape, `items()` setter for runtime replacement, anchor/attach/offset
      positioning model, and the macOS native-backend caveats.
- [x] `dropdownbutton.md` (2026-04-30) — added `Framework integration`,
      expanded `Behavior` and `Examples & patterns`, merged
      `Localization & reactivity`. Corrected the `on_item_click`
      payload (a `{type, text, value}` dict, not an item object) and
      documented `command=` running alongside `show_menu` on click.
      Surfaced `density`, `popdown_options`, `show_dropdown_button`,
      `dropdown_button_icon`, `textsignal`, runtime-mutation API
      (`add_command`/`add_separator`/`add_checkbutton`/`add_radiobutton`/
      `configure_item`/`items()` setter), and shortcut display.
- [x] `menubutton.md` (2026-04-30) — added `Framework integration`,
      `Examples & patterns`, and `Localization & reactivity`; renamed
      `Quick start` → `Basic usage`. Documented the supported variant
      set (no `link`), `direction=`, cascading submenus, check/radio
      entries, icon-only menubutton, and runtime menu rebuilding.
      Clarified that `MenuButton` itself has no `command=` (items do)
      and that menu item labels are *not* re-resolved on locale
      change — pattern: `MessageCatalog.translate()` at construction
      and rebuild on locale switch (link to DropdownButton/ContextMenu
      for fully reactive items). Captured the macOS NSMenu caveat.

**Actions category complete.** Move on to inputs next (highest user
traffic remaining): `entry.md`, `combobox.md`, `spinbox.md`, etc. —
see `docs/widgets/inputs/`.

The category template lives at `docs/_template/widget-action-template.md`.
Run `python tools/check_doc_structure.py --category actions` to confirm
required H2s.

Run **one page at a time** as a deliberate session. Each session covers:

- **Structural fit** — does the page follow the right template for its content
  type? Use `python tools/check_doc_structure.py` (from Phase 5I) to flag
  missing required H2s, then judge the rest.
- **Accuracy** — snippets are clean, but does the *narrative* match the API?
  (Methods that no longer exist, options whose semantics changed.)
- **Completeness** — are concepts a good docs site would cover present?
- **Clarity** — framing, ordering, jargon.

Architectural pages (`platform/*`, `capabilities/*`, `design-system/*`,
`reference/*/index.md`) — same treatment, stronger weight on accuracy.

**Session workflow:**
1. Read the page end-to-end. Note gaps.
2. Rewrite in one pass.
3. `python tools/check_doc_snippets.py --run --file <page>` — confirm 0 failures.
4. Commit: `Docs: editorial review — <page title>`.

**Widget page priority** — do actions, inputs, dialogs, and data-display first
(highest user traffic); then layout, navigation, overlays, selection, views,
primitives.

**Bugs surfaced during guide review** (logged in plan, not yet fixed):
- `AppSettings.light_theme`/`dark_theme` defaults are `docs-light`/`docs-dark`
  (counterintuitive; should probably be `bootstrap-light`/`bootstrap-dark`)
- `follow_system_appearance` is silently no-op on Windows/Linux
- `ListView` calls `deselect_all()`/`is_selected()` on its datasource but
  `BaseDataSource` exposes `unselect_all()`/no `is_selected` — mismatch
- `Signal.map()` uses weakref; inline `textvariable=sig.map(fn)` can stop
  updating after the derived signal is GC'd
- `MessageDialog._parse_buttons` stores the `:role` suffix into deprecated
  `bootstyle` field instead of `accent`

**Renderer conventions** (when authoring new factories — read the
existing `docs_scripts/shots/*.py` for live examples):

- Factory signature: `def factory(parent: Widget) -> Optional[Callable]`.
  `parent` is a renderer-supplied padded `Frame`; build widgets into it.
- Return a `finalize` callable when the shot needs visual state flags
  (`state(["focus"])`, `state(["hover"])`) applied at capture time —
  Tk may otherwise clear them between deiconify and grab.
- Use `widget.focus_set()` for true focus rings; the state flag alone
  isn't always honored by ttk styles.
- **Don't** use `pack_propagate(False)` on a Frame with `width=` but no
  `height=` — height defaults to 0 and the shot renders blank. Either
  set both, or drop the propagate call.
- The renderer deliberately does NOT use `override_redirect=True` or
  `focus_force()` — both kill WM focus event propagation and flatten
  focus/hover visuals.

**Authoring loop for a new widget shot:**

1. Read `docs/widgets/<category>/<name>.md` to find the `IMAGE:`
   placeholder spec or pick a sensible default composition.
2. Add or extend a factory in `docs_scripts/shots/<category>.py`.
3. Add a `[[shots]]` entry to `docs_scripts/screenshots.toml`.
4. Render: `python -m docs_scripts.render --slug widgets-<name>`.
5. View output at `docs/assets/{light,dark}/widgets-<name>.png`.
6. Replace the `IMAGE:` block (or insert a new `<figure markdown>`
   block) in the .md file with the canonical light + dark refs.
7. Run `python tools/check_doc_images.py` to confirm 0 missing.
8. Commit factory + manifest + .md + PNGs together; commit message
   format: `Docs: screenshots for X, Y, Z (6E batch N)`.

The plan doc (`analysis/docs-review-and-plan.md`) has the full
architecture decisions log.

---

## Documentation toolchain

- **Zensical** (separate from plain MkDocs), not Sphinx. Configuration:
  `zensical.toml`. Install via `pip install -e ".[docs]"`. Serve with
  `.venv/bin/zensical serve -o`.
- **Plain Markdown only** in docstrings — no reST roles like `:func:`,
  `:param:`, or `.. note::`. The MkDocs `admonition` extension is
  enabled, so `!!! note "Heading"` blocks are allowed in docstrings.
- **mkdocstrings** renders the API reference from source docstrings
  using the Google convention. Reference pages are bare
  `::: module.Class` directives. Class docstrings carry narrative and
  `Attributes:`; `__init__` docstrings carry `Args:`. Both render —
  don't relocate, fill gaps.

---

## Linting and validation

Public-API docstring discipline is enforced by ruff `D` rules with the
Google convention, configured in `pyproject.toml` under `[tool.ruff]`.
Run from the repo root:

```bash
.venv/bin/ruff check src/ttkbootstrap
```

Internal directories (`widgets/mixins`, `widgets/internal`,
`widgets/parts`, `style/builders`, `style/builders_tk`,
`core/capabilities`, `core/mixins`, `cli`, `assets`) are blanket-ignored
in `[tool.ruff.lint.per-file-ignores]`.

Public-surface files whose docstrings haven't yet been brought to spec
are listed individually in the same block. Each entry is removed once
that file passes:

```bash
.venv/bin/ruff check --select D --isolated src/ttkbootstrap/path/to/file.py
```

Use `--isolated` to bypass `pyproject.toml` and see the real violations
the ignore is currently suppressing.

---

## Conventions

- One canonical import in examples: `import ttkbootstrap as ttk`.
- The `bootstyle` parameter is **deprecated**. In descriptive prose,
  describe styling via the canonical tokens (`accent`, `variant`,
  `density`, `surface`, `show_border`). The `bootstyle` parameter is
  still marked DEPRECATED in argument docs for users who haven't
  migrated.
- Class docstrings describe what something **is** and **does**
  mechanically. Don't write "when to use this," "best for…," or
  comparisons to sibling classes — those belong in user-guide pages
  under `docs/widgets/` or `docs/guides/`.
- Examples in docstrings are off by default. Add an `Examples:` section
  only when the call shape is non-obvious from the signature alone
  (decorators, context managers, abstract subclassing patterns,
  ambiguous polymorphic args). "Construct it and pack it" doesn't
  qualify.

---

## Branches and commits

- Active feature work for v2 lives on `release/v2`.
- The docs review effort lives on `docs/review-and-cleanup`.
- Commit messages on this branch use the format
  `Docs review phase N: <summary>` for phase-scoped commits and
  `Docs: <summary>` for individual file cleanups.
