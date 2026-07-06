# CLAUDE.md

Guidance for working in the ttkbootstrap repository.

## What this is

ttkbootstrap is a theming extension for tkinter/ttk: it generates modern,
flat, Bootstrap-inspired themes on demand and adds a `bootstyle` keyword
API to ttk widgets. Pure Python; the only runtime dependency is Pillow
(used for image-based widget assets). Public API entry point is
`src/ttkbootstrap/__init__.py`, typically imported as `import ttkbootstrap as ttk`.

- Package version / metadata: `pyproject.toml` (src layout, `requires-python >=3.10`).
- Docs site: mkdocs (`mkdocs.yml`, `docs/`), published to readthedocs.

## Direction: 2.0 cleanup (read before large changes)

The active initiative is a **2.0 cleanup/consolidation release — no new
features.** Goals: remove cruft, standardize/normalize the API (aggressive/
breaking is OK when meaningful, paired with a migration path), fix memory leaks
and theme-switch perf, make user-defined custom styles easy, and overhaul the
docs. ttkbootstrap stays a **styling extension for vanilla tkinter** — not a
widget library (the forward-looking framework is a separate project, bootstack).

The full worklist (locked decisions + workstreams) lives in
**`development/2_0_plan.md`**, and the integration branch is **`2.0`** (cut PRs
against it, not `master`). Headlines: mixin-hybrid API (replace the import-time
monkey-patch), single canonical `bootstyle` string (no tuple/list/alt-order),
semantic-anchor theme model, deterministic version-stamped theme walk +
image-cache cleanup (mechanisms borrowed from bootstack, not its API), and a
centralized compat quarantine for all legacy normalization + deprecation
warnings. Consult that doc before starting 2.0 work.

