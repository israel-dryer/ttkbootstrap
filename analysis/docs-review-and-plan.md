# Documentation Review and Implementation Plan

Tracking document for the docs overhaul started 2026-04-29. Captures observations, decisions, and the phased plan so progress survives across sessions.

---

## Context

### Goals (from the original ask)

1. The API is fully documented in the API reference.
2. The Platform section is fully explained, accurately cross-referenced, and contains everything expected of a UI platform documentation site.
3. Images and image placeholders are filled in where appropriate or removed.
4. Plus: organization, content, language, and platform-specific feature surfacing.

### Documentation model (decided)

The docs use a deliberate **user-guide vs. API-spec** split, in line with how Python, Rust, and Django document themselves:

- `docs/widgets/`, `docs/guides/`, `docs/capabilities/`, `docs/platform/`, `docs/design-system/` — **user guide**: narrative, examples, when-to-use, screenshots.
- `docs/reference/` — **API spec**: rendered from source docstrings via mkdocstrings (`::: module.Class`). No hand-written narrative.

This means reference-page quality is a function of **docstring quality** in `src/`. The spec is durable only if the docstrings are durable.

### Toolchain

- MkDocs (Zensical config in `zensical.toml`), **not** Sphinx.
- Docstrings: plain Markdown, Google style. **No** reST roles or directives (`:func:`, `:param:`, `.. note::`).
- `[project.plugins.mkdocstrings.handlers.python.options]` in `zensical.toml:399-408` sets `docstring_style = "google"`, `heading_level = 3`, `show_signature = true`.
- Public API surface = `_MODULE_EXPORTS` in `src/ttkbootstrap/__init__.py:164-220` and `_TK_EXPORTS` at `:141-153`.

---

## Observations

### A. API Reference (Goal 1)

Coverage by file count is ~84%. Coverage by *content* depends entirely on docstrings.

**Undocumented public exports** (no reference page):

| Category | Names |
|---|---|
| Tkinter re-exports | `Tk`, `Menu`, `Text`, `Canvas`, `TkFrame`, `Variable`, `StringVar`, `IntVar`, `BooleanVar`, `DoubleVar`, `PhotoImage` |
| App | `Window` (alias for `App`), `Shortcut`, `get_shortcuts` |
| Widgets | `MenuBar`, `SideNavItem`, `SideNavGroup`, `SideNavHeader`, `SideNavSeparator`, `Accordion`, `Badge`, `CheckToggle`, `RadioToggle`, `TK_WIDGETS`, `TTK_WIDGETS` |

**Duplicate reference pages** — the same symbol has multiple URLs:

- `reference/widgets/App.md`, `AppShell.md`, `Toplevel.md`, `Style.md` duplicate canonical pages in `reference/app/`, `reference/style/`.
- All 13 dialog pages (`Dialog.md`, `MessageDialog.md`, `MessageBox.md`, `ColorChooser.md`, `ColorChooserDialog.md`, `ColorDropperDialog.md`, `DateDialog.md`, `FontDialog.md`, `FilterDialog.md`, `FormDialog.md`, `QueryDialog.md`, `QueryBox.md`) appear under both `reference/widgets/` and `reference/dialogs/`.

**Deprecated aliases** (`__init__.py:126-139`) have full reference pages but no deprecation marker:
`NavigationView.md`, `NavigationViewItem.md`, `NavigationViewGroup.md`, `NavigationViewHeader.md`, `NavigationViewSeparator.md`.

**Orphan reference subtree** — `docs/reference/capabilities/` (`bind.md`, `pack.md`, `winfo.md`, `grid.md`, `place.md`, `bindtags.md`, `busy.md`, `clipboard.md`, `focus.md`, `grab.md`, `localization.md`, `selection.md`, `signals.md`, `after.md`) describes Tk methods exposed through mixins. Awkward as pure spec; needs a decision (see Open Questions).

**Off-tree files** — `docs/reference/core/app.md`, `docs/reference/core/style.md` are not in nav.

