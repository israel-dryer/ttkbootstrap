# ttkbootstrap 2.0 — Engine Design (Workstream A keystone)

> Output of the dedicated engine design session (2026-06-25). Pairs with
> `development/2_0_plan.md` (durable worklist) and `development/2_0_handoff.md`.
> This is the agreed design for the repaint/image-cache rewrite. Line refs are
> point-in-time against `style.py` on the `2.0` branch — verify before relying.

## Scope

Workstream A: replace the `Publisher` repaint plumbing and the unbounded image
cache with bootstack's **mechanisms** (not its API). In-place in `style.py`
(the `style/` package split is a later PR — locked below). No theme/anchor or
mixin work in this stream.

## Locked decisions (this session)

1. **Style rebuild = lazy, version-stamped.** Stamp styles like widgets; a style
   is rebuilt only when a stale *mounted* widget references it. Both repaint and
   rebuild become O(mounted), not O(all-styles-ever-used).
2. **Multi-root = enforce single-root with a clear `RuntimeError`.** Closes the
   silent-no-op trap where the singleton binds to the first root. Full
   multi-root stays out of 2.0 scope.
3. **Packaging = engine PR in-place, split later.** Rewrite the repaint/image
   paths inside the current `style.py` first (clean, behavior-focused diff),
   then do the `style/` package split + mixin API as follow-on PRs.
4. **Image cache = content-addressed memoization** (refinement, see below):
   key on the pixel-determining inputs, not the theme name, so cross-theme
   -identical assets dedupe and are never re-rendered.

Deferred (do **not** gate this stream): bootstyle strictness default, built-in
theme drift — those belong to Workstreams D/E.

## Current state (what we're replacing)

`Publisher` (`internal/publisher.py`) does exactly two jobs; the `TTK` channel
is dead (nothing publishes/subscribes to it):

- **Legacy `tk.*` widgets** subscribe a repaint closure at construction
  (`style.py` `__init__wrapper` ~`5540`/`5552`); `theme_use` fires
  `publish_message(Channel.STD)` (~`710`/`716`) to repaint them all.
- **Combobox popdown** subscribes its own closure (~`5427`), with a
  destroy-unbind added in Workstream B.

Unsubscribe is split between the `Window` global `<Destroy>` binding
(`window.py` ~`106`) and the combobox's own binding. Structural defect:
**`Publisher` holds a strong ref to every styled widget via its closure** — the
leak class Workstream B patched widget-by-widget but did not root out.

Alongside:
- `theme_use` → `_create_ttk_styles_on_theme_change` rebuilds **every** registered
  style on every switch.
- `theme_images` (per `StyleBuilderTTK`, ~`1282`) never evicts; `theme_use`
  spins up a **new** builder per theme (~`714`) while old builders + their
  PhotoImages stay pinned in `_theme_objects`. No cross-theme dedup (names are
  per-builder/uuid-scoped).

## Repaint model (resolved)

A monotonic `Style._theme_version`, bumped in `theme_use`. Stamps:
`_style_versions[name]` and `widget._theme_version`. On `theme_use`, after
`super().theme_use(name)` swaps the Tcl theme DB, run a **DFS over
`winfo_children()` from the root**; for each widget stamped `< current`:

- **ttk widget** → read its style token; ensure `(current_theme, style)` is fresh
  in the Tcl DB (rebuild via the builder if stale, then stamp the style); restamp
  the widget. ttk reflects the reconfig on its next redraw automatically.
- **tk-legacy widget** → no Tcl style; re-run `update_tk_widget_style(w)` inline.
  The walk reaches it because it is in `winfo_children()` — **this is what lets us
  delete the `Publisher` subscription entirely.**

Key points:
- **Per-theme Tcl style DBs.** ttkbootstrap builds each theme with
  `theme_create(name, TTK_CLAM)`, so a style configured under theme A is invisible
  under theme B — that is *why* the legacy code rebuilds on switch. The walk
  rebuilds `(theme, style)` on demand and stamps it; the monotonic version drives
  staleness. Theme-return (A→B→A) re-runs A's `configure` calls, which is cheap
  because images are content-addressed cache hits (below).
- **No registry, no strong refs.** A widget born at version V stamps V and paints
  once in its constructor; the `__init__wrapper` keeps the *initial* paint but
  **drops `Publisher.subscribe`**. Destroyed widgets are simply absent from the
  tree — the whole subscribe/unsubscribe dance (incl. `window.py:106`) goes away.
- **Single-root enforcement.** Constructing a second root against an existing
  `Style` raises `RuntimeError` with a clear message instead of silently
  no-oping. Tests share one root via the `conftest.py` `root` fixture.
- **Combobox popdown** folds in as a per-Combobox step in the walk — PRE-FLIGHT
  CHECK (a): confirm the popdown toplevel is reachable by the root DFS; if not,
  repaint it explicitly when the walk hits a Combobox.
- Event-free walk → also fixes the `<Map>`-deferred canvas mis-repaint bug class.

