# 2.0 — Recolorable raster widget assets (design brief)

> **Status: PROPOSAL / design-pass-not-yet-held.** This is a brief to refine
> with the user before implementing, per the project's hard rule (new public
> surface + engine-adjacent work gets a design pass first, like the engine /
> split / toolkit / icons strands did). Do not start coding the public surface
> until the open questions below are settled with the user.

## Goal

Let a set of built-in widgets be styled from **pre-made image assets that are
recolored on demand** — a collection of template/source images, each tinted to
the requested theme color at render time and cached — instead of (or alongside)
the font-glyph icons (`style/icons.py`) and geometric draws
(`Assets.circle/rect/rounded_rect`) used today.

**Target widgets (user's list):** radio, checkbox, switch (toggle), slider
(`Scale`), scrollbar, progressbar.

This mirrors bootstack, where a single grayscale/template asset is recolored for
any theme color rather than shipping one image per color.

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
  *derives* its cache key from the same inputs it renders from, so the key can't
  drift from the pixels. It already ports bootstack's snap-at-the-source
  pipeline: even-pixel-snap the final size, adaptive supersample (3×/2×/1×),
  LANCZOS downscale, `UnsharpMask`. **Reuse `_render` / the snap helpers.**
- `style/icons.py` `Assets.icon` + `icon_element` (PR 6a/6b): the exact
  precedent to copy. `icon` takes an *already-resolved* color and routes through
  the cache with key `("icon", name, snapped_size, color)`; `icon_element` is the
  per-widget-state sugar that renders one image per ttk state and bakes a
  validated, first-match-wins image element. **The recolor surface should be the
  same shape with a raster source instead of a font glyph.**
- `style/layout.py` (PR 5/6b): `image_element` (validated state→image element),
  `state_map`/`statespec` (the `!neg` / space-AND grammar), `layout()`/`El`, and
  **`register_style`** (`layout()` auto-registers so a toolkit-built style
  resolves via `style="..."`). Recolor assets plug straight into these.

So the work is: (1) a recolor recipe on `Assets`, (2) a `recolor_element`
mirroring `icon_element`, (3) a vendored asset directory + packaging, (4)
migrating the six target builders.

## Proposed design

### 1. The recolor recipe — `Assets.recolor(...)`

Add to `style/assets.py`, modeled on `Assets.icon`:

```python
def recolor(self, name, size, color, *, method="tint"):
    """Recolor a vendored template image to `color`, cached.

    `name` selects a source asset (see assets/widgets/); `size` is the final
    (DPI-scaled) pixel size; `color` is an already-resolved color string (keyword
    resolution lives in the public atom, like Icon). Returns the Tcl image name.
    """
    size = _wh(size); size = (_even(size[0]), _even(size[1]))
    key = ("recolor", name, size, color, method)        # NOTE: no theme name
    return self.style._get_or_create_image(
        key, lambda: ImageTk.PhotoImage(RecolorRenderer.render(name, size, color, method)))
```

- Takes a **resolved** color (consistent with `circle`/`rect`/`icon`); a public
  atom resolves keywords (see #2).
- Key is `("recolor", name, snapped_size, color, method)` — theme-independent.
- Renders through a `RecolorRenderer` (new, in a leaf module, mirroring
  `IconRenderer`): load the source once (class-level cache), apply the recolor,
  then the shared snap/supersample/LANCZOS/UnsharpMask pipeline.

### 2. The public atoms / state sugar

Mirror the icon surface so users get a consistent vocabulary:

- **`RecoloredImage(name, size, color=None)`** (working name) — the atom: resolve
  the keyword color once against the active theme, return a cached Tk image
  usable as `image=`. Same shape as `Icon(...)`.
- **`recolor_element(style, name, *, size, default, states=None, **options)`** —
  the per-state sugar, a near-copy of `icon_element`: each per-state spec renders
  via `Assets.recolor` and assembles a validated image element. Reuse
  `icon_element`'s spec grammar verbatim (bare string = asset name, color follows
  the configured foreground; `{name?, color?}` dict otherwise) and its
  `<ttkstyle>.<element>` naming + foreground-lookup rule.

**Strongly consider generalizing instead of copy-pasting.** `icon_element` and
`recolor_element` differ only in the per-spec renderer (`assets.icon` vs
`assets.recolor`). Factor the shared body into one internal helper that takes the
render callable, and keep `icon_element` / `recolor_element` as thin wrappers.
Confirm this refactor with the user (it touches the just-merged icon code).

Re-export the public names from `style/__init__.py` **and** top-level
`ttkbootstrap` (the pattern every toolkit PR followed). Keep `import ttkbootstrap`
warning-free and the source-asset load lazy (font is loaded on first render
today — match that: don't read PNGs at import).

### 3. The recolor operation itself (the one real new decision)

How a source image maps to `color`. Pick per asset type:

- **Flat tint (monochrome source).** Source is a single-color/alpha silhouette
  (like a glyph). Replace RGB with `color`, **keep the source alpha**. Cheapest,
  matches the flat 2.0 aesthetic, and is what most of these widgets want
  (indicator dots, toggle knobs, scrollbar thumbs, progressbar fills).
  Implementation: split alpha, build `Image.new("RGBA", size, color)`, reattach
  the source alpha.
- **Luminance-preserving recolor (shaded source).** If a source has shading you
  want to retain (subtle gradients/bevels — probably not needed for the flat
  look), multiply a solid `color` layer against the source luminance, or map via
  a palette. Heavier; only if a flat tint looks wrong.
- **Multi-region / palette replace.** If one source needs two theme colors (e.g.
  a track + a thumb in one image), use an indexed-palette source and replace
  named palette entries. Adds complexity — prefer **one asset per recolorable
  region** and compose at the layout level instead.

**Recommendation:** start with **flat tint** only; it covers the target widgets
and keeps the renderer tiny. Add luminance-preserving later only if a real asset
needs it. Whatever methods exist must be **in the cache key** (the `method` arg
above) so two methods on the same source don't collide.

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
override** — set the style's `background` (their surface) and, if contrast needs
it, `foreground`. This is the same workflow as today, but it composes *better*
here: because `recolor_element` derives the indicator color from the style's
**configured foreground** (and the cache is keyed on the resolved color), the
override is self-consistent in one step —

1. user overrides the style → sets `background` + a contrasting `foreground`;
2. the indicator color *follows that foreground* → new resolved color → new cache
   key → it re-renders in the right color automatically (no manual asset regen);
3. true-alpha edges composite cleanly over the new background.

Contrast this with legacy `make_transparent`-baked assets, where the surface was
in the pixels, so overriding `background` alone left the indicator's fringe still
blended against the old `bg`. Document this escape hatch in the public docstrings.
The one thing the override can't do for the user is *choose* a good contrasting
foreground — that's their value judgment, same as today.

### 4. Where the assets live + packaging

- New dir: **`src/ttkbootstrap/assets/widgets/`** (sibling of `assets/icons/`),
  with a `README.md` + `LICENSE` describing provenance (port from bootstack's
  asset set if that's the source). Source images as PNG with alpha.
- **Packaging gotcha (already hit once):** the `assets/*` glob in
  `pyproject.toml` package-data does **not** recurse. `assets/icons/*` had to be
  added explicitly (PR 6a). Add **`assets/widgets/*`** the same way, and add a
  test that the files resolve from an installed layout (resolve paths relative to
  `__file__`, like `_ICONS_DIR` in `icons.py`, so it works from a wheel).
- A regen/import tool under `tools/` (like `tools/generate_icon_metrics.py`) if
  the assets need any offline preprocessing.

### 5. Builder migration (one PR per widget, or grouped)

For each of radio / checkbox / switch / scale / scrollbar / progressbar:

- Replace the `create_*_assets` glyph/draw calls (or `a.icon(...)` /
  `a.circle(...)`) with `a.recolor(...)` / `recolor_element(...)`, preserving the
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

## Open questions for the user (settle before coding)

1. ~~**Replace or coexist?**~~ **RESOLVED (user, 2026-06-28): replace.** For the
   six listed widgets the recolored rasters replace the current rendering (icon
   quality not good enough for general widget indicators). The icon engine and
   glyph icons stay for all *other* widgets (date/carets/sizegrip). See the
   decision + per-widget table at the top.
2. **Asset source.** Are the source images coming from bootstack's asset set, to
   be hand-authored, or generated? This decides the `tools/` step and the
   LICENSE/README provenance.
3. **Recolor method scope.** Is flat tint enough (recommended), or is a
   shaded/luminance-preserving or multi-region asset in scope?
4. **One element per region vs multi-color source** for scrollbar (track+thumb)
   and progressbar (trough+bar) — recommend one asset per recolorable region.
5. **Generalize `icon_element` → shared core** (recommended) vs a standalone
   `recolor_element` copy? The former edits recently-merged icon code.
6. **Scope/sequencing.** One design PR + renderer first (no builder changes, like
   PR 6a was for icons), then per-widget migration PRs gated on the visual
   spot-check? That worked well for the icon strand and is the recommended shape.

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