**Nav config issues** in `zensical.toml`:
- `SideNav` listed twice — line 266 and line 289.
- Lines 267-270 alias `NavigationViewItem.md` etc. as "SideNavItem" — confusing because the file is named for the deprecated alias.

### B. Platform Section (Goal 2)

All 14 pages substantive (~2,270 lines). Cross-referencing strong. Split between Platform (mechanics) and Capabilities (framework features) is articulated in `docs/index.md:93-101` and mostly observed.

**Missing topics expected of a desktop UI platform site:**

| Topic | Current state | Action |
|---|---|---|
| Threading & async | Mentioned in `event-loop.md`, `performance.md`. No recipe. | New page: `platform/threading-and-async.md` |
| Accessibility | Absent | New page: `platform/accessibility.md` |
| macOS specifics | Only notarization in `build-and-ship.md` | New page or section: App menu / Cmd vs Ctrl / native fullscreen / Quit / Retina |
| Windows specifics | Largely absent | DPI manifest / dark title bar / taskbar / MSI signing |
| Linux specifics | Absent | X11 vs Wayland / fractional scaling / `.desktop` / AppImage / Flatpak |
| i18n runtime | Only message catalogs | RTL layout / font fallback for CJK & Arabic / locale detection |
| Auto-update | Absent | Pattern guidance or "use 3rd-party" pointer |
| Crash handling & logging | One paragraph in `debugging.md` | Structured logging + uncaught exception handler + dialog-on-crash |
| Native vs custom dialogs | Absent | When `tkinter.filedialog` vs `ttkbootstrap.MessageDialog` |

**Broken cross-reference** — `docs/platform/build-and-ship.md:128` points to `../capabilities/icons-and-imagery.md`; correct path is `../capabilities/icons/index.md`.

### C. Images and Placeholders (Goal 3)

- 65 image files on disk in `docs/assets/{light,dark}/` (60 PNG + 6 MP4 + favicon + 2 logos).
- 50 references resolve correctly. Only **10 of 77** widget pages have screenshots.
- **3 broken paths** to non-existent `docs/_img/`:
  - `docs/widgets/selection/selectbox.md:13-14`
  - `docs/widgets/inputs/scale.md:12-13`
- **15 widget pages** carry an `IMAGE:` text placeholder (mostly layout, navigation, views, dialogs).
- Screenshot generators exist in `docs_scripts/` (7 scripts: button, checkbutton, radiobutton, dateentry, numericentry, spinnerentry, textentry). No CI integration.

### D. User-Guide Audit

**Empty guide files** (0 bytes) linked from `docs/guides/index.md`:
- `docs/guides/dialogs.md`
- `docs/guides/forms.md`
- `docs/guides/tables-and-lists.md`
- `docs/guides/toolbars.md`

**Duplicate concepts across sections:**
- Icons: `guides/icons.md` + `design-system/icons.md` + `capabilities/icons/icons.md`
- Typography: `guides/typography.md` + `design-system/typography.md`
- Theming: `guides/theming.md` + `design-system/custom-themes.md`
- Layout: `guides/layout.md` + `capabilities/layout/index.md` + `capabilities/layout/containers.md`
- Localization: `guides/localization.md` + `capabilities/localization.md` (this pair is the cleanest split)

Suggested canonical homes:
- **Design System** = the *what* (tokens, names, palette, type scale).
- **Guides** = *how to use it in your app*.
- **Capabilities** = *what the framework does for you*.

**Examples** — mixed Tk-vars + signals usage. The framework prefers signals (`docs/index.md:62-65`); examples should lead with signals and offer Tk-vars as a "compatibility" alternative.

**Canonical import** — `import ttkbootstrap as ttk` per the docstring at `__init__.py:7-13`. Audit examples for drift.

**Widget page templates** — `docs/_template/widget-*-template.md` exist; pages mostly conform. Drift should be caught by a structure linter, not by hand.

### E. Cross-Cutting

- `LIBRARY_STRUCTURE.md` at the repo root duplicates information now living in `docs/platform/project-structure.md` and is already drifting. Should be deleted or folded in.
- No "Migrating from v1" or "Migrating from tkinter" guide. Highest-leverage missing user-guide page given `_DEPRECATED_ALIASES`.
- Capabilities ↔ Platform overlap on signals, virtual events, layout — the boundary is documented but not always observed in the prose.

### F. Platform-Specific Features That Need Surfacing

Each lives in two places under the spec/guide split: in the **docstring** (so the spec renders it) AND in the **user-guide** narrative.

| Feature | Docstring needs | User-guide page |
|---|---|---|
| `Shortcuts` `<Mod>` → Cmd on macOS, Ctrl elsewhere | `Shortcuts` class docstring | `platform/platform-differences.md` (new) |
| Native macOS App menu items (About, Preferences, Quit) | `MenuManager`, `App` | `widgets/application/app.md`, macOS section |
| DPI scaling per OS | `App`, `Image` | `platform/images-and-dpi.md` per-OS subsections |
| Dialogs are not native | each dialog class | `widgets/dialogs/index.md` |
| Window decorations / fullscreen | `App`, `Toplevel` | `platform/windows.md` |
| Toast positioning conventions | `Toast` | `widgets/overlays/toast.md` |
| `PathEntry` separator handling | `PathEntry` | `widgets/inputs/pathentry.md` |
| `ContextMenu` macOS Ctrl-click | `ContextMenu` | `widgets/actions/contextmenu.md` |

---

## Plan

Phased by dependency and risk. Phase 1 is trivial cleanup. Phase 2 sets up the spec discipline that everything else depends on. Phases 3–6 are larger content work.

Status legend: `[ ]` pending · `[~]` in progress · `[x]` done · `[-]` deferred.

### Phase 1 — One-line fixes (low risk, high signal)

- [x] **1A.** Removed duplicate `SideNav` entry in `zensical.toml` and moved `SideNavItem`/`Group`/`Header`/`Separator` to alphabetical position next to canonical `SideNav`.
- [x] **1B.** Fixed broken link in `docs/platform/build-and-ship.md:128` (now `../capabilities/icons/index.md`, label updated to "Icons & Images").
- [x] **1C.** Replaced `_img/` paths in `docs/widgets/selection/selectbox.md` (2 occurrences) and `docs/widgets/inputs/scale.md` with the canonical HTML-comment `IMAGE:` placeholder used by other widget pages.
- [x] **1D.** Renamed `NavigationViewItem/Group/Header/Separator.md` → `SideNavItem/Group/Header/Separator.md` (via `git mv`, history preserved). Updated `zensical.toml` paths. `NavigationView.md` (the deprecation redirect) left in place; it's not in nav and Phase 7B will systematize deprecated names.
- [-] **1E.** Deferred. `LIBRARY_STRUCTURE.md` is **not** a duplicate of `docs/platform/project-structure.md` — it's a contributor/AI-context map of `src/ttkbootstrap/` internals (added in PR #974), while project-structure.md is for *user* apps. Leaving as-is for now; revisit later.

### Phase 2 — Make the spec model durable

This is the foundation for Goal 1.

- [x] **2A.** Wired `ruff` `D` rules with Google convention in `pyproject.toml` ([tool.ruff] section). Internal directories blanket-ignored via `[tool.ruff.lint.per-file-ignores]`; currently-dirty public-surface files are listed individually so each entry can be removed once that file's docstrings are brought to spec. `ruff check src/ttkbootstrap` passes today. The 13 priority files cleaned in 2D form the enforced baseline.
- [x] **2B.** Docstring template defined below ("Docstring template" section). Anchored on the existing local style: class docstring carries narrative (purpose, when to use) and `Examples:`; `__init__` docstring carries `Args:` and per-parameter details. mkdocstrings renders both (`merge_init_into_class` is unset → default False), so location follows convention; only content matters. `BaseDataSource` (`src/ttkbootstrap/datasource/base.py:27-53`) is one reference; `Form` (`form.py:111-155`) and `Button.__init__` (`button.py:56-85`) are also strong examples of the local style.
- [-] **2C/2D.** Deferred to a session with a running Tk display for rendered review. All public-surface files now pass `ruff check --select D` with zero suppressions (per-file-ignores list cleared 2026-04-29). Content quality (thin narratives, missing Attributes/Args depth) for the 20 priority symbols remains to be verified against the rendered output.
  - Priority symbols: `App`, `AppShell`, `Toplevel`, `Window`, `Button`, `Label`, `Frame`, `GridFrame`, `PackFrame`, `TextEntry`, `NumericEntry`, `DateEntry`, `Combobox`, `OptionMenu`, `SelectBox`, `TableView`, `TreeView`, `Form`, `Style`, `Bootstyle`, `MessageDialog`, `BaseDataSource`