### Wiring to remove / change
- Delete `Publisher` usage: `style.py` ~`710`/`716` (publish), ~`5427` and ~`5552`
  (subscribe), `window.py` ~`106` (unsubscribe). Then remove
  `internal/publisher.py` and its top-level shim once nothing imports it.
- `theme_use`: bump version + run the walk in place of
  `_create_ttk_styles_on_theme_change()` + `publish_message`.

## Image cache (content-addressed)

**Memoize the asset builders on their resolved inputs.** Key =
`(builder-id, *resolved-args)` where args are the pixel-determining values:
resolved hex color(s), final scaled pixel size, state, geometry (radius, border,
arrow direction, stripe, …). **Not** the theme name. One shared cache on `Style`.

- Same key anywhere (any theme) → one PhotoImage, built once, shared across theme
  DBs. The Tcl image **name derives from the key** (`ttkb_<digest>`), so
  `image create photo` runs only on a miss and multiple styles/themes reference
  the same name safely.
- A color/size change → new key → new image rendered lazily on style rebuild; the
  old image just stops being referenced.

**Default-on.** The cache is the default path, not an opt-in toggle — it is the
leak/correctness fix, not a perf knob. Escape hatches only: `clear_image_cache()`
and a debug force-miss (e.g. env flag) for diagnosing render bugs.

**Versioning split.** Content-addressing *subsumes* per-image versioning: an
image is immutable by its key, so a color/theme change yields a *different* key
(different image), never an invalidation. The monotonic `_theme_version` stamps
only the **mutable** things (styles, widgets); images — the **immutable** things
— are addressed by content. The two mechanisms compose; the version stamp never
touches image identity.

Consequences:
- **Theme-return is cheap** — the expensive part (Pillow rendering) is a cache hit;
  only the (cheap) ttk `configure` calls re-run. Monotonic-version-only suffices.
- **Default-on raises the stakes on the purity audit (check (b)).** With caching
  as the default path, *every* builder must be pure w.r.t. its key or users get
  silent wrong-color assets after a theme switch — so the audit is a hard gate
  for PR 2, not optional.
- **Eviction is not timing-coupled.** Nothing is cleared on theme switch. Growth
  is bounded by *distinct* visual assets across visited themes (deduped), not by
  widgets-created × themes-visited. PR 2 ships a single content-addressed cache +
  an explicit `clear_image_cache()`; default-on is the argument for eventually
  adding **mark-and-sweep-during-the-walk** eviction (touch = keep, unmarked =
  free) — deferred unless profiling demands it.

**Correctness obligation — PRE-FLIGHT CHECK (b):** every asset builder must be
*pure with respect to its keyed args*. Audit the ~40 `theme_images[...] =` sites
(~`1565`–`4873`): any color/size read from `self.colors`/`self.theme` *inside* a
builder rather than passed as an argument must be lifted into the key, or the
cache returns a stale image after a theme change. The ~40 sites funnel through a
`_get_or_create_image(key, render_fn)` helper.

## Pre-flight check (a) — RESOLVED (PR 1 session)

The combobox popdown is **not** reachable by the root `winfo_children()` DFS.
At the Tcl level the popdown *is* a child of the combobox
(`winfo children .!combobox` → `.!combobox.popdown`), but tkinter's Python-side
`winfo_children()` skips it because the popdown is created lazily by ttk at the
Tcl level and never registered in tkinter's per-widget `children` dict. So the
generic walk cannot reach it. **Resolution (as designed):** the walk calls
`Bootstyle.update_ttk_widget_style` for every ttk widget, and that method now
repaints the popdown inline when it sees a `TCombobox` (no subscription). Probe
preserved at scratchpad `probe_popdown.py`.

## PR 1 — DONE (this session)

Implemented on `feat/2.0-pr1-repaint-engine` off `2.0`. Suite: 24 passed.
- `Style._theme_version` monotonic counter; `theme_use` bumps it then runs
  `_theme_walk()` (DFS from `self.master`, repaint+restamp stale widgets via
  `_repaint_widget`: ttk → `update_ttk_widget_style`, tk → `update_tk_widget_style`).
- `_create_ttk_styles_on_theme_change` (rebuild-every-registered-style) deleted;
  rebuild is now lazy/O(mounted) driven by `style_exists_in_theme` per visited
  widget. (`_style_versions` from the design was **not** added — per-theme Tcl
  style DBs already make `style_exists_in_theme` the staleness signal, so a
  parallel style-version dict would be a redundant second source of truth.)
- `Publisher` usage removed from the engine: subscribe sites, the publish calls
  in `theme_use`, and `window.py`'s `<Destroy>` unsubscribe binding. The
  `internal/publisher.py` module + its top-level `ttkbootstrap.publisher` shim
  are **kept** (now unused by core) to honor the "removed in 3.0" deprecation
  promise on that public path; delete both in 3.0.
- `autostyle=False` tk widgets now set `_tb_no_autostyle` and the walk skips
  them — preserves the pre-2.0 "opted-out widget never repaints" behavior that
  previously fell out of never-subscribing.
