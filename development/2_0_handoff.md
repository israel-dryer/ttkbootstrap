# ttkbootstrap 2.0 — Session Handoff

> Living handoff for the 2.0 cleanup. Update at the end of each working session.
> Pair with `development/2_0_plan.md` (the durable worklist) and `CLAUDE.md`.

_Last updated: 2026-06-25 (Workstream I — style-construction toolkit — **PR 5
merged** into `2.0` (#1077) per `development/2_0_toolkit_design.md`; suite
**75 passed**)._

## Where we are

Integration branch: **`2.0`** (cut all 2.0 PRs against it, not `master`).
Suite: `python -m pytest -q` → **75 passed**, headless, order-independent.

The engine keystone (Workstream A) is **complete and merged**: PR 1 (repaint,
#1073) + PR 2 (content-addressed image cache, #1074). **PR 3 — the mixin API
(Workstream C)** is **merged** (#1075). **PR 4 — the `style/` package split
(Workstream G)** is **merged** (#1076; pure move, see "PR 4" below). **PR 5 —
the style-construction toolkit (Workstream I, Tier 1)** is **merged** (#1077; see
"PR 5" below). Next: migrate the remaining ~50 asset/layout sites onto the
toolkit (fast-follow, mechanical), then Workstream E (theme/anchor model) + D
(bootstyle canonical grammar); Tier-2 toolkit follows E.

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