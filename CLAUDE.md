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

### Current handoff (2026-04-29)

Phases 1–5 and 7 are complete. **Phase 6 (screenshot pipeline) is in
progress.** Status:

- **6A — DONE.** Image policy: every widget page that renders something
  visible has a light + dark screenshot pair (`docs-light` / `docs-dark`
  themes). Opt-out only for theme-agnostic assets via
  `themes = ["light"]`.
- **6B — DONE.** Renderer scaffold: `docs_scripts/render.py` reads
  `docs_scripts/screenshots.toml` and runs **one subprocess per
  `(slug, theme)` pair** for clean Tk lifecycle isolation. Factories
  live under `docs_scripts/shots/<widget>.py`.
- **6C — DONE.** `ttkb screenshots [--slug | --page | --theme]` wraps
  the renderer; lives in `src/ttkbootstrap/cli/screenshots.py`.
- **6D — DONE.** `tools/check_doc_images.py` verifies every Markdown
  image reference resolves on disk; surfaces `IMAGE:` placeholders as
  INFO (or FAIL with `--strict-placeholders`).
- **6E — IN PROGRESS.** 8 batches landed (~34 widgets done): button,
  checkbutton, radiobutton, dateentry, numericentry, spinnerentry,
  textentry, frame, labelframe, separator, sizegrip, accordion,
  expander, panedwindow, scrollbar, scrollview, scale, scrolledtext,
  tabs, notebook, pagestack, tabview, label, badge, progressbar,
  floodgauge, meter, switch, checktoggle, radiotoggle, optionmenu,
  calendar, entry, combobox, spinbox, text, canvas, labeledscale,
  passwordentry, pathentry, timeentry. ~31 widget pages still need
  shots; 4 popup/modal placeholders deferred (`datedialog`,
  `messagebox`, `selectbox` × 2).
- **6F — NOT STARTED.** MP4/GIF for animated widgets: Toast, Tooltip,
  Accordion (animation), Expander, PageStack, FloodGauge, Meter. Needs
  display + recording tool.

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