**Current handoff state** (read `development/2_0_handoff.md` first): all the
independent cleanup slices are **merged** into `2.0` — deprecated top-level shims
removed + headless/demo test split (#1068), public/internal split (#1069),
widget lifecycle-leak fixes (Workstream B, #1070), `FloodgaugeLegacy` runtime
`DeprecationWarning` (#1071), and the `examples/` `test_`-prefix rename (#1072).
The engine keystone (Workstream A) is now in progress: the design is locked in
`development/2_0_engine_design.md`, and **PR 1 — the repaint engine** (version
-stamped theme walk replacing `Publisher`, lazy per-theme style rebuild,
single-root `RuntimeError`) is **merged** into `2.0` (#1073). **PR 2** — the
content-addressed image cache (`Style._image_cache` + `_get_or_create_image` +
`clear_image_cache`; per-builder `theme_images` leak removed) — is **merged**
into `2.0` (#1074). That **completes the engine (Workstream A) keystone**.
**PR 3** — the mixin API (Workstream C) — is **merged** into `2.0` (#1075): the
import-time monkey-patch is retired in favor of concrete
`BootMixin`/`AutoStyleMixin` subclasses re-exported from `__init__.py`, plus
`bootify`/`apply_bootstyle`/opt-in `enable_global_api`; the ~450-line
`TYPE_CHECKING` stub block + `__init__.pyi` are deleted. **PR 4** — the `style/`
package split (Workstream G) — is **merged** into `2.0` (#1076): `style.py`
became a `style/` package (`theme`/`builders_tk`/`builders_ttk`/`engine`/
`bootstyle`) via a pure, behavior-preserving move; `ttkbootstrap.style` stays a
valid public path (no shim). Design pass: `development/2_0_style_split_design.md`.
**PR 5** — the public style-construction toolkit (Workstream I, Tier 1) — is
**merged** into `2.0` (#1077): new `style/assets.py` (`Assets` facade —
`circle`/`rect`/`rounded_rect` recipes + an `image()` escape hatch wrapping PR
2's image cache, with keys *derived* from the render inputs and bootstack's
snapped/oversampled render pipeline) + `style/layout.py` (`El`/`layout`,
`image_element`, `statespec`/`state_map`, `StyleName`), re-exported from
`ttkbootstrap.style` and top-level `ttkbootstrap`. The scale + radiobutton
builders are migrated onto it as the acceptance proof. Design pass:
`development/2_0_toolkit_design.md`. The held **PR 6** (asset/layout fast-follow on
`feat/2.0-pr6-toolkit-migration`) was **superseded**: its hand-drawn glyphs
looked poor, so 2.0 instead **renders glyph-shaped assets from a vendored
Bootstrap Icons font** (metrics-based fit ported from bootstack; reuses the PR-5
pipeline + PR-2 cache; no new pip dep), per the API-locked design in
`development/2_0_icons_design.md`. **PR 6a** — the icon engine — is **merged** into
`2.0` (#1079): vendored `assets/icons/` font + `style/icons.py` (`IconRenderer`) +
`Assets.icon` + public `Icon` atom / `icon_element` state→icon sugar, re-exported
from `ttkbootstrap.style` and top-level `ttkbootstrap`; no builder changes, suite
89 passed. Render tuning (icon-specific 6×/3×/1× supersample + gentle 0.5/50
sharpen) and `record-circle-fill` for radio-on were settled via a live visual
spot-check; `examples/icon_preview.py` is the tool. **PR 6b** — the glyph-builder
migration — is **merged** into `2.0` (#1080): check/radio/toggle×2/date/arrows/
sizegrip wired onto `a.icon`/`icon_element` (six `create_*_assets` glyph methods
deleted), the held branch's geometric/`layout` cleanup landed, and the public
style-registration path added (`register_style` + `layout()` auto-registers — the
PR-6a finding). Two light↔dark spot-check rounds settled the arrows on solid
`caret-*-fill` (incl. menubutton + datepicker header), toggle sizing, and
`calendar3`; suite 92. That completes the Workstream I icon work. **Historical next:** an
optional small visual-polish PR (value/asset tweaks — see
`development/2_0_handoff.md` "FOLLOW-UP"), then theme/anchor (E) + bootstyle
canonical (D), each with a design pass first. Proceed PR by PR per the design doc;
don't exceed a PR's scope without revisiting it.

Recolorable raster widget assets (#1081), the modular `StyleBuilderTTK`
registry (#1082), and scaling/asset-geometry normalization (#1083) are now also
merged into `2.0`; the expected suite is 177 tests. The focused private color
ramps and `StyleBuilderTTK` helpers (#1085, merge commit `b7872a98`, per
`development/2_0_color_helpers_design.md`) are now also **merged** into `2.0`;
the expected suite is 189 tests. The fast-follow color-math PR (#1087, merge
commit `0218aba3`, per `development/2_0_color_math_followup_design.md`) is now
also **merged** — it retired the last 10 ad-hoc HSV/alpha sites onto mix-based
`shade`/`tint`/`mute` helpers (the AST guard now enforces zero raw color math in
ttk recipes); `elevate` and `input_bg` from the original stub were **dropped/
deferred to Workstream E** after ground truth invalidated them. Expected suite is
191 tests. **Workstream E (theme/anchor) is now COMPLETE** — the semantic-anchor
`Theme` model, curated 15-family/30-theme catalog, `install_legacy_themes()` +
16-key adapter, `Colors` resolved view + ramp addressing, the hue-correct
`inputbg` fix, and the ttkcreator `Theme` rework all merged (PRs #1088/#1089/
#1090; default theme is now `bootstrap-light`; expected suite 211). Design in
`development/2_0_theme_anchor_design.md`; migration guide (for the Workstream-H
docs rewrite) in `development/2_0_theme_migration.md`. **Workstream D (canonical
bootstyle grammar) is now COMPLETE** — three PRs merged into `2.0` (design in
`development/2_0_bootstyle_grammar_design.md`): D1 #1091 (closed-vocab tokenizer
replacing the substring regex + loud failure on unknown tokens; single vocab
source of truth in `constants.py`; new `style/_compat.py` quarantine with
`set_bootstyle_strict`/`TTKBOOTSTRAP_STRICT`), D2 #1092 (migrated every
first-party tuple caller — meter/dateentry/tooltip/datepicker + the two demos —
to canonical strings, then turned the tuple `DeprecationWarning` on), D3 #1093
(generated `BootStyle` `Literal` (107 strings) + reference table
`development/2_0_bootstyle_reference.md` from vocab × registry, via
`tools/generate_bootstyle_reference.py`, with sync tests). `BootType` fixed
(`round` added; `toggle`/`toolbutton` moved to the new `BootBase`); dead
`focus`/`input` dropped. Expected suite ~263 (excl. the known `nl.msg`
localization env flake). **Current:** the remaining 2.0 headliner is the docs
overhaul (Workstream H) — fold in the bootstyle reference and
`development/2_0_theme_migration.md`.

## Repository layout

```
src/ttkbootstrap/
  __init__.py        # public exports; defines the concrete BootMixin/AutoStyleMixin widget
                     #   subclasses (e.g. `class Button(BootMixin, ttk.Button)`) that carry the
                     #   `bootstyle`/`autostyle` api. No import-time monkey-patch (2.0, PR 3) —
                     #   opt into it via enable_global_api().
  style/             # THE CORE — theme/style engine package (see below). Split from the old
                     #   style.py in 2.0 (PR 4); public import path `ttkbootstrap.style` unchanged.
                     #   theme.py (Colors, ThemeDefinition), builders_tk.py (StyleBuilderTK),
                     #   builders_ttk.py (StyleBuilderTTK — the bulk), engine.py (Style),
                     #   bootstyle.py (Keywords, Bootstyle, tokenizer, BootMixin/AutoStyleMixin, delivery),
                     #   _compat.py (2.0 Workstream D/F quarantine: normalize_bootstyle, strictness).
  window.py          # Window / Toplevel classes
  constants.py       # constants (PRIMARY, SUCCESS, ...) + the single bootstyle vocab source of
                     #   truth: BOOTSTYLE_* tuples, BootColor/BootType/BootBase, generated BootStyle
  colorutils.py      # color math (Colors helpers, make_transparent, contrast)
  themes/standard.py # STANDARD_THEMES dict: every built-in theme's color definitions
  themes/user.py     # user-defined themes
  widgets/           # CANONICAL custom widgets: dateentry, meter, floodgauge, tableview,
                     #   scrolled, tooltip, toast, labeledscale
  dialogs/           # Messagebox, Querybox, colorchooser, datepicker, fontdialog, etc.
  localization/      # msgcat-based i18n (msgs.py holds translations)
  internal/          # PRIVATE plumbing (no underscore in the name): publisher.py, utility.py.
                     #   No back-compat guarantee. See "internal/ vs public" below.
  utility.py         # PUBLIC utility funcs: enable_high_dpi_awareness, scale_size
  publisher.py       # deprecation shim -> internal/publisher.py (warns; removed in 3.0)
tests/               # HEADLESS pytest only (4 test_*.py + conftest.py). CI-runnable.
examples/            # interactive mainloop() demos (moved out of tests/ in #1068)
docs/, gallery/, cookbook/   # documentation and examples
```

### internal/ vs public (important — new in 2.0)

Implementation-detail modules live in **`src/ttkbootstrap/internal/`** (the
name is `internal`, *not* `_internal`). Anything under it has no
back-compat guarantee.

When moving something public→internal, leave a thin shim at the old public path
that re-exports from `internal/` and emits a `DeprecationWarning` ("…moved to
ttkbootstrap.internal.X; removed in 3.0") — e.g. `ttkbootstrap.publisher`. For a
module that stays public but sheds internal helpers (e.g. `utility.py`), forward
the moved names via module-level `__getattr__` with the same warning instead of
a whole shim module. **Importing `ttkbootstrap` itself must stay warning-free**
— shims warn only when an old path is actually used.

The older top-level shims (`ttkbootstrap.scrolled/tableview/toast/tooltip`,
`dialogs/dialogs.py`) were **removed** in #1068 — import from
`ttkbootstrap.widgets.<name>` / `ttkbootstrap.dialogs`. Edit real
implementations in `src/ttkbootstrap/widgets/`, never a shim.

## The style engine (`style/` package)

Everything visual flows through here. Split from the old monolithic `style.py`
in 2.0 (PR 4) into a `style/` package; `ttkbootstrap.style` re-exports the full
surface, so the import path is unchanged. The submodules layer downward
(`theme` → `builders_tk` → `builders_ttk` → `engine` → `bootstyle`), with a few
function-local back-edge imports. Key classes (by module):

- **`Style`** (`engine.py`) — singleton (`Style.get_instance()`), subclasses
  `ttk.Style`. Owns theme definitions and the active theme. `theme_use()`
  switches themes and runs the version-stamped theme walk (PR 1) that repaints
  only stale mounted widgets — styles rebuild lazily/O(mounted), not all up front.
- **`StyleBuilderTTK`** (`builders_ttk.py`) — holds `create_*_style(colorname)`
  methods (e.g. `create_button_style`, `create_outline_toolbutton_style`). These
  build a ttk style and call `_register_ttkstyle()`.
- **`StyleBuilderTK`** (`builders_tk.py`) — styles legacy `tk.*` widgets (Menu,
  Text, Canvas, …).
- **`Colors` / `ThemeDefinition`** (`theme.py`) — the color model + theme
  container.
- **`Bootstyle`** (`bootstyle.py`) — the resolver: `update_ttk_widget_style()` maps a
  `bootstyle=`/`style=` string to a built ttk style. Two delivery paths feed it
  (2.0, PR 3): the default `BootMixin`/`AutoStyleMixin` concrete subclasses
  (in `__init__.py`), and the opt-in global monkey-patch
  (`enable_global_api()` → `setup_ttkbootstrap_api()`). As of Workstream D the
  parser is a real **tokenizer over a closed vocabulary** (fixed slot order
  `[color-][modifier-]<base-type>[-orient]`), not a substring regex: unknown
  tokens fail loudly (warn by default; `set_bootstyle_strict(True)` /
  `TTKBOOTSTRAP_STRICT=1` raises). It handles **two input dialects** —
  dash/space bootstyle strings (loud) vs already-built dotted ttk style names
  from the theme walk / `Style.configure` / custom styles (lenient). The vocab
  lives once in `constants.py`; the reference (`BootStyle` `Literal` + docs
  table) is generated by `tools/generate_bootstyle_reference.py`, sync-tested.
  Legacy forms (tuple/list bootstyle) are quarantined in `style/_compat.py`
  (warn-and-normalize through 2.x, removed in 3.0).

### Lazy style building — the model to keep in mind

Styles are built **on demand**, not up front. The base `TButton`, `TEntry`,
etc. are only configured the first time a widget that needs them is created
(or via `_create_ttk_styles_on_theme_change` for already-registered styles).
At theme load, `create_default_style()` configures the root `.` style plus a
small set of always-needed styles.

Consequence (and a real past bug, #1062): native/third-party ttk widgets the
app never instantiates directly — e.g. the `ttk::button` widgets inside Tk's
file dialog on Linux — fall back to the bare clam look if no corresponding
ttkbootstrap widget has been created. The fix pattern is to build the needed
base style eagerly in `create_default_style()`.

## Gotchas

- **`Style` is a process-wide singleton (`Style.instance`) tied to the first Tk
  root.** Creating and destroying separate roots in one process leaves the
  singleton mis-bound, so later theming silently no-ops. Tests share ONE root
  via the `root` fixture in `tests/conftest.py` — see "Writing tests" below.
  (Properly fixing the singleton is part of the deferred `style.py` engine
  rewrite.)
- **Themes are clam-derived** (`theme_create(name, TTK_CLAM)`). An unstyled
  base ttk style shows clam's default appearance until ttkbootstrap configures it.

## Dev environment & commands

A virtualenv with an editable install lives at `.venv/` (Python 3.x on macOS;
`python` on PATH resolves to it). The package is also importable with
`PYTHONPATH=src`.

- Run the headless suite: `python -m pytest -q` (config in `pyproject.toml`
  under `[tool.pytest.ini_options]`; `testpaths = ["tests"]`).
- pytest is installed in `.venv`. If a fresh env lacks it: `pip install pytest`.
- The interactive demos in `examples/` call `mainloop()` and need a display —
  they are NOT collected by pytest.
- Build docs: `mkdocs serve` (deps in `requirements.txt`).

### Writing tests

`tests/` is headless-only. New GUI tests should **take the `root` fixture** from
`tests/conftest.py` (one shared session root; widgets and theme are reset per
test) instead of creating their own `ttk.Window` — creating your own root
re-triggers the singleton mis-binding above. Query a built style's value with
`app.tk.call("ttk::style", "lookup", "<Style>", "-<option>")`. Put any
interactive/visual demo in `examples/`, not `tests/`.

## Conventions

- Match the style of the file you're editing (comment density, naming).
- Custom widgets that need image assets generate them through the style
  builder / Pillow pipeline; favor native ttk/clam mechanisms over images
  where both are viable (perf and cross-platform consistency).
- Commit messages: imperative subject; reference the issue (`fixes #NNNN`)
  where applicable.
- Branch + PR per change. **2.0 cleanup work targets the `2.0` branch**;
  maintenance/bugfixes target `master`.
