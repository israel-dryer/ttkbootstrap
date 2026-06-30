# ttkbootstrap 2.0 — Session Handoff

> Living handoff for the 2.0 cleanup. Update at the end of each working session.
> Pair with `development/2_0_plan.md` (the durable worklist) and `CLAUDE.md`.

_Last updated: 2026-06-29 (scaling and asset-geometry normalization approved,
implemented, and visually approved on `refactor/2.0-scaling`; open as draft PR
#1083 against `2.0`.)_

## Where we are

Integration branch: **`2.0`** (cut all 2.0 PRs against it, not `master`).
Expected suite on `2.0`: **147 passed**, headless, order-independent. Expected
after the scaling branch: **177 passed**. On this machine Python 3.12 reports
**176 passed / 1 environment failure** because its Tcl install cannot read
`tk8.6/msgs/nl.msg`; excluding the six-test localization module gives **171
passed**.

The engine keystone (Workstream A) is **complete and merged**: PR 1 (repaint,
#1073) + PR 2 (content-addressed image cache, #1074). **PR 3 — the mixin API
(Workstream C)** is **merged** (#1075). **PR 4 — the `style/` package split
(Workstream G)** is **merged** (#1076; pure move, see "PR 4" below). **PR 5 —
the style-construction toolkit (Workstream I, Tier 1)** is **merged** (#1077; see
"PR 5" below). **PR 6a — the icon engine (Workstream I, Tier 1.5)** is **merged**
(#1079; see "PR 6a — MERGED" below).

**PR 6b is MERGED (#1080)** — the icon engine is wired into every glyph builder,
the geometric/layout cleanup landed, and the public registration path is in. That
completes the Workstream I icon work for 2.0.

**The recolorable raster-assets PR is MERGED (#1081).** At that merge the
expected suite was 104 tests, and the light↔dark manual gate passed. See the
implementation summary immediately below.

**PR #1082 is MERGED.** `2.0` now includes the 161-line coordinator, frozen
registry, and 22 widget-family modules. Merge commit: `fa1cede8`.

**Current actionable → review and merge draft PR #1083.** Branch:
`refactor/2.0-scaling`, cut from `2.0` at `fa1cede8`; implementation commit
`b491a0be`. Approved design: `development/2_0_scaling_design.md`. Automated and
human gates pass.

**Next after scaling:** design a focused Workstream E slice: cheap private ramps
plus only the builder helpers ttkbootstrap needs (`active`, `pressed`,
`border`, `disabled`, and
`on_color`). Keep those helpers on `StyleBuilderTTK`; defer a public palette API
unless a simple concrete need emerges. Canonical bootstyle grammar (D) follows
later with its own design pass.

## Scaling and asset geometry — DRAFT PR #1083, VISUALLY APPROVED

Approved decisions: public size-bearing `Assets`/Icon APIs take logical UI
units; `IconRenderer.render()` remains a physical-pixel leaf; final
layout-facing images keep exact dimensions with no even snap; #1081 geometry is
locked at checkbox/radio 18×18, switches 38×18, scale thumb 22×22 and track
12×6, progressbar thickness 8/4/12, and scrollbar thumb 18×8 at 100%.

- New private `style/scaling.py`: one service attached to the Tk root; 96-DPI
  Windows/X11 and 72-DPI Aqua baselines; nominal quarter-step normalization;
  round-half-away conversion; direct source-pixel conversion; no global state.
- `Style`, both builders, public `utility.scale_size`, `Assets`, icons, and
  recolored rasters share that service. `Window(scaling=...)` remains applied
  before `Style` and the first lazy build. Windows stays system-DPI-aware;
  per-monitor-v2/live rebuilds remain out of scope.
- Size-bearing toolkit inputs are logical. Builders no longer pre-scale asset
  inputs. `icon_element` also scales numeric border/padding/width/height once.
  Exact odd image frames are preserved; the icon renderer owns its physical
  frame normalization.
- Element manifest v2 records `source_size` separately from approved logical
  `size`, `border`, and `padding`. Rotations transform logical metadata with the
  pixels. Cache keys remain based on final physical dimensions and colors.
- Tk-facing builder padding, borders, focus/insert widths, sash and arrow
  geometry, progress/floodgauge thickness, Treeview geometry, and legacy-tk
  widths now scale once. AST guards reject new unscaled numeric builder geometry
  and pre-scaled logical toolkit inputs.
- Verification: focused scaling/toolkit/icon/recolor suite **68 passed**;
  expected full suite **177 tests**; local full result **176 passed / 1 known Tcl
  `nl.msg` environment failure**; excluding localization **171 passed**.
  Warning-free import; 36 fresh-process style imports; Python 3.10 parsed 88
  source/test files; 226 annotation targets force-evaluated. Preview constructs
  successfully in separate processes at all four factors.
- Human gate passed (user, 2026-06-29): both preview tabs and flatly↔darkly
  switching approved at 100%, 125%, 150%, and 200%.

**Recolorable raster widget assets — MERGED #1081, VISUALLY APPROVED.** Source
branch: `feat/2.0-recolor-elements`. Locked design:
**`development/2_0_recolor_assets_design.md`**. Radio/checkbox/switch/scale/
scrollbar/progressbar now use bootstack-derived templates from
`assets/elements/`; icons remain for date/carets/sizegrip.

- New leaf `style/elements.py`: lazy JSON manifest/source cache; black/white
  structural channels + optional magenta fill; source alpha preserved; no
  cyan/teal or surface preblend. Horizontal flip handles switch-off; quarter
  turns generate vertical slider/scrollbar/progressbar assets and rotate their
  border/padding metadata. `Assets.recolor` is the only new public surface.
- `StyleBuilderTTK.configure()` now owns the builder-to-engine raw configure
  seam; all 44 raw configuration sites call the local alias, and only that
  alias reaches `Style._build_configure` to bypass public bootstyle resolution.
- Cache key covers asset, final scaled size, every resolved target color, and
  transform. Manifest sources are authored at 2x and resized once.
- Standard + round scrollbars are arrowless raster-thumb layouts; their native
  troughs blend into `colors.bg` and require no trough image asset.
  Selected radio is an accent annulus. Existing striped progressbars remain on
  the stripe renderer. New `bootstyle="thin"` progressbar + public `THIN`
  constant use `progressbar-thin.png`. Checkbutton, radiobutton, and both switch
  layouts use a cached transparent spacer between the indicator and label.
  Progressbar images and layout children stretch only along their orientation
  (`EW` horizontal, `NS` vertical), preventing cross-axis image repetition;
  their style background is the theme surface (`colors.bg`), not the bar color.
  Standard and round scrollbar thumbs now follow the same contract: no
  element-level sticky, axis-only layout sticky, and a surface background.
- Verification: recolor/channel/alpha/transform/metadata/cache/layout/package
  tests added; targeted **38 passed**; remaining headless suite excluding the
  broken local Tcl localization file **98 passed**; warning-free import,
  standalone module guard, Python 3.10 grammar parse, and 684-namespace
  annotation evaluation clean.
- Manual gate passed (user, 2026-06-28): `examples/recolor_assets_preview.py`
  approved after indicator spacing, progressbar stretch/surface, and scrollbar
  thumb-only/native-trough corrections.

## Builder modularization — MERGED #1082, VISUALLY APPROVED

Goal: replace the 2,600+ line `style/builders_ttk.py` recipe monolith with a
private, decorator-backed registry and one module per widget family, following
bootstack's organization without adopting its style grammar or widget API.

Locked scope from the 2026-06-28 discussion:

- Keep the existing bootstyle grammar, generated ttk style names, lazy build
  behavior, theme lifecycle, visuals, and public APIs unchanged.
- Keep `StyleBuilderTTK` as the small per-theme context/coordinator: style,
  colors/theme/assets, scaling/configuration helpers, theme setup, and registry
  dispatch.
- Add a private `style/builders/` package with explicit module imports,
  deterministic `(variant, widget-family)` registration, and family-local asset
  helpers. Put only genuinely shared helpers (such as arrow/spacer assets) in
  `builders/utils.py`.
- Preserve recipes that build/register multiple ttk styles (horizontal +
  vertical pairs, headers, chevrons, and related styles). Do not assume one
  registry call produces only the requested style name.
- Do not copy bootstack's swallowed loader exceptions or silent duplicate
  replacement: imports should fail visibly and duplicate registry keys should
  fail tests.

Implementation summary:

- Merged PR: **#1082**, targeting `2.0`; merge commit `fa1cede8`
  (implementation commit `96bcab40`, handoff commit `f8c20dd8`).
- Approved design: `development/2_0_builder_split_design.md`.
- `StyleBuilderTTK`: 2,689-line monolith → 161-line per-theme coordinator.
- Private frozen registry: 36 exact `(variant, widget-family)` keys; explicit
  loader; duplicate, late, invalid, and non-callable registration fail visibly.
- Recipes: 22 family modules plus `builders/utils.py`; only caret and indicator
  spacer helpers are shared. Multi-output recipes and the three existing recipe
  dependencies are preserved.
- Dispatch: `Bootstyle` uses registry lookup; `name_to_method()` and all ttk
  recipe reflection are removed. Third-party passthrough remains lookup-only,
  while exceptions inside registered recipes propagate.
- Tests: +18 registry/dispatch/lazy/multi-output tests and +25 standalone module
  cases. Targeted registry/package suite **66 passed**.
- Structural gates: warning-free import; Python 3.10 parsed 35 style modules;
  25 fresh-process builder imports; 222 annotation targets force-evaluated.
- Full local suite: **146 passed / 1 environment failure** at missing
  `tk8.6/msgs/nl.msg`; excluding the six-test localization module gives
  **141 passed**. Expected on a complete Tcl install: **147 passed**.
- Manual gate passed (user, 2026-06-29): the current light↔dark set runs well.

Use one implementation branch/PR. Splitting this into parallel branches would
create avoidable conflicts in `builders_ttk.py`, `bootstyle.py`, and package
imports; the coherent unit is the complete behavior-preserving modularization.

## PR 6b — MERGED (2026-06-28, #1080, Workstream I — glyph builders on icons)

Built hybrid: Opus settled the public API + the held-branch keep/drop split and
implemented the registration path; a Sonnet agent did the mechanical glyph/layout
migration against the locked `development/2_0_icons_design.md`; Opus reviewed the
diff. Three commits; suite **92 passed**, warning-free import, font not loaded at
import, standalone cycle guard + PEP 649 sweep clean.

- **`f282262` — public style-registration path** (the PR-6a finding). New
  `register_style(style, ttkstyle)` in `style/layout.py`; **`layout()` now
  auto-registers** the style it applies (defining a layout is what gives a style
  its identity — mirrors ttk's own `style.layout`), so a toolkit-built style
  whose terminal step is `layout()` resolves via `style="..."` with no extra
  step. Re-exported from `ttkbootstrap.style` + top-level. +3 tests.
- **`435ec23` — Part A: glyph builders → icons** (−715/+155). check/radio/
  round-toggle/square-toggle/date/arrows/sizegrip migrated onto `icon_element`/
  `a.icon` per the design's glyph+color tables; the six `create_*_assets` glyph
  methods deleted; `ImageFont`/`Transpose` imports removed. Toggles are **one
  look** (`toggle-on`/`toggle-off`; square is a visual alias). Radio on =
  `record-circle-fill`. Existing state-color math + scaled sizes preserved.
  **Deviation (correct):** element names use the full `{ttkstyle}.indicator`
  prefix (not `sn.element`) so `icon_element`'s foreground lookup targets the
  configured style — matches PR 5's radiobutton convention.
- **`b63db19` — Part B: geometric/layout cleanup** (−353/+150). Separator,
  progressbar (+stripes), scrollbars (round/square), combobox, floodgauge,
  spinbox, treeview, calendar layouts re-applied onto `rect`/`rounded_rect`/
  `image`/`image_element`/`layout`/`El`/`state_map` (re-applied fresh from the
  held branch as reference — not cherry-picked; the file had drifted).

- **Open glyph picks — settle on the spot-check:** `calendar-event` (date) vs
  `calendar`; `grip-horizontal` (sizegrip) vs a corner-grip glyph; LIGHT-on-light
  knockout readability (existing contrast logic preserved as a safety net);
  toggle aspect ratio (rendered at `[24,15]`). Change a pick by editing the one
  glyph name in the builder.
- **Spot-check checklist:** check/radio/toggle indicators across all states
  (esp. disabled = muted) on a light theme and a dark theme; combobox/spinbox/
  scrollbar chevrons (normal/active/disabled); date button calendar; sizegrip;
  separator + striped-progressbar tile alignment; round vs square scrollbar
  thumb shape.

### Spot-check round 2 — DONE (2026-06-28, commits `a8a5f5d`, `9590798`)
From the user's first visual pass: toggle sized up to the glyph's true ~1.6:1
aspect (`[24,15]→[32,20]`, element width 28→36); date button → `calendar3`;
combobox/spinbox arrows switched from outline `chevron-*` to solid `caret-*-fill`
+ right `-padding(6)`; **menubutton** (solid + outline) native clam triangle →
`caret-down-fill` image indicator (new `_build_menubutton_arrow` helper; outline
recolors on hover, solid doesn't); **datepicker header** `◀/▶` text →
`caret-left/right-fill` images in the bar's contrasting fg. Suite 92, warning-free.

### FOLLOW-UP (deferred to a separate PR) — visual polish
**Decision (user, 2026-06-28): PR 6b's job was the *bones* — the icon engine
wired into every glyph builder + the geometric/layout cleanup + the public
registration path. That is done, so PR 6b is merge-ready and a PR is open against
`2.0`. The remaining work is value/asset tweaking, deferred to a follow-up PR.**
Polish candidates (eyeball a fresh `python -m ttkbootstrap` + a date picker):
menubutton caret **size/right-padding** (currently `[13,11]` caret + 10px pad, up
from the tiny native `arrowsize=4` — may read large); datepicker arrow size (14px)
next to the bold title; toggle final sizing; remaining glyph picks
(`grip-horizontal` sizegrip, LIGHT-on-light readability).

## PR 6a — MERGED (2026-06-27, #1079, Workstream I Tier 1.5 — icon engine)

Merged into `2.0` (was `feat/2.0-pr6a-icon-engine`). Engine only — touches **no**
builders, so nothing visual changed yet; suite **89 passed** (was 75; +14 in
`tests/widget_styles/test_icons.py`). Independently diff-reviewed (no leaks;
cache/leaf-layering invariants hold). Per `development/2_0_icons_design.md` (see
its "PR 6a — IMPLEMENTED" section).

- **Vendored** `src/ttkbootstrap/assets/icons/` (`bootstrap.ttf` + `glyphmap.json`
  + `icon_metrics.json`, MIT, LICENSE+README) + regen tool
  `tools/generate_icon_metrics.py`; `assets/icons/*` added to pyproject
  package-data (the `assets/*` glob does not recurse). No new pip dep.
- **`style/icons.py`** (leaf: PIL+stdlib + the two leaf toolkit modules; `Style`
  reached only function-locally): `IconRenderer` lazy-loads font/glyphmap/metrics
  once (persists for process lifetime), renders one glyph via bootstack's
  metrics fit-and-center; **unknown glyph raises**. Public `Icon(name,size,color)`
  atom (keyword-or-hex, resolved once) + `icon_element(...)` state→icon sugar.
- **`Assets.icon`** routes through `Style._get_or_create_image`, key
  `("icon", name, even-snapped size, resolved color)`; takes an already-resolved
  color (like `circle`/`rect`), keyword resolution lives in `Icon`.
- **Render tuning** (settled via a live light↔dark spot-check on Retina):
  icon-specific **6×/3×/1× supersample** (vs bootstack's 3/2/1) + gentle
  **`UnsharpMask(0.5/50)`** — curve smoothness comes from supersampling, not the
  sharpen. **Radio "on" → `record-circle-fill`** (solid knockout), not the thin
  `record-circle`. `examples/icon_preview.py` is the spot-check tool.
- **Gates:** `icons` added to the standalone-import cycle guard; PEP 649
  annotation sweep clean; import warning-free + font not loaded at import.
- **Finding carried to PR 6b (IMPORTANT):** a hand-built custom style applied via
  `style="X.TWidget"` is **silently re-resolved to base `TWidget`** unless the
  name was registered with the private `Style._register_ttkstyle(...)` —
  `BootMixin` only honors `style=` for `style_exists_in_theme()` styles. The real
  builders register; the design's public mock #2 + the demo did not. **PR 6b /
  Tier-2 must give the public toolkit a non-private registration path** (e.g.
  `layout()` registers the style name, or a public `register_style`). Details in
  the design doc's "Finding for PR 6b" section.
- **Open minor glyph picks (defer to 6b spot-check):** `calendar` vs
  `calendar-event`; sizegrip glyph.

## PR 6 — HELD + icon pivot (2026-06-27)

The fast-follow toolkit migration was implemented on
`feat/2.0-pr6-toolkit-migration` (9 commits, suite 75 passed): geometric recipes
(`circle`/`rect`/`rounded_rect`), all 21 `layout()` pyramids, `image_element`/
`state_map` conversions, and `image()`-escape-hatch glyph draws for check/radio/
date/arrows/sizegrip/stripes. **It is NOT merged and is HELD** — the hand-drawn
*glyph* draws looked poor, prompting the icon-font pivot.

**Decision (LOCKED with user):** render glyph-shaped widget assets from a
**vendored Bootstrap Icons font** (`bootstrap.ttf` + `glyphmap.json` +
`icon_metrics.json` from `bootstack/src/bootstack/assets/icons/`, ~610 KB, MIT,
no new pip dep), porting bootstack's metrics-based fit-and-center renderer (the
alignment fix = precomputed em-fraction ink bbox, kills the `getbbox` skew /
`font_offset` fudge) and reusing the PR-5 `style/assets.py` snap/oversample/
UnsharpMask pipeline + the PR-2 `_get_or_create_image` cache. Full design +
locked API + acceptance proof: **`development/2_0_icons_design.md`**. Memory:
`project_2_0_icon_assets`.

Locked headlines: flat single-glyph indicator aesthetic; public surface =
`Icon(name,size,color)` atom + style-level `icon_element(...)` state→icon sugar
(spec grammar adopted from ttkbootstrap-icons' `StatefulIconMixin`, but **not**
its per-widget theme-follow delivery — that fights the no-`Publisher` engine);
switch = one look; arrows = chevron. Geometric assets (tracks/troughs, stripes,
plain scale thumb) stay on the recipes.

**PR plan (replaces the held PR 6):**
- **PR 6a — icon engine (no behavior change):** vendor the 3 assets + regen tool
  + license; `style/icons.py` (`IconRenderer`); `Assets.icon`; public `Icon` +
  `icon_element`; re-exports; tests. Touches **no** builders → suite stays green.
  **✅ MERGED (#1079) — see "PR 6a — MERGED" above.**
- **PR 6b — migrate glyph builders + land the kept geometric/layout cleanup**
  (cherry-pick the geometric/`layout`/`image_element` commits from the held
  branch; drop the hand-drawn glyph commits). Gate the merge on a **human visual
  spot-check** (light↔dark) — the headless suite asserts color-at-pixel, not
  appearance. **Also add the public style-registration path** (PR-6a finding).
  **← next actionable.**

### Merged into `2.0`
- **#1068** — Tier-0 cleanup:
  - Removed long-deprecated top-level shims (`scrolled.py`, `tableview.py`,
    `toast.py`, `tooltip.py`, `dialogs/dialogs.py`). Import from
    `ttkbootstrap.widgets.<name>` / `ttkbootstrap.dialogs` now.
  - Split headless tests from interactive demos: `tests/` is pytest-only (4
    `test_*.py` + new `tests/conftest.py`); ~54 demos moved to `examples/`.
  - `conftest.py` adds a session-scoped shared root + per-test `root` fixture
    (scene + theme reset) — fixes the `Style` singleton bleeding between tests.
  - `pyproject.toml` gained `[tool.pytest.ini_options]` (`testpaths=["tests"]`,
    `gui` marker).
- **#1069** — Public/internal split:
  - New `src/ttkbootstrap/internal/` package (name is `internal`, no underscore).
  - `publisher` → `internal/publisher.py`; top-level `ttkbootstrap.publisher`
    is now a warn-and-reexport shim (removed in 3.0).
  - `utility` stays public (`enable_high_dpi_awareness`, `scale_size`); its two
    internal helpers (`get_image_name`, `center_on_parent`) moved to
    `internal/utility.py`, forwarded from `utility.py` via `__getattr__` + warning.
- **Workstream B (widget-level lifecycle leaks)** — `destroy()`/unsubscribe paths:
  - Canvas `Floodgauge`: trace ids tracked; removed on `destroy()` and when a
    `variable`/`textvariable` is swapped via `configure` (was unbounded trace
    accumulation + external vars pinning a dead widget). `destroy()` also cancels
    the running `after()` animation loop.
  - `Meter`: `_set_interactive_bind()` unbinds before rebinding (no orphaned
    indicator binds when toggling `interactive`); `destroy()` detaches the
    `amountusedvar` write trace.
  - `Combobox` popdown: self-unsubscribes from `Publisher` via a once-bound
    `<Destroy>` handler (`style.py` ~`5434`), so cleanup no longer depends solely
    on the `Window` global `<Destroy>` binding (absent under a vanilla `tk.Tk()`).
  - New `tests/widgets/test_lifecycle.py` (6 headless regression tests).
  - **Not done (left for the engine session):** the `Publisher` mechanism itself
    (keystone, below).
- **`FloodgaugeLegacy` deprecation** — instantiating it now emits a runtime
  `DeprecationWarning` (3.0 removal); was docstring-only. Canvas `Floodgauge`
  stays warning-free, and so does `import ttkbootstrap` (warning fires on init,
  not import). New `tests/widgets/test_deprecations.py` (2 tests). Its lifecycle
  trace leaks were left as-is — the widget is on the way out.
- **Example demo rename** — dropped the misleading `test_` prefix from the ~31
  interactive demos under `examples/` (moved out of `tests/` in #1068 but kept
  their prefixes). Pure renames; `examples/widgets/test_tableview.py` →
  `tableview_yscrollbar.py` to avoid colliding with the existing `tableview.py`.

## The hard rule

**Do not start the `style.py` engine rewrite as ad-hoc coding.** The design
discussion has now been held (see below) — the agreed design lives in
`development/2_0_engine_design.md`. Implementation proceeds **PR by PR per that
doc**, starting with PR 1; do not exceed PR 1's scope without revisiting the doc.

## Engine design session — DONE (2026-06-25)

The dedicated design discussion is complete. Full design:
**`development/2_0_engine_design.md`**. Decisions locked this session:

1. **Style rebuild = lazy, version-stamped** — rebuild a `(theme, style)` only
   when a stale *mounted* widget references it; O(mounted), not O(all-styles).
2. **Multi-root = enforce single-root with a clear `RuntimeError`** — close the
   silent-no-op trap; full multi-root out of 2.0 scope.
3. **Packaging = engine PR in-place, split later** — rewrite repaint/image paths
   inside `style.py` first; `style/` package split is a follow-on PR.
4. **Image cache = content-addressed memoization** — key the asset builders on
   their pixel-determining inputs (resolved hex, scaled size, state, geometry),
   NOT the theme name, so cross-theme-identical assets dedupe and never
   re-render. This also moots theme-return rebuild cost and decouples eviction
   from theme-switch timing.

Resolved repaint model: monotonic `Style._theme_version`; DFS over
`winfo_children()` repaints+restamps only stale widgets (ttk → ensure its
`(theme,style)` fresh; tk-legacy → re-run `update_tk_widget_style` inline);
the `__init__wrapper` keeps its initial paint but **drops `Publisher.subscribe`**.
This deletes `Publisher` wholesale (the leak class disappears — no registry, no
strong refs).

### Agreed PR sequence
- **PR 1 — repaint engine (in-place):** version stamp + theme walk; delete
  `Publisher` (subscribe sites `style.py` ~`5427`/`5552`, publish ~`710`/`716`,
  unsubscribe `window.py` ~`106`); lazy per-theme style rebuild; single-root
  `RuntimeError`. **← next actionable slice.**
- **PR 2 — image cache:** route ~40 `theme_images[...]=` sites through
  `_get_or_create_image`; single content-addressed cache + `clear_image_cache()`;
  builder-purity audit.
- **PR 3+ —** mixin API (C), then `style/` split (G), then theme/anchor (E) +
  bootstyle canonical (D).

### Two pre-flight checks for implementation (not yet settled)
- (a) Is the **combobox popdown** toplevel reached by the root `winfo_children()`
  DFS, or does it need an explicit per-Combobox repaint in the walk?
- (b) **Builder-purity audit**: any asset builder reading color/size from
  `self.colors`/`self.theme` internally (not via args) must lift that input into
  the cache key, else stale images survive a theme change.

Verification to lean on: `tests/widgets/test_lifecycle.py` (destroy/recreate
harness) + `tests/widget_styles/` (built-style values).

## PR 1 — MERGED (2026-06-25, #1073)

Merged into `2.0` (was `feat/2.0-pr1-repaint-engine`); suite **24 passed**.
Full write-up + the pre-flight (a) resolution in
`development/2_0_engine_design.md`. Headlines:
- Monotonic `Style._theme_version`; `theme_use` bumps it then runs `_theme_walk`
  (DFS from the root, repaint+restamp only stale widgets). Deleted
  `_create_ttk_styles_on_theme_change`; rebuild is now lazy/O(mounted).
- `Publisher` removed from the engine (no subscribe/publish/unsubscribe). Module
  + the `ttkbootstrap.publisher` shim kept unused until the 3.0 removal date.
- Combobox popdown repainted inline in `update_ttk_widget_style` (pre-flight (a):
  the popdown is **not** reachable by the Python `winfo_children()` DFS).
- `autostyle=False` tk widgets set `_tb_no_autostyle`; the walk skips them.
- Single-root enforced: `Window.__init__` → `_require_single_root` raises a clear
  `RuntimeError`; `Window.destroy` now clears the class-level `Style.instance`.
- New tests in `tests/widgets/test_lifecycle.py`: no-Publisher-subscriptions,
  walk stamps/repaints mounted widgets, theme-switch-cycle leak check,
  autostyle-skip, single-root raise.

## PR 2 — MERGED (2026-06-25, #1074)

Merged into `2.0` (was `feat/2.0-pr2-image-cache`); suite **28 passed**.
Full write-up + pre-flight (b) resolution in `development/2_0_engine_design.md`.
Headlines:
- Single content-addressed cache `Style._image_cache` + private
  `Style._get_or_create_image(key, factory)` + `Style.clear_image_cache()`.
- All ~40 `theme_images[...] =` sites routed through the helper; per-builder
  `theme_images` dict removed (the image leak) and the fragile
  `_PhotoImage__photo.name` accesses gone.
- Keys are the resolved local colors + scaled size + variant/geometry tag
  (never `colorname`), so theme differences are captured by construction.
- `_get_or_create_image` kept **private**; public toolkit (`image_asset`) is
  Workstream I.
- Verified pixel-level (no stale image after switch) and bounded (20 theme
  round-trips hold the cache flat). New `tests/widget_styles/test_image_cache.py`.

## PR 3 — MERGED (2026-06-25, #1075)

Merged into `2.0` (was `feat/2.0-pr3-mixin-api`). Replaces the import-time
monkey-patch with the mixin-hybrid API (Workstream C). Suite: **42 passed**.
Design pass + the one open fork (tk-side scope) were resolved up front: **full
retirement of the import-time patch** — the blessed tk widgets get a mixin too,
not just ttk.

Headlines:
- **Two mixins in `style.py`** (after `Bootstyle`): `BootMixin` (ttk — intercepts
  `bootstyle`/`style` on `__init__`/`configure`/`config`/`__setitem__`/
  `__getitem__` via `super()`, reusing the unchanged `update_ttk_widget_style` +
  `stamp_theme_version`) and `AutoStyleMixin` (tk — autostyle at construction,
  honoring `autostyle=False` → `_tb_no_autostyle` opt-out, same flag the PR 1
  theme walk skips). Real `super()` methods, so the old late-binding closure bug
  is gone. (Side finding: the legacy `__setitem__`/`__getitem__` overrides never
  actually installed — `widget.__getitem` raised `AttributeError` swallowed by a
  bare `except: continue` — so the mixin's correct accessors are a net gain.)
- **Concrete subclasses re-exported from `__init__.py`**: 19 ttk (`class
  Button(BootMixin, ttk.Button)` …; `OptionMenu` restores tkinter's
  `__getitem__`/`__setitem__` for menu-item access) + 6 tk (`Tk`, `Menu`, `Text`,
  `Canvas`, `TkFrame`, `LabelFrame` with `AutoStyleMixin`). Defined **before** the
  widgets/dialogs/window imports, since those import widget names from
  `ttkbootstrap` — so the whole internal tree flows through the mixins with **no
  global patch**.
- **Import-time `setup_ttkbootstrap_api()` call removed**; it is now the body of
  the opt-in `enable_global_api()` (idempotent; its wrappers defer to
  `BootMixin`/`AutoStyleMixin` instances via an `isinstance` guard, so the global
  path never double-resolves a blessed widget). `import ttkbootstrap` stays
  warning-free.
- **New delivery primitives** (all re-exported): `bootify(cls)` →
  `type(cls.__name__, (BootMixin, cls), {})`; `apply_bootstyle(widget, bootstyle)`
  for per-instance styling with no class mutation; `enable_global_api()`.
- **Typing**: deleted the ~450-line inline `TYPE_CHECKING` block **and** the
  54 KB `__init__.pyi`. Concrete classes carry a one-line docstring each;
  `bootstyle` is now statically visible. Accepted trade-off (per the locked
  decision): native per-widget kwargs degrade from the hand-maintained stubs to
  typeshed-inherited + `**kwargs`.
- **Two regressions found + fixed during the sweep:** `Toplevel` (subclasses
  `tkinter.Toplevel` directly, so it missed the retired tk patch) now paints
  itself via `Bootstyle.update_tk_widget_style`/`stamp_theme_version` in
  `window.py`; `tableview.py`'s 8 context menus switched from raw `tk.Menu` to the
  blessed `ttk.Menu`. `Window` was already fine (its `Style(themename)` themes the
  root).
- **Back-compat preserved:** the legacy tuple/list `bootstyle` form still resolves
  (used internally by `Meter`/`DateEntry`/tooltip/datepicker) — canonical-string
  enforcement is Workstream D, untouched here.
- **Tests:** new `tests/test_mixin_api.py` (14 tests: subclass shape, stock
  tkinter stays unpatched, bootstyle/configure/item-access resolution, tuple
  back-compat, OptionMenu item access, autostyle opt-out, `bootify`,
  `apply_bootstyle`, `enable_global_api` idempotency). `test_lifecycle.py`'s
  autostyle-opt-out test updated to use the blessed `ttk.Canvas`.

## PR 4 — MERGED (2026-06-25, #1076, Workstream G — `style/` split)

Design pass first (per the hard rule): `development/2_0_style_split_design.md`.
Scope decision (asked + answered): **pure, behavior-preserving move**; the
Workstream I toolkit is a separate follow-on PR. Merged into `2.0` (was
`feat/2.0-pr4-style-split`). Suite: **61 passed**.

- `style.py` → `style/` package: `theme.py` (Colors, ThemeDefinition),
  `builders_tk.py` (StyleBuilderTK), `builders_ttk.py` (StyleBuilderTTK — the
  bulk), `engine.py` (Style), `bootstyle.py` (Keywords, Bootstyle,
  BootMixin/AutoStyleMixin, bootify/apply_bootstyle/enable_global_api),
  `__init__.py` (re-exports the full public surface).
- Strict downward import layering (theme→builders_tk→builders_ttk→engine→
  bootstyle); the only cycles are **6 function-local back-edges** (Colors→Style,
  the two builders' `__init__`→Style, engine→Bootstyle ×2). No import-time cycle;
  each submodule imports standalone.
- **No shim needed** — `ttkbootstrap.style` stays a valid public path; every
  existing `from ttkbootstrap.style import …` resolves unchanged;
  `import ttkbootstrap` stays warning-free. Submodule paths (`style.engine`, …)
  are implementation detail (treat like `internal/`).
- New `tests/test_style_package.py` (structural guards: public surface, legacy
  imports, standalone-submodule cycle guard, consumer imports).
- **Python 3.14 / PEP 649 gotcha** found + handled: lazy annotations masked a
  missing annotation-only import (`ThemeDefinition` in `builders_tk`). A
  "does it import?" check is insufficient on 3.14 — added an annotation
  force-evaluation sweep. **Reuse it for E/D code moves.** Details in the design
  doc's "Implementation — DONE" section.

## PR 5 — MERGED (2026-06-25, #1077, Workstream I Tier-1 toolkit)

Merged into `2.0` (was `feat/2.0-pr5-toolkit`), per
`development/2_0_toolkit_design.md`. Suite: **75 passed** (was 61; +14 in
`tests/test_toolkit.py`). Headlines:

- **New `style/assets.py`** — `Assets(style)` facade over PR 2's
  `Style._get_or_create_image`. Recipes `circle`/`rect`/`rounded_rect` + the
  `image(size, draw_fn, *key_parts)` escape hatch. The cache key is *derived
  from the render inputs* (resolved hex + snapped size + geometry), so it cannot
  drift from the pixels — the hazard PR 2's purity audit managed by hand. Ports
  bootstack's snap-at-the-source pipeline: even-pixel-snap the size, adaptive
  oversample (3×/2×/1× by size), LANCZOS + `UnsharpMask`. No public
  `oversample`/`inset` knobs. `rect` is solid-fill (no AA, no snap → keeps exact
  size, e.g. the 40×5 scale track).
- **New `style/layout.py`** — `El`/`layout` (lowers an `El` tree to ttk's nested
  `(name, opts)` form; children via constructor kwarg, not bootstack's fluent
  positional parenting), `image_element` (named, validated state→image map),
  `statespec`/`state_map` (validate the `!neg`/space-AND grammar against
  `TTK_STATES` — the Workstream D loud-failure seam; keep the token set here),
  `StyleName` (absorbs the `DEFAULT/""`→PRIMARY, `f"{color}.{STYLE}"`, and
  `.TS→.S` element-name dance).
- **Acceptance test met**: `create_scale_assets`/`create_scale_style` and
  `create_radiobutton_assets`/`create_radiobutton_style` migrated onto the
  toolkit — shorter and clearer (radio style 69→29 lines incl. docstring; the
  30-line layout pyramid → 5 readable lines). Behavior-preserved: layouts query
  identical to the originals (`expand`=`'1'`, `sticky`=`'nswe'`, same element
  names + radio pyramid, same `foreground`/disabled map). The migrated radio
  keeps the original `sticky=""` on indicator/focus (the design's example
  omitted it; kept for behavior-exactness).
- **Public surface** re-exported from `style/__init__.py` *and* top-level
  `ttkbootstrap` (`Assets`, `El`, `layout`, `image_element`, `statespec`,
  `state_map`, `StyleName`); `import ttkbootstrap` stays warning-free.
- **`test_image_cache.py` helper** updated: the scale thumb's key tag moved from
  `"scale.thumb"` to the recipe's `("circle", fill, size, None, 0)`; assertions
  unchanged (still color-at-pixel, robust to the snapped-pipeline AA change).
- **Gates re-run**: standalone-import cycle guard (assets/layout import alone;
  they're leaves — assets→PIL, layout→constants, no engine edge) and the PEP 649
  annotation force-evaluation sweep (3.14) over the two new modules + migrated
  builders — both clean.
- **Open follow-up (merged without it)**: a spot visual diff on scale/radio/check
  to confirm the snapped pipeline reads equal-or-better (sharper/DPI-stable, not
  color drift) — couldn't run a GUI in the headless dev env. Worth an eyeball
  before the next release.
- **Deferred (out of PR 5 scope)**: migrating the *remaining* ~25 asset / ~25
  layout sites onto the toolkit (mechanical, same shapes repeated) — design doc
  step 4, a fast-follow. Tier 2 (`state_colors` from ramp steps; composite
  recipes) waits on Workstream E.

## Workstream I — DESIGN PASS DONE (2026-06-25), implementation done (see "PR 5")

Design pass held (per the hard rule — new public surface, like the engine/split
got one). Full design: **`development/2_0_toolkit_design.md`**. The next session
**implements PR 5 from that doc**; do not exceed its scope without revisiting it.

Tier-1 toolkit lands in **`style/assets.py`** (`Assets` facade: `circle`/`rect`/
`rounded_rect` shape recipes + an `image(size, draw_fn, *key_parts)` escape hatch,
all wrapping PR 2's `_get_or_create_image`) + **`style/layout.py`** (`layout()`/
`El`, `image_element`, `statespec`/`state_map`, `StyleName`). Re-exported from
`style/__init__.py` and top-level `ttkbootstrap` (public custom-style API).

Decisions locked this session:
- **PR scope = one PR** (assets + layout together; the acceptance test spans both).
- **The key is derived from the recipe, never hand-written** — kills the
  hand-built-key purity hazard that PR 2's whole audit existed to manage.
- **Fidelity = adopt bootstack's snap-at-the-source pipeline** (not the earlier
  (A)/(B) drift tradeoff). Per user steer, mined `bootstack/src` and ported four
  mechanisms into `Assets`: round the DPI factor; **even-pixel-snap** the final
  size before keying/rendering (kills fractional-DPI LANCZOS blur); **adaptive
  oversample** (3×/2×/1× by size) + snap draw origin to oversample multiples;
  LANCZOS + `UnsharpMask`. Result is *crisper, DPI-stable* assets, not color drift
  → PR 2's color-at-pixel purity tests still pass. No public `oversample`/`inset`
  knobs. (bootstack refs in the design doc's fidelity section.)
- **`El`/`image_element` mirror bootstack's `Element.spec()`/`ElementImage.build()`**
  (same author, keep models in sync), with two deliberate divergences: constructor
  `children=[...]` (not fluent positional parenting) and validating `statespec`
  (the Workstream D loud-failure seam).

Acceptance test pre-validated in the doc: `create_scale_assets` ~64→~22 lines,
`create_radiobutton_style` ~67→~18, both clearer. Carry the **PEP 649 annotation
force-evaluation sweep** into the new modules + migrated builders (3.14 gotcha).

Then E (theme/anchor model) + D (bootstyle canonical grammar), carrying the
`_compat` adapters. Tier-2 toolkit (`state_colors` from ramp steps) follows E.

## Open decisions (from the plan)
- ~~Multi-root~~ — **LOCKED**: enforce single-root with a clear `RuntimeError`.
- bootstyle strictness default: warn-by-default + opt-in strict (lean) vs strict.
  (Deferred to Workstream D — does not gate the engine PRs.)
- Built-in theme drift from auto-ramps (lean: accept) vs pin specific themes.
  (Deferred to Workstream E — does not gate the engine PRs.)

## Conventions established this effort
- `internal/` (no underscore) for private plumbing; warn-shim old public paths,
  remove in 3.0; `import ttkbootstrap` stays warning-free.
- Tiered deprecation: things deprecated for years → removed in 2.0; new 2.0
  standardizations → warn-and-normalize through 2.x, removed in 3.0.
- 2.0 PRs target `2.0`; maintenance/bugfixes target `master`.