### Phase 3 — Reference-spec gap close

- [-] **3A.** Skipped per scope decision: Tk re-exports (`Tk`, `Menu`, `Text`, `Canvas`, `TkFrame`, `Variable`, `StringVar`, `IntVar`, `BooleanVar`, `DoubleVar`, `PhotoImage`) point at stdlib classes. Their canonical docs are at python.org; a redundant page in our reference is editorial work for little value. Re-visit if user need surfaces.
- [x] **3B.** Reconciled: only `MenuBar` was actually missing. (`SideNavItem/Group/Header/Separator` existed under their old `NavigationView*` names; renamed in Phase 1D. `Accordion`, `Badge`, `CheckToggle`, `RadioToggle` already had pages — survey notes were over-broad.) Created `docs/reference/widgets/MenuBar.md`.
- [x] **3C.** Created `docs/reference/app/Shortcut.md` and `docs/reference/app/get_shortcuts.md`. Also added the existing `Shortcuts.md` to nav (it had a file but no nav entry). `Window` resolved by mention in `App` class docstring (Phase 2D); separate page deferred — alias inheriting App's spec is sufficient.
- [-] **3D.** Decision (confirmed by user 2026-04-29): leave `TK_WIDGETS` / `TTK_WIDGETS` as public constants for `isinstance()` use, but skip a dedicated reference page. Hand-writing prose for two tuples-of-classes is editorial; mkdocstrings doesn't autodoc them well; the canonical view of their composition is in `src/ttkbootstrap/widgets/__init__.py`.
- [x] **3E.** Resolved duplicate URLs in `reference/widgets/`. Deleted 16 files via `git rm` (preserves history): `App.md`, `AppShell.md`, `Toplevel.md`, `Style.md`, and 12 dialog pages. All were byte-identical to their canonical home in `reference/app/`, `reference/style/`, or `reference/dialogs/` (except `widgets/AppShell.md` which was a redirect-style page with no inbound links, and `widgets/App.md` which was a thinner version of the canonical). No nav entries pointed at any of them; ruff still passes.
- [x] **3F.** No change needed. `reference/capabilities/` pages already follow the spec model — each renders the relevant mixin via `::: ttkbootstrap.core.capabilities.X.YMixin`. They serve users browsing "what can my widget do?" The brief intro paragraph on each page is mechanical (not editorial). Originally flagged for review; no action required.
- [x] **3G.** Done. `docs/reference/core/app.md` and `docs/reference/core/style.md` were both 0-byte stubs with no nav reference. Deleted via `git rm`; empty `docs/reference/core/` directory removed.
- [x] **3H.** Audited and patched `reference/<section>/index.md` pages: `app/index.md` gained `Shortcut` and `get_shortcuts` entries (the latter previously linked to `Shortcuts.md` instead of its own page); `style/index.md` and `reference/index.md` had stale "bootstyle" framing in narrative — replaced with the canonical token vocabulary (`accent`, `variant`, `surface`, etc.); `i18n/index.md` referenced a non-existent "Platform → Localization" page — corrected to "Guides → Localization."

### Phase 4 — Platform section completion (Goal 2)

- [x] **4A.** New page: `platform/threading-and-async.md`. Covers worker thread + `Queue` pattern, `after_idle`, `after_repeat`, and `asyncio` integration trade-offs. Added to nav under Operations.
- [x] **4B.** New page: `platform/platform-differences.md`. Single matrix-style page covering macOS / Windows / Linux differences (Mod key, ContextMenu trigger and backend, Toast position, App quit behavior, window_style, system appearance sync, state directory, native vs themed dialogs). Added to nav.
- [x] **4C.** New page: `platform/accessibility.md`. Keyboard navigation, tab order, focus rings (visual_focus system), contrast guidance, honest screen reader status per OS, practical checklist. Added to nav.
- [x] **4D.** Expanded `platform/images-and-dpi.md` with per-OS sections: macOS Retina (OS-handled, @1x assets), Windows DPI manifest (auto via hdpi=True, Image utility for sizing), Linux X11 fractional scaling (explicit scaling param), Wayland note, scaling summary table, image caching and common pitfalls.
- [ ] **4E.** Expand `platform/build-and-ship.md` with Windows MSI signing, Linux AppImage / `.deb` / Flatpak. (Or explicitly delegate, like the existing Briefcase handoff for macOS.)
- [ ] **4F.** Expand `platform/debugging.md` with structured logging setup, uncaught exception handler, crash dialog pattern.
- [x] **4G.** Added "Native vs custom dialogs" section to `docs/widgets/dialogs/index.md` explaining that ttkbootstrap dialogs are themed Tk windows (not OS-native) and directing users to `tkinter.filedialog` / `tkinter.colorchooser` for native behavior.

### Phase 5 — User-guide cleanup

- [ ] **5A.** Fill the four empty guides (or remove them from nav):
  - `docs/guides/dialogs.md`
  - `docs/guides/forms.md`
  - `docs/guides/tables-and-lists.md`
  - `docs/guides/toolbars.md`
- [ ] **5B.** Deduplicate icon documentation. Pick one canonical home per the *what / how / what-it-does* split (suggest: tokens in Design System, usage in Guides, framework behavior in Capabilities). Make the others link rather than restate.
- [ ] **5C.** Same for typography.
- [ ] **5D.** Same for theming.
- [ ] **5E.** Same for layout / spacing.
- [-] **5F.** Deferred. Library will be rebranded; migration story will be handled as part of that effort rather than as a standalone guide.
- [ ] **5G.** Update widget-page examples to lead with signals; show Tk-vars as a "compatibility" alternative where relevant.
- [~] **5H.** Standardize the canonical import (`import ttkbootstrap as ttk`) across all examples in guides and widgets. Fixed `scrollbar.md` (`tk.Text` → `ttk.Text`) and `menubutton.md` (`from tkinter import Menu` → `ttk.Menu`). Remaining `from ttkbootstrap import X` patterns in guides are intentional named imports (localization helpers `L`, `LV`, `MessageCatalog`, `IntlFormatter`; theming utilities; `Font`) — acceptable alongside `import ttkbootstrap as ttk`.
- [ ] **5I.** Add `tools/check_doc_structure.py` — verifies each `docs/widgets/<category>/<widget>.md` has the required H2s from `docs/_template/widget-<category>-template.md`. Run in CI.

### Phase 6 — Images & screenshot pipeline (Goal 3)

- [ ] **6A.** Decide image policy. Recommended: every widget page that renders something visible has at least one screenshot.
- [ ] **6B.** Generalize `docs_scripts/widgets_*.py` and `widget_*.py` into a single `docs_scripts/render.py` driven by a manifest (YAML or TOML). Replace per-widget scripts with manifest entries.
- [ ] **6C.** Add a `make screenshots` (or `ttkb screenshots`) command.
- [ ] **6D.** Add a CI check: every `docs/widgets/**/*.md` that references an image must have that image on disk. Should have caught the `_img/` breakage.
- [ ] **6E.** Generate screenshots for the 67 widget pages currently without them. Replace the 15 `IMAGE:` placeholders.
- [ ] **6F.** Extend MP4 / GIF use to widgets that animate: Toast, Tooltip, Accordion, Expander, PageStack, FloodGauge, Meter.

