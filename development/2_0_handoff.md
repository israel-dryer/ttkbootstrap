# ttkbootstrap 2.0 — Session Handoff

> Living handoff for the 2.0 cleanup. Update at the end of each working session.
> Pair with `development/2_0_plan.md` (the durable worklist) and `CLAUDE.md`.

_Last updated: 2026-06-25 (PR 2 — image cache — implemented on
`feat/2.0-pr2-image-cache`)._

## Where we are

Integration branch: **`2.0`** (cut all 2.0 PRs against it, not `master`).
Suite: `python -m pytest -q` → **28 passed**, headless, order-independent.

PR 1 (engine repaint) is **merged** into `2.0` (#1073). PR 2 (content-addressed
image cache) is **implemented and green** on `feat/2.0-pr2-image-cache` (off
`2.0`); not yet merged. Details in `development/2_0_engine_design.md`
("PR 2 — DONE" + "Pre-flight check (b)"). Next actionable slice is **PR 3 —
the mixin API (Workstream C)**.

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

## PR 2 — DONE (2026-06-25)

Implemented on `feat/2.0-pr2-image-cache` (off `2.0`); suite **28 passed**.
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

To merge: PR `feat/2.0-pr2-image-cache` → `2.0`.

## Next session: PR 3 — the mixin API (Workstream C)

This leaves the engine (Workstream A) keystone complete. PR 3 moves to the API
delivery: the `BootMixin` hybrid (see `development/2_0_plan.md` Workstream C and
the locked decisions). Replaces the import-time monkey-patch with concrete
typed subclasses (`class Button(BootMixin, ttk.Button)`), a `bootify(cls)`
factory, `apply_bootstyle(widget, style)`, and opt-in `enable_global_api()`;
deletes the ~450-line `TYPE_CHECKING` stub block and the 55 KB `__init__.pyi`,
and removes the late-binding closure bug in `setup_ttkbootstrap_api`. After C
comes the `style/` package split (G) — which is also where the **public**
`image_asset`/style-construction toolkit (Workstream I) wraps PR 2's
`_get_or_create_image` chokepoint — then the theme/anchor model (E) + bootstyle
canonical grammar (D) carrying the `_compat` adapters.

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