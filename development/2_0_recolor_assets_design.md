# 2.0 — Recolorable raster widget assets (design brief)

> **Status: IMPLEMENTED + VISUALLY APPROVED (2026-06-28).** The staged
> `assets/elements/` templates are the source set; the decisions at the end of
> this document are implemented on `feat/2.0-recolor-elements`.

## Goal

Let a set of built-in widgets be styled from **pre-made image assets that are
recolored on demand** — a collection of template/source images, each tinted to
the requested theme color at render time and cached — instead of (or alongside)
the font-glyph icons (`style/icons.py`) and geometric draws
(`Assets.circle/rect/rounded_rect`) used today.

**Target widgets (user's list):** radio, checkbox, switch (toggle), slider
(`Scale`), scrollbar, progressbar.

This ports bootstack's manifest-driven element-image mechanism, adapted to
ttkbootstrap's content-addressed cache and true-alpha compositing.

### DECISION (user, 2026-06-28): recolored rasters REPLACE the current rendering

For these six widgets the recolored raster assets **replace** what's there now —
the user judged the font-glyph icon quality not good enough for general widget
indicators. **The icon engine itself stays** (`style/icons.py`, `Icon`,
`icon_element`): widgets NOT on this list keep using glyph icons — date button
(`calendar3`), combobox/spinbox/menubutton/datepicker carets (`caret-*-fill`),
sizegrip (`grip-horizontal`). Only the six listed widgets move to recolor.

**What "replace" means per widget (important — only half the list is on icons today):**

| Widget | Renders today via | Migrate to |
|---|---|---|
| radio | **icon** `record-circle-fill` / `circle` (PR 6b) | `recolor` |
| checkbox | **icon** `check-square-fill` etc. (PR 6b) | `recolor` |
| switch (toggle) | **icon** `toggle-on`/`toggle-off` (PR 6b) | `recolor` |
| slider (`Scale`) | **geometric** `Assets.circle` thumb (PR 5) | `recolor` |
| scrollbar | **geometric** `Assets.rounded_rect` pill thumb | `recolor` |
| progressbar | **geometric** `Assets.rect` + striped tiles | `recolor` |

So radio/checkbox/switch un-wire their `icon_element`/`a.icon` calls; scale/
scrollbar/progressbar swap their geometric recipe calls. State-color math and
scaled sizes are preserved in both cases (see "Builder migration" below).

## Why this fits the existing 2.0 architecture

The hard part is already built. 2.0 has a **content-addressed image cache** and a
**key-safe asset toolkit**, so recoloring is a *new recipe on an existing
pipeline*, not new infrastructure:

- `Style._get_or_create_image(key, factory)` + `Style.clear_image_cache()`
  (engine, PR 2): one process-wide cache keyed on the pixel-determining inputs.
  Keys must **never** include the theme name — identical assets across themes
  dedupe by construction.
- `style/assets.py` `Assets` (PR 5): the key-safe front door. Every recipe
  derives its cache key from the same inputs it renders from. Reuse its even-size
  helper, but resize the authored 2x raster directly rather than procedurally
  supersampling it.
- `style/icons.py` `Assets.icon` (PR 6a/6b): the cache-routing precedent.
  Recolor differs at the element layer because its templates are multi-channel,
  manifest-sized, and carry stretch metadata; `icon_element` is not generalized.
- `style/layout.py` (PR 5/6b): `image_element` (validated state→image element),
  `state_map`/`statespec` (the `!neg` / space-AND grammar), `layout()`/`El`, and
  **`register_style`** (`layout()` auto-registers so a toolkit-built style
  resolves via `style="..."`). Recolor assets plug straight into these.

So the work is: (1) a manifest-driven recolor recipe on `Assets`, (2) the
vendored `assets/elements/` directory + packaging, and (3) migrating the six
target builders. Unlike the original proposal, there is no top-level atom or
`recolor_element`: multi-channel, manifest-sized element templates do not share
the icon surface's single-color grammar.

## Proposed design

### 1. The recolor recipe — `Assets.recolor(...)`

Add to `style/assets.py`, modeled on `Assets.icon` but sized from the manifest:

```python
def recolor(self, name, *, white, black, magenta=None, transform=None):
    """Recolor a manifest element template and return its cached image result."""
```

- Colors are already-resolved strings. `white` and `black` are required
  structural-channel targets; `magenta` is an optional third fill-channel
  target (currently used by the slider handle). There is no cyan/teal channel.
- `transform` supports horizontal flip and quarter-turn rotations. Switch off
  uses a horizontal flip; vertical slider tracks, scrollbar parts, and
  progressbars use a quarter-turn. The transform is in the cache key and
  transforms metadata with the pixels.
- Final dimensions come from manifest width/height + `default_dpi` + current Tk
  scaling. Callers do not supply a second, drift-prone size.
- The cache key contains the asset name, snapped size, all target colors, and
  transform; it never contains the theme name.
- `RecolorRenderer` lazy-loads JSON and PNG sources and returns the image plus
  scaled manifest metadata. The fixed 2x source is recolored at source
  resolution and resized once; it does not use the procedural supersampler.

### 2. Public surface

The only public addition is **`Assets.recolor(...)`**. It returns an immutable
result containing the Tcl image name and scaled manifest metadata (`width`,
`height`, `border`, `padding`). This keeps custom-style construction possible
without turning the built-in template keys into a new top-level image API.

There is deliberately no `RecoloredImage` atom and no `recolor_element` sugar.
Icons are independently useful single-color content images; these templates are
multi-channel ttk element parts whose size and stretch rules come from a
manifest. Builders and public users compose `Assets.recolor` with the existing
`image_element`. `icon_element` stays untouched.

### 3. Source-channel recolor operation

The templates have four semantic source channels: **black, white, optional
magenta, and transparent alpha**. Black and white are structural regions;
magenta is a third fill region, not a focus/edge channel. Focus is represented
by rendering another state image with different target colors.

- Grayscale source pixels interpolate from `black` at 0 to `white` at 255. This
  preserves authored antialiasing between structural regions.
- Magenta-region pixels interpolate from `magenta` to `white` across the
  magenta-to-white transition in the slider source. This is the fill boundary,
  not a focus ring.
- Source alpha is copied unchanged. Fully transparent pixels remain transparent.
- No cyan/teal channel exists, and no transparent-background replacement exists.

### 3a. Surface / compositing — CONSTRAINT (settled, user 2026-06-28)

The single most important rule for this strand. A builder does **not** know the
actual background a given widget instance sits on — ttk styles are shared by name
(`primary.TCheckbutton` is one config applied to every primary checkbutton
regardless of its container), and the builders never look up a parent's
background. The only surface a builder has is the theme-global `self.colors.bg` /
`inputbg` / `selectbg`. This is structural, not a gap to fill; Workstream E keeps
the surface layer minimal and does **not** adopt a per-surface taxonomy.

Therefore:

- **Composite via true alpha. Always.** Render the source on a **transparent RGBA
  canvas** and recolor RGB while **preserving the source alpha** (the flat-tint
  method above). The asset then composites cleanly over *any* surface — no halo,
  no surface knowledge required. This is already how `Assets.circle/rounded_rect`
  and the icon renderer work; match it.
- **NEVER use the legacy `make_transparent(..., self.colors.bg)` pre-blend in a
  recolor asset.** That *bakes* a single assumed surface into the pixels, which is
  exactly the fringe-on-off-color-surface bug. (It's fine for flat *color* values
  like a disabled fg; just not for the recolorable image pixels.)
- **Contrast/knockout is NOT solved by alpha and stays a known limitation.** A
  light indicator on a light surface is still low-contrast with perfect alpha.
  The shared-style model can't make this per-surface. Keep the icon work's global
  contrast safety net (against `colors.bg`) and accept the global-`bg` assumption.

**The supported escape hatch — widget on a custom surface.** Handling a widget
that sits on a non-default background is the *user's* job via a **style
override** — set the style's `background`/`foreground`, render the template with
those resolved values through `Assets.recolor`, and install it with
`image_element`. The resolved colors produce a distinct cache key, while
true-alpha edges composite cleanly over the custom background.

Contrast this with legacy `make_transparent`-baked assets, where the surface was
in the pixels, so overriding `background` alone left the indicator's fringe still
blended against the old `bg`. Document this escape hatch in the public docstrings.
The one thing the override can't do for the user is *choose* a good contrasting
foreground — that's their value judgment, same as today.

### 4. Where the assets live + packaging

- New dir: **`src/ttkbootstrap/assets/elements/`** (sibling of `assets/icons/`),
  with a `README.md` describing the bootstack-derived/adapted provenance and
  source-channel contract. `manifest.json` is authoritative for dimensions,
  source DPI, border, and padding.
- **Packaging gotcha (already hit once):** the `assets/*` glob in
  `pyproject.toml` package-data does **not** recurse. `assets/icons/*` had to be
  added explicitly (PR 6a). Add **`assets/elements/*`** the same way, and add a
  test that the files resolve from an installed layout (resolve paths relative to
  `__file__`, like `_ICONS_DIR` in `icons.py`, so it works from a wheel).
- A regen/import tool under `tools/` (like `tools/generate_icon_metrics.py`) if
  the assets need any offline preprocessing.

### 5. Builder migration (one PR per widget, or grouped)

For each of radio / checkbox / switch / scale / scrollbar / progressbar:

- Replace the `create_*_assets` glyph/draw calls (or `a.icon(...)` /
  `a.circle(...)`) with `a.recolor(...)` + `image_element(...)`, preserving the
  existing **state-color math** (the `Colors.update_hsv(..., vd=±0.05)`
  pressed/active derivations) and the **scaled sizes** (`self.scale_size(...)`).
- Keep element names carrying the **full `{ttkstyle}.indicator` prefix** so the
  state-foreground lookup targets the configured style (the convention PRs 5/6b
  settled — see `builders_ttk.py` radiobutton/checkbutton).
- If a builder constructs a custom style whose terminal step is `layout()`, it
  auto-registers (PR 6b). For hand-built names, call `register_style` — otherwise
  `BootMixin` silently re-resolves `style="X"` to the base style (the PR-6a
  finding).
- Reference call sites to copy: `builders_ttk.py` round-scrollbar
  assets+style (~`783`), radiobutton `icon_element` (~`2334`), toggle indicators
  (~`1631`/`1697`), striped progressbar (~`320`).

Approved visual behavior:

- Selected radio is an accent annulus, not a center dot.
- Standard scrollbars are arrowless and use a recolored raster thumb; the native
  trough blends into the widget surface with `troughcolor=colors.bg`.
- Existing striped progressbars retain their stripe renderer.
- Add a distinct **thin progressbar** variant using `progressbar-thin.png`,
  selected with `bootstyle="thin"`; add `THIN` to the public constants and the
  current bootstyle grammar.

### 6. Gates (every prior toolkit PR ran these — keep them)

- Headless suite green (`python -m pytest -q`); add tests under
  `tests/widget_styles/` asserting color-at-pixel for a recolored asset and a
  theme-switch dedupe/no-stale check (copy `test_image_cache.py` patterns).
- **Standalone-import cycle guard**: the new renderer module must import alone
  (leaf: PIL + stdlib + the two leaf toolkit modules; reach `Style`
  function-locally, like `icons.py` does). Add it to the cycle-guard test.
- **PEP 649 annotation force-evaluation sweep** over new/migrated modules (3.14).
- **Human visual spot-check, light↔dark** — the headless suite asserts
  color-at-pixel, not appearance. Build a preview in `examples/` (model it on
  `examples/icon_preview.py`) showing all six widgets across states on a light
  and a dark theme. This is a merge gate, same as PR 6b.

## Locked decisions (user, 2026-06-28)

1. Recolored rasters replace current rendering for the six target widgets;
   icons remain for date/carets/sizegrip.
2. Use the staged bootstack-derived/adapted `assets/elements/` source set.
3. Use black/white structural channels, optional magenta fill, and preserved
   alpha; no cyan/teal channel and no alpha flattening.
4. Selected radio is an annulus; scrollbars are arrowless; striped progressbars
   remain striped; a new thin progressbar variant is included.
5. Public surface is `Assets.recolor` only; do not refactor `icon_element`.
6. Transforms are first-class: switch off is flipped horizontally, and vertical
   slider/scrollbar/progressbar parts are rotated from horizontal sources.
7. Land the renderer/assets foundation first, then migrate indicator widgets,
   then scale/scrollbar/progressbar, with visual checks before merge.

## Pointers (read these in the code)

- `src/ttkbootstrap/style/assets.py` — `_render`, `_even`, `_oversample`, the
  recipes, `Assets.icon`. **Copy the `icon` method's shape for `recolor`.**
- `src/ttkbootstrap/style/icons.py` — `IconRenderer` (lazy class-level asset
  cache, the render pipeline), `Icon`, `icon_element`, `_resolve_color`,
  `_state_foreground`. **The whole module is the template for the recolor one.**
- `src/ttkbootstrap/style/layout.py` — `image_element`, `state_map`,
  `register_style`.
- `src/ttkbootstrap/style/engine.py` — `_get_or_create_image`,
  `_image_cache`, `clear_image_cache`.
- `development/2_0_icons_design.md` — the closest precedent design; structure the
  recolor design pass the same way.