### Phase 7 — Polish

- [ ] **7A.** Add admonitions (`!!! note`, `!!! warning`) for platform-specific callouts in user-guide pages (not docstrings).
- [x] **7B.** Created `docs/reference/deprecated.md` listing all 12 aliases from `_DEPRECATED_ALIASES` with replacement names and migration snippet. Added to nav in `zensical.toml` and `reference/index.md`.
- [ ] **7C.** Final sweep: rebuild, click every nav item, search for "TODO" / "TBD" / "coming soon" in `docs/`.

---

## Docstring Template

Local convention: class docstring carries narrative + examples; `__init__` docstring carries `Args:`. mkdocstrings (per `zensical.toml:399-408`) renders both — `merge_init_into_class` is unset, so each appears as its own section on the rendered page. **Don't relocate existing content; fill the gaps.**

### Class docstring

Spec, not user guide. Describe what the class **is** and what it **does** — mechanics, not editorial. Don't write "when to use it," "best practices," or "how it compares to X." Those belong on the user-guide page (`docs/widgets/...`).

```
"""<One-line summary ending with a period.>

<1–2 short paragraphs describing what the class is and how it behaves
mechanically.> No advice, no comparisons, no "when to use." If users
need to choose between this and a sibling class, that's a user-guide
question.

Attributes:
    <name> (<type>): <one-line description>.
    ...

Notes:
    <Behavioral facts not covered above: threading, lifecycle, ordering,
    side effects, cache behavior, etc. Anything that's part of the
    contract.> Only include if there's something to say.

Platform:
    On macOS, ...
    On Windows, ...
    <Only if behavior differs by platform.>

Deprecated:
    Since 2.0. Use `<replacement>` instead. Will be removed in 3.0.
    <Only if applicable.>
"""
```

Examples are **off by default**. The user guide owns examples and screenshots. Add an `Examples:` section to a docstring **only** when one of the following is true:

- The call shape is non-obvious from the signature (decorator, context manager, abstract subclassing pattern, callback signature, unusual nested data structure).
- An ambiguity in the signature (e.g. polymorphic argument types) is best resolved by showing one line of code.

"Construct it and pack it" is not a reason to add an example. Most widget classes will not have `Examples:` blocks.

### `__init__` docstring

```
"""<One-line summary of construction.>

Args:
    <name> (<type>): <description>. Mention defaults in prose, not in the type.
    ...

Other Parameters:
    <kw> (<type>): <description>.
    ...
        (Use Other Parameters for `**kwargs` items expanded from a TypedDict.)

Raises:
    <ExceptionType>: <when it's raised>.
"""
```

### Rules

- **Spec, not user guide.** Describe mechanics. No editorial language: no "best to use when…", no comparisons to sibling classes, no recommendations, no rationale.
- **Plain Markdown only.** No reST roles or directives (`:param:`, `:func:`, `.. note::`).
- **Google style.** mkdocstrings is configured for it (`zensical.toml:400`).
- **Code fences must specify a language** (`python`, `bash`, etc.).
- **Examples must be runnable as-shown** with `import ttkbootstrap as ttk`.
- **One canonical import** in examples: `import ttkbootstrap as ttk`.
- **Don't duplicate Args between class and `__init__`.** Args go on `__init__`.
- **Keep `Attributes:` on the class**, not on `__init__`.
- **Admonitions are allowed but optional.** The `admonition` extension is enabled (`zensical.toml:418`), so `!!! note "Events"` and similar render correctly. Existing docstrings use this convention for `Events:` blocks. Plain prose sections (`Notes:`, `Platform:`) are equally fine — pick one style per docstring and stay consistent with the surrounding file.
- **Don't link to user-guide pages from docstrings.** The spec is self-contained. Cross-links live on the reference page or the user-guide page itself, not inside the source.
- **Don't reference `bootstyle` in descriptive prose.** The `bootstyle` parameter is deprecated (see `_DEPRECATED_ALIASES` and inline DEPRECATED markers in `*Kwargs` TypedDicts). In class-level narrative, describe styling via the canonical tokens — `accent`, `variant`, `density`, `surface`, `show_border`, etc. — typically as "theme-aware styling" or by naming the tokens directly. The `bootstyle` parameter itself can still be marked DEPRECATED in `Other Parameters:` for users who haven't migrated.

---

## Open Questions

1. **`docs/reference/capabilities/` direction (Phase 3F).** Spec for mixins, or move to user-guide? Decision needs to be made before 3F.
2. **`reference/widgets/` deprecated-alias files (Phase 1D vs 3E).** Rename to canonical, or delete entirely once duplicates are removed?
3. **`TK_WIDGETS` / `TTK_WIDGETS` (Phase 3D).** Public API or internal? Currently in `_MODULE_EXPORTS["ttkbootstrap.api.widgets"]`.
4. **Per-OS packaging guidance scope (Phase 4E).** First-party recipes, or "use Briefcase / use PyInstaller" pointers?
5. **Image policy strictness (Phase 6A).** Mandatory for every widget, or judgment call per page?
6. **`Tabs` and `TabView` API status.** ~~Both classes exist in `widgets/composites/tabs/` and have reference + user-guide pages, but neither is in `_MODULE_EXPORTS`.~~ Resolved 2026-04-29: per user direction, made consistent with peer layout widgets. Added `Tabs` and `TabView` to `api/widgets.py` exports and to `__init__.py` `_MODULE_EXPORTS` + TYPE_CHECKING block. `import ttkbootstrap as ttk; ttk.Tabs` now resolves.

---

## Decisions Log

Date — Decision — Rationale.

- 2026-04-29 — Adopted user-guide vs API-spec split as the documentation model. Reference pages stay bare `::: module.Class`; narrative goes in user guide. Spec quality = docstring quality. CI lint enforces it.
- 2026-04-29 — `LIBRARY_STRUCTURE.md` reframed: not a duplicate, serves contributors/AI context. Final disposition pending user decision (1E).
- 2026-04-29 — Image placeholder convention is the HTML-comment block (`<!-- IMAGE: ... -->`) used in layout/navigation widget pages. Visible quote-block placeholders replaced.
- 2026-04-29 — Docstring location convention: class docstring carries narrative + `Attributes:` + `Examples:`; `__init__` carries `Args:`. Both render via mkdocstrings (`merge_init_into_class` unset). Don't relocate existing content; fill gaps in the class docstring.
- 2026-04-29 — Phase 2 sequencing changed: 2B → 2D (in batches) → 2A. Tooling (2A) added at the end so CI doesn't go red on day 1.
- 2026-04-29 — Docstring template tightened: spec, not user guide. No "when to use," no comparisons, no editorial. Mechanics + minimal examples. User-guide content stays in `docs/widgets/...`, `docs/guides/...`.
- 2026-04-29 — Examples in docstrings made off-by-default. Only included when the call shape is non-obvious or signature ambiguity needs a one-liner to resolve. The user guide owns examples and screenshots.
- 2026-04-29 — `bootstyle` is deprecated and should not appear in descriptive prose. Class narratives describe styling via the canonical tokens (`accent`, `variant`, etc.). The deprecated `bootstyle` parameter itself is still marked DEPRECATED in argument docs for users who haven't migrated.
- 2026-04-29 — Phase 2A landed. `ruff` `D` rules with Google convention enforced via `[tool.ruff]` in `pyproject.toml`. Currently-dirty public-surface files use per-file ignores; each entry is removed when that file's docstrings conform. Internal directories (`builders/`, `mixins/`, `internal/`, `parts/`, `capabilities/`, `cli/`, `assets/`) are blanket-ignored. New files in non-ignored directories are linted from day 1.
- 2026-04-29 — `Tabs` and `TabView` promoted to public API exports per user direction (consistent with peer layout widgets `PageStack`, `Notebook`, `SideNav`, `Toolbar`). Added to `api/widgets.py` and `__init__.py` `_MODULE_EXPORTS` + TYPE_CHECKING block.
- 2026-04-29 — `TK_WIDGETS` / `TTK_WIDGETS` left public but with no dedicated reference page. Same call applies to Tk re-exports (`Tk`, `Variable`, `StringVar`, etc.) — canonical Python docs already cover them; a redundant page in our reference is editorial work for little value.

