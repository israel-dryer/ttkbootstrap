# ttkbootstrap 2.0 — Session Handoff

> Living handoff for the 2.0 cleanup. Update at the end of each working session.
> Pair with `development/2_0_plan.md` (the durable worklist) and `CLAUDE.md`.

_Last updated: 2026-06-25._

## Where we are

Integration branch: **`2.0`** (cut all 2.0 PRs against it, not `master`).
Suite: `python -m pytest -q` → **18 passed**, headless, order-independent.

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
    (keystone, below). `FloodgaugeLegacy` has the same trace-leak pattern but is
    slated for deprecation — left alone.

## The hard rule

**Do not start the `style.py` engine rewrite (the split into a `style/` package,
the mixin API, the theme/anchor model, the version-stamped theme walk) as ad-hoc
coding.** The user wants a **dedicated design discussion first**. Independent,
low-risk cleanup can proceed without it.

## Suggested next slices (independent, no design session needed)

1. **`FloodgaugeLegacy`** — plan lists it for outright 2.0 removal, but it only
   has a docstring deprecation (never a runtime `DeprecationWarning`). User's
   lean: **add a `DeprecationWarning` in 2.0, remove in 3.0** rather than delete
   cold. Exported from `__init__.py`, `widgets/__init__.py`, `__init__.pyi`,
   defined in `widgets/floodgauge.py`.
2. **Wart:** ~30 demos in `examples/` still carry `test_` prefixes (no longer
   collected, just misleading names). Trivial rename.

(Workstream B widget-level lifecycle leaks — **done**, see Merged section above.)

## The keystone (needs the design session)

**Workstream A — engine repaint.** The opening concrete item is **eliminating
`Publisher`** (now `internal/publisher.py`): it is solely the legacy-tk-widget +
combobox-popdown repaint plumbing (only the `STD` channel is used; `TTK` is dead
code). Replace it with bootstack's **version-stamped theme walk** (DFS
`winfo_children()`, stamp `_theme_version`, repaint only stale). This rewrites
core `theme_use` paths and the widget-constructor wrappers in `style.py`, so it
belongs in the design session, not a quick PR. Wiring today:
`style.py` ~`709`/`715` (publish), ~`5426`/`5540` (subscribe), `window.py` ~`106`
(unsubscribe on `<Destroy>`).

## Open decisions (from the plan)
- bootstyle strictness default: warn-by-default + opt-in strict (lean) vs strict.
- Multi-root: enforce single-root with a clear error (lean) vs defer.
- Built-in theme drift from auto-ramps (lean: accept) vs pin specific themes.

## Conventions established this effort
- `internal/` (no underscore) for private plumbing; warn-shim old public paths,
  remove in 3.0; `import ttkbootstrap` stays warning-free.
- Tiered deprecation: things deprecated for years → removed in 2.0; new 2.0
  standardizations → warn-and-normalize through 2.x, removed in 3.0.
- 2.0 PRs target `2.0`; maintenance/bugfixes target `master`.