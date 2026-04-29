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

- [ ] **2A.** Add a docstring-coverage tool (`interrogate`, `ruff D`, or `pydocstyle`) configured to lint **only** the public surface (the symbols in `_MODULE_EXPORTS` and the modules they live in). Add to dev requirements and CI.
- [ ] **2B.** Define a docstring template for the public API:
  - One-line summary
  - Longer description (1–3 paragraphs)
  - `Args:`, `Attributes:`, `Returns:`, `Raises:`, `Examples:` (Google style)
  - For deprecated symbols: `Deprecated:` section with replacement and removal version
  - For platform-specific behavior: a "Platform notes" paragraph (plain Markdown, no admonitions in docstrings — they don't render the same)
- [ ] **2C.** Build the docs locally and review the rendered reference for the 20 most-used symbols. Spot the thin docstrings:
  - `App`, `AppShell`, `Toplevel`, `Window`
  - `Button`, `Label`, `Frame`, `GridFrame`, `PackFrame`
  - `TextEntry`, `NumericEntry`, `DateEntry`, `Combobox`, `OptionMenu`, `SelectBox`
  - `TableView`, `TreeView`, `Form`
  - `Style`, `Bootstyle`
  - `MessageDialog`, `BaseDataSource`
- [ ] **2D.** Fix any thin docstrings found in 2C in source (`src/ttkbootstrap/...`). Track per-symbol completion below.

### Phase 3 — Reference-spec gap close

- [ ] **3A.** Decide handling for stdlib re-exports. Recommended: single page `docs/reference/app/tk-reexports.md` listing `Tk`, `Menu`, `Text`, `Canvas`, `TkFrame`, `Variable`, `StringVar`, `IntVar`, `BooleanVar`, `DoubleVar`, `PhotoImage` with one-liners and links to Python's own docs.
- [ ] **3B.** Add reference pages for missing widgets: `MenuBar`, `SideNavItem`, `SideNavGroup`, `SideNavHeader`, `SideNavSeparator`, `Accordion`, `Badge`, `CheckToggle`, `RadioToggle`. Each is `::: module.Name` after the docstring is spec-grade.
- [ ] **3C.** Add reference pages for `Window`, `Shortcut`, `get_shortcuts`. (`Window` may just point at `App`.)
- [ ] **3D.** Decide on `TK_WIDGETS` / `TTK_WIDGETS` constants — either reference page (probably under `reference/style/` or a new `reference/constants/`) or make them private.
- [ ] **3E.** Resolve duplicate URLs in `reference/widgets/`. Delete `App.md`, `AppShell.md`, `Toplevel.md`, `Style.md`, and the 13 dialog pages from `reference/widgets/`. Update `zensical.toml` so the Widgets nav doesn't duplicate App/Style/Dialogs entries.
- [ ] **3F.** Decide what `docs/reference/capabilities/` is (see Open Questions). Either:
  - Convert each page to `::: ttkbootstrap.core.mixins.X` for the mixin that exposes those Tk methods, **or**
  - Move the content to `docs/capabilities/` as user-guide pages and remove `reference/capabilities/`.
- [ ] **3G.** Decide what `docs/reference/core/app.md` and `docs/reference/core/style.md` are. They aren't in nav. Promote, delete, or document why they exist.
- [ ] **3H.** Audit `docs/reference/<section>/index.md` pages — under spec mode these are the navigation surface. They should be navigable maps (alphabetized, grouped, one-line summaries), not placeholder lists.

### Phase 4 — Platform section completion (Goal 2)

- [ ] **4A.** New page: `platform/threading-and-async.md`. Covers worker thread + `Queue` pattern, `app.after_idle`, `asyncio` integration trade-offs.
- [ ] **4B.** New page: `platform/platform-differences.md`. Single matrix-style page covering macOS / Windows / Linux differences (Cmd vs Ctrl, App menu, DPI, fullscreen, Toast position, path separators, native dialogs). Cross-linked from every affected widget and reference page.
- [ ] **4C.** New page: `platform/accessibility.md`. Keyboard navigation, focus order, screen reader status per OS, contrast, focus rings.
- [ ] **4D.** Expand `platform/images-and-dpi.md` with per-OS subsections covering @2x assets, fractional scaling on Linux, Retina on macOS, DPI manifest on Windows.
- [ ] **4E.** Expand `platform/build-and-ship.md` with Windows MSI signing, Linux AppImage / `.deb` / Flatpak. (Or explicitly delegate, like the existing Briefcase handoff for macOS.)
- [ ] **4F.** Expand `platform/debugging.md` with structured logging setup, uncaught exception handler, crash dialog pattern.
- [ ] **4G.** Add a "native vs custom dialogs" subsection to `widgets/dialogs/index.md` calling out that `MessageDialog`, `ColorChooser`, etc. are not OS-native; users wanting native file pickers should use `tkinter.filedialog`.

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
- [ ] **5F.** New page: `guides/migrating.md`. Covers v1 → v2 (deprecated aliases from `_DEPRECATED_ALIASES`) and tkinter → ttkbootstrap.
- [ ] **5G.** Update widget-page examples to lead with signals; show Tk-vars as a "compatibility" alternative where relevant.
- [ ] **5H.** Standardize the canonical import (`import ttkbootstrap as ttk`) across all examples in guides and widgets. Search for `import tkinter`, `from ttkbootstrap import`.
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
- [ ] **7B.** Add a "Deprecated names" page under API Reference listing every alias in `_DEPRECATED_ALIASES` with replacement and planned removal version. Auto-generate if possible.
- [ ] **7C.** Final sweep: rebuild, click every nav item, search for "TODO" / "TBD" / "coming soon" in `docs/`.

---

## Open Questions

1. **`docs/reference/capabilities/` direction (Phase 3F).** Spec for mixins, or move to user-guide? Decision needs to be made before 3F.
2. **`reference/widgets/` deprecated-alias files (Phase 1D vs 3E).** Rename to canonical, or delete entirely once duplicates are removed?
3. **`TK_WIDGETS` / `TTK_WIDGETS` (Phase 3D).** Public API or internal? Currently in `_MODULE_EXPORTS["ttkbootstrap.api.widgets"]`.
4. **Per-OS packaging guidance scope (Phase 4E).** First-party recipes, or "use Briefcase / use PyInstaller" pointers?
5. **Image policy strictness (Phase 6A).** Mandatory for every widget, or judgment call per page?

---

## Decisions Log

Date — Decision — Rationale.

- 2026-04-29 — Adopted user-guide vs API-spec split as the documentation model. Reference pages stay bare `::: module.Class`; narrative goes in user guide. Spec quality = docstring quality. CI lint enforces it.
- 2026-04-29 — `LIBRARY_STRUCTURE.md` reframed: not a duplicate, serves contributors/AI context. Final disposition pending user decision (1E).
- 2026-04-29 — Image placeholder convention is the HTML-comment block (`<!-- IMAGE: ... -->`) used in layout/navigation widget pages. Visible quote-block placeholders replaced.

---

## Per-Symbol Docstring Status (Phase 2C/2D tracker)

Filled out as Phase 2 progresses.

| Symbol | Source location | Status | Notes |
|---|---|---|---|
| `App` | `runtime/app.py` | [ ] | |
| `AppShell` | `widgets/composites/appshell.py` | [ ] | |
| `Toplevel` | `runtime/toplevel.py` | [ ] | |
| `Button` | `widgets/primitives/button.py` | [ ] | |
| `Label` | `widgets/primitives/label.py` | [ ] | |
| `Frame` | `widgets/primitives/frame.py` | [ ] | |
| `GridFrame` | `widgets/primitives/gridframe.py` | [ ] | |
| `PackFrame` | `widgets/primitives/packframe.py` | [ ] | |
| `TextEntry` | `widgets/composites/textentry.py` | [ ] | |
| `NumericEntry` | `widgets/composites/numericentry.py` | [ ] | |
| `DateEntry` | `widgets/composites/dateentry.py` | [ ] | |
| `Combobox` | `widgets/primitives/combobox.py` | [ ] | |
| `OptionMenu` | `widgets/primitives/optionmenu.py` | [ ] | |
| `SelectBox` | `widgets/composites/selectbox.py` | [ ] | |
| `TableView` | `widgets/composites/tableview/` | [ ] | |
| `TreeView` | `widgets/primitives/treeview.py` | [ ] | |
| `Form` | `widgets/composites/form.py` | [ ] | |
| `Style` | `style/style.py` | [ ] | |
| `Bootstyle` | `style/bootstyle.py` | [ ] | |
| `MessageDialog` | `dialogs/message.py` | [ ] | |
| `BaseDataSource` | `datasource/base.py` | [ ] | |