---

## Per-Symbol Docstring Status (Phase 2C/2D tracker)

Surveyed 2026-04-29. "Gap" describes what's missing relative to the template; the existing `__init__` Args layout is the local convention and is preserved.

Under the tightened template, **no `Examples:`** is the default. Most rows now reduce to: confirm class narrative is mechanical (not editorial), confirm `Args:` is complete, confirm `Attributes:` covers public attributes.

| Symbol | Source | Class docstring | `__init__` Args | Gap | Status |
|---|---|---|---|---|---|
| `BaseDataSource` | `datasource/base.py` | rich | yes | none — reference for abstract-subclass pattern; example is justified | [x] |
| `Toplevel` | `runtime/toplevel.py` | multi-section | yes | done — added `Platform:` (Windows/X11/Aqua), removed construct-and-mainloop example | [x] |
| `AppShell` | `widgets/composites/appshell.py` | multi-section | yes | done — removed example (covered by `add_page` docs and user guide) | [x] |
| `Form` | `widgets/composites/form.py` | rich | yes | done — removed duplicated `Args:` from class docstring | [x] |
| `GridFrame` | `widgets/primitives/gridframe.py` | multi-section | yes | none — verified on-spec; example shows non-obvious auto-placement and is justified | [x] |
| `PackFrame` | `widgets/primitives/packframe.py` | multi-section | yes | none — verified on-spec; example shows non-obvious auto-placement and is justified | [x] |
| `TextEntry` | `widgets/composites/textentry.py` | multi-section | yes | none — verified on-spec | [x] |
| `NumericEntry` | `widgets/composites/numericentry.py` | multi-section | yes | none — verified on-spec | [x] |
| `DateEntry` | `widgets/composites/dateentry.py` | multi-section | yes | none — verified on-spec | [x] |
| `SelectBox` | `widgets/composites/selectbox.py` | brief | yes | none — verified on-spec (brief is fine, it's mechanical) | [x] |
| `Style` | `style/style.py` | multi-section | yes | none — verified on-spec | [x] |
| `MessageDialog` | `dialogs/message.py` | multi-section | yes | done — fixed doubled summary, removed editorial advice, mentioned `show()`/`.result` call shape, updated `bootstyle` references in Args | [x] |
| `App` | `runtime/app.py` | multi-section | yes | done — added `Platform:` section, added missing `window_style` to `__init__` Args | [x] |
| `Window` | (alias for `App`) | inherits | inherits | done — alias acknowledged in `App` class docstring; reference page deferred to Phase 3C | [x] |
| `OptionMenu` | `widgets/primitives/optionmenu.py` | multi-section | yes | done — removed duplicated Events admonition from `__init__`, neutralized "Bootstyle icon spec" wording | [x] |
| `TableView` | `widgets/composites/tableview/` | multi-section | extensive | done — improved class summary; `__init__` is fine | [x] |
| `Button` | `widgets/primitives/button.py` | one-liner | extensive | done — added 2-sentence mechanical narrative to class docstring | [x] |
| `Label` | `widgets/primitives/label.py` | one-liner | extensive | done — added 2-sentence mechanical narrative to class docstring | [x] |
| `Frame` | `widgets/primitives/frame.py` | one-liner | extensive | done — added 2-sentence mechanical narrative to class docstring | [x] |
| `Combobox` | `widgets/primitives/combobox.py` | one-liner | extensive | done — added 2-sentence mechanical narrative to class docstring | [x] |
| `TreeView` | `widgets/primitives/treeview.py` | one-liner | extensive | done — added 2-sentence mechanical narrative to class docstring | [x] |
| `Bootstyle` | `style/bootstyle.py` | brief | n/a (functions) | done — clarified class docstring (handles accent/variant + deprecated bootstyle), updated module summary | [x] |