- Single-root: `Window.__init__` calls `_require_single_root` (raises
  `RuntimeError` if a Style is bound to a different live root); `Window.destroy`
  now clears the **class** attr `Style.instance` (was a no-op instance attr),
  so sequential roots work and the singleton rebinds cleanly.
- Composite widgets (Meter/Floodgauge) repaint via Tk's native `<<ThemeChanged>>`
  virtual event (fired by `theme_use`), independent of the deleted Publisher —
  verified still firing.

## Pre-flight check (b) — RESOLVED (PR 2 session)

Builder-purity audit of all 13 asset builders (all ~40 `theme_images[...]`
sites) completed via four parallel sub-audits. Findings:
- **Pure builders** (receive pre-resolved hex args; key directly on them):
  `create_simple_arrow_assets`, `create_arrow_assets` (dead code, unused),
  `create_round_scrollbar_assets`, `create_scrollbar_assets`,
  `create_date_button_assets`, `create_sizegrip_assets`.
- **Impure builders** (resolve colors internally from `self.colors` /
  `self.is_light_theme` / `make_transparent` / `update_hsv`):
  `create_separator_style`, `create_striped_progressbar_assets`,
  `create_scale_assets`, `create_square_toggle_assets`,
  `create_round_toggle_assets`, `create_radiobutton_assets`,
  `create_checkbutton_assets`.

Resolution: every image is keyed on the **resolved local values its draw
closure actually uses** (resolved hex colors + scaled size + a variant/geometry
tag), never on `colorname`. Because the resolved hex differs across themes, the
key differs across themes by construction — `is_light_theme` is subsumed (it
only *selects* a color, whose hex is already in the key). Two special cases
lifted explicitly: the radiobutton's outline-vs-fill **geometry branch**
(`colorname == LIGHT and is_light_theme`) is captured as a boolean in the key;
the checkbutton's OS-font glyph is captured via `(indicator, font_offset)`
(process-constant, but keyed for safety). Verified pixel-level: a scale thumb's
center pixel tracks each theme's resolved primary (no stale image).

## PR 2 — DONE (this session)

Implemented on `feat/2.0-pr2-image-cache` off `2.0` (PR 1 already merged).
Suite: 28 passed.
- Single content-addressed cache `Style._image_cache` + private
  `Style._get_or_create_image(key, factory)` (memoize on a miss; hold a strong
  ref to keep the PhotoImage/Tcl image alive) + `Style.clear_image_cache()`.
- All ~40 `theme_images[...] =` sites routed through the helper; the
  per-builder `theme_images` dict **removed** (it was the image leak: old
  builders pinned in `_theme_objects` kept a full set of PhotoImages per
  visited theme). The fragile `_PhotoImage__photo.name` accesses are gone too.
- `_get_or_create_image` kept **private** for PR 2; the public custom-style
  toolkit (`image_asset` + shape recipes) is deferred to Workstream I, which
  will wrap this same chokepoint.
- Leak verified: 20 cosmo↔darkly round-trips hold the cache flat (was unbounded
  growth before). New tests in `tests/widget_styles/test_image_cache.py`:
  dedup, fresh-pixels-on-switch (purity gate), theme-return-is-a-cache-hit,
  clear-empties.

Note on `clear_image_cache`: it is a memory/diagnostics hatch, **not** a live
refresh — styles are built once per `(theme, style)`, so a same-theme switch
after a clear does not re-render existing styles (they still "exist", now
pointing at freed image names). Recovery is activating a not-yet-built theme.
Docstring states this. A safe live-refresh would need the deferred
mark-and-sweep-during-the-walk eviction.

## PR sequence

- **PR 1 — repaint engine (in-place):** version stamp + theme walk; delete
  `Publisher` (both subscribe sites + `window.py` unsubscribe + publish in
  `theme_use`); lazy per-theme style rebuild; single-root `RuntimeError`.
  Behavior-focused; leans on `tests/widgets/test_lifecycle.py` as the regression
  net. Add a destroy/recreate + theme-switch stress assertion for subscriber/leak
  count going to zero. **← DONE.**
- **PR 2 — image cache:** content-addressed cache + `clear_image_cache()`;
  builder-purity audit. **← DONE (see above).**
- **PR 2 — image cache:** route the ~40 image sites through
  `_get_or_create_image`; single content-addressed cache on `Style`;
  `clear_image_cache()`; the builder-purity audit. Depends on PR 1's
  infrastructure but is a separable review.
- **PR 3+ —** mixin API (Workstream C), then `style/` package split
  (Workstream G), then theme/anchor model (E) + bootstyle canonical (D) carrying
  the `_compat` adapters.

## Verification to lean on
- `tests/widgets/test_lifecycle.py` — destroy/recreate harness; catches
  repaint/leak regressions.
- `tests/widget_styles/` — asserts built style values.
- New for PR 1: assert `Publisher` is gone and that N create/destroy/theme-switch
  cycles leave no residual per-widget references (the old subscriber-count check,
  now a tree/stamp check).
