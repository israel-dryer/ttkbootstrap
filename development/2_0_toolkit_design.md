# ttkbootstrap 2.0 — Style-Construction Toolkit Design (Workstream I, Tier 1)

> Output of the Workstream I design pass (2026-06-25). Pairs with
> `development/2_0_plan.md` (durable worklist, Workstream I at lines ~246–284),
> `development/2_0_handoff.md` (session state), and the engine design
> (`development/2_0_engine_design.md` — PR 2 built the `_get_or_create_image`
> chokepoint this toolkit wraps). Line refs are point-in-time against the
> `style/` package on the `2.0` branch — verify before relying.

## Scope

Workstream I, **Tier 1 only**: the mechanical, low-risk public helpers that make
image/state-based ttk styles tractable, and that de-duplicate the asset/layout
boilerplate in `builders_ttk.py`. Tier 2 (`state_colors` from ramp steps,
composite recipes) depends on the semantic-anchor model (Workstream E) and is
**out of scope** here.

This is a design pass first, per the established discipline (engine, split, and
mixin work each got one). **No code moves until the API shape below is signed
off.** The toolkit is a **new public API surface** — the delivery vehicle for
"make custom styles easy" — so it earns the same up-front design as the engine.

The toolkit lands in **`style/assets.py`** (image construction) and
**`style/layout.py`** (layout/element/statespec/name helpers). Neither file
exists yet (the split deliberately did not pre-create them).

## The acceptance test (from the plan)

> Rewriting `create_scale_assets` / `create_radiobutton_style` on the toolkit
> must come out **shorter and clearer**, or the abstraction is wrong.

This doc designs the API *against* those two builders and shows the before/after
(see "Acceptance test — proof" below). They were chosen well: between them they
exercise every Tier-1 primitive — shape-recipe assets, a custom composite draw,
a state→image element map, a nested layout pyramid, and the colorname/`.TS`
name dance.

## The warts, catalogued from current code

Surveyed across `builders_ttk.py` (30 `Image.new` sites, ~40 `_get_or_create_image`
calls, ~25 `layout()` pyramids). The recurring shapes:

1. **Per-asset SSAA boilerplate.** Every image draw is
   `Image.new("RGBA", (OVERSAMPLE, OVERSAMPLE))` → draw → `ImageTk.PhotoImage(
   img.resize(size, Resampling.LANCZOS))`, repeated ~25× verbatim. The
   oversample canvas is an inconsistent magic number per family — `(100,100)`,
   `(134,134)`, `(226,130)`, `(210,220)`, `(13,11)`, `(11,11)` — with draw
   coordinates hand-fitted to *that* canvas (`[1,1,133,133]`, `[40,40,94,94]`,
   ellipse `(0,0,95,95)` on a 100-px canvas).

2. **Hand-built cache keys that must mirror the closure.** Every
   `_get_or_create_image(("radio.on", light_outline, on_fill, on_indicator,
   off_border, tuple(size)), make_on)` call re-lists, by hand, exactly the values
   `make_on` closes over. **The entire PR 2 purity audit (pre-flight check (b))
   existed to get these keys right** — a key that drifts from the draw silently
   returns a stale-color image after a theme switch. This is the toolkit's
   highest-value target: make the key *fall out of* the render description so it
   cannot drift.

3. **Positional bare-string image statespecs.** `element_create(name, "image",
   default, ("disabled", img), ("pressed", img), ...)` — order-significant
   tuples with unvalidated state strings.

4. **Nested layout tuple/dict pyramids.** A 3-level indicator/focus/label tree is
   ~30 lines of `(name, {"children": [(name, {"sticky": ...}), ...]})`
   (radiobutton ~`2682`, scale ~`715`).

5. **Name/orientation surgery + the `DEFAULT/""` dance.** Every builder opens with
   `if any([colorname == DEFAULT, colorname == ""])` and threads
   `f"{colorname}.{STYLE}"` plus `h_ttkstyle.replace(".TS", ".S")` to derive the
   element prefix.

## Design principle

**Thin helpers, not a DSL.** The toolkit is a *new public compat surface* — every
symbol is something we must keep working through 2.x. Keep it small and
orthogonal: each helper does one mechanical job, composes with raw ttk calls
(you can mix toolkit and `style.element_create` freely), and adds no runtime
state of its own beyond the existing `Style._image_cache`.

**The key is derived, never hand-written.** The single biggest correctness win:
a render's cache key is computed from the inputs that determine its pixels, so it
is impossible to write a draw whose key omits a color it uses. Shape recipes make
this automatic; the escape hatch makes it explicit-but-adjacent (the key parts
sit in the same call as the draw, not 15 lines away).

## `style/assets.py` — image construction

A small `Assets(style)` facade bound to the engine's cache. Builders reach it via
a cached `self.assets` property; public users construct `Assets(Style.get_instance())`.

### Shape recipes (renderer + key in one)

These cover the bulk of assets (any single filled/outlined primitive). The recipe
*is* both the renderer and the key — you cannot under-specify the key:

```python
a = Assets(style)              # internally: self.assets

a.circle(fill, size, *, outline=None, width=0)
a.rect(fill, size)                                   # solid fill, no AA needed
a.rounded_rect(fill, size, radius, *, outline=None, width=0)
```

- `size` is the **final widget pixel size** (already DPI-scaled by the caller;
  int → square, or `(w, h)`). The recipe owns the **snapped SSAA pipeline ported
  from bootstack** (see the resolved fidelity section): even-pixel-snap the size,
  pick the adaptive oversample factor (3×/2×/1× by size), draw on the
  `snapped_size × oversample` canvas, snap the draw origin to oversample multiples,
  `LANCZOS` downscale, `UnsharpMask`, wrap in `PhotoImage`. **No `oversample`
  parameter on the public signature** — it's internal and adaptive.
- Returns the Tcl image name (same contract as `_get_or_create_image`).
- The key is built internally as `("circle", fill, snapped_size, outline, width)`
  etc. — **complete by construction, theme-independent** (resolved hex is in the
  key, so cross-theme-identical assets dedupe; this is exactly PR 2's invariant,
  now enforced by the recipe instead of by audit). The *snapped* size is in the
  key, so two logical sizes that snap equal share one image.

### General escape hatch (custom composite draws)

For the handful of multi-shape draws (radio "on" = concentric circles, the
date-button calendar, striped polygons, arrow glyphs), an explicit draw with an
explicit-but-adjacent key:

```python
a.image(size, draw_fn, *key_parts)
```

- `draw_fn(draw, w, h)` receives a fresh `ImageDraw.Draw` over the oversampled
  `(w, h)` canvas (where `w, h` is the snapped size × the adaptive oversample); it
  draws relative to `w, h` (so the magic `134`/`94`/`40` oversample constants
  become `w`-relative expressions, killing wart #1's coordinate coupling). The
  snap + downscale + `UnsharpMask` happen around `draw_fn` exactly as in the
  recipes.
- Key = `(draw_fn.__qualname__, snapped_size, *key_parts)`. The caller still
  lists the colors the draw uses in `*key_parts`, **but they sit in the same call
  as the draw**, not in a detached tuple — and the `__qualname__` distinguishes
  draws so two different shapes never collide on equal key_parts.
- Still removes `Image.new` / `.resize(LANCZOS)` / `PhotoImage` /
  separate-`_get_or_create_image` boilerplate even where a recipe doesn't fit.

`a.rect` skips oversampling (axis-aligned solid fill has no edges to anti-alias —
matches today's `Image.new("RGB", size, color)` exactly).

### How it wraps PR 2

`Assets` is a thin layer over `Style._get_or_create_image(key, factory)`:

```python
class Assets:
    def __init__(self, style): self.style = style
    def circle(self, fill, size, *, outline=None, width=0, oversample=8):
        size = _wh(size)
        key = ("circle", fill, size, outline, width)
        return self.style._get_or_create_image(key, lambda: _draw_circle(...))
```

`_get_or_create_image` stays the private chokepoint and the single source of cache
truth; `Assets` is the public, ergonomic, key-safe front door to it. No second
cache, no behavior change to the cache itself.

## `style/layout.py` — layout, elements, statespecs, names

### `layout()` + `El` — the layout-pyramid killer

```python
from ttkbootstrap.style.layout import layout, El

layout(style, ttkstyle,
    El("Radiobutton.padding", sticky=NSEW, children=[
        El(f"{ttkstyle}.indicator", side=LEFT),
        El("Radiobutton.focus", side=LEFT, children=[
            El("Radiobutton.label", sticky=NSEW),
        ]),
    ]),
)
```

`El(name, *, side=, sticky=, expand=, border=, children=[])` carries the ttk
element options as keywords; `layout()` lowers the `El` tree to ttk's
`(name, {opts, "children": [...]})` nested form and calls `style.layout(...)`.
Pure structural sugar — the biggest readability win, zero behavioral surface.

### `image_element()` — named, validated state→image map

```python
image_element(style, f"{ttkstyle}.indicator", default=on,
    states={"disabled selected": on_disabled,
            "disabled": on_disabled_alt,
            "!selected": off},
    width=width, border=border, sticky=W)
```

Wraps `element_create(..., "image", default, *statespecs, **opts)`. `states` is an
**ordered** dict (ttk statespecs are first-match-wins; dict insertion order is the
match order, made explicit). Each key is validated via `statespec` below — a typo
like `"diabled"` fails loudly instead of silently never matching (the natural home
for Workstream D's loud-failure validation).

### `statespec` / `state_map()` — grammar validation

```python
statespec("disabled selected")     # -> ("disabled", "selected")  (validated)
statespec("!selected")             # -> ("!selected",)
state_map(disabled=disabled_fg)    # -> [("disabled", disabled_fg)]  for style.map
```

Validates the `!negation` + space-AND grammar against the known ttk/bootstyle
state tokens; raises on unknown tokens. `state_map()` is the `style.map(...)`
analog (replaces bare `foreground=[("disabled", fg)]` lists). Loud-failure
validation here is the seam shared with Workstream D — keep the token set in one
place both can import.

### `StyleName` — the `DEFAULT/""` + `.TS→.S` absorber

```python
sn = StyleName("TScale", colorname, orient="Horizontal")
sn.colorname  # PRIMARY when input was DEFAULT/"" (per-widget default), else as given
sn.ttk_style  # "Horizontal.TScale" or "primary.Horizontal.TScale"
sn.element  # "Horizontal.Scale"  (drops the T from the ttk class token)
```

Absorbs `if any([colorname == DEFAULT, colorname == ""])`, the
`f"{colorname}.{STYLE}"` prefixing, the `.replace(".TS", ".S")` element-name
derivation, and the "default colorname → PRIMARY" rule that ~30 builders repeat.
Lowest-risk, most-mechanical primitive; orthogonal to the image/layout helpers.

### Alignment with bootstack's `Element` / `ElementImage`

bootstack already ships these analogs (`style/element.py:6-174`), which is a
maintenance asset — the same author keeps both mental models in sync:

- `El` ≈ bootstack's **`Element(name, *, expand, side, sticky, border)`** with a
  recursive **`.spec()`** that lowers to the ttk `(name, {opts, "children":[...]})`
  tuple/dict. Port the `.spec()` lowering directly.
- `image_element` ≈ bootstack's **`ElementImage(...).state_specs([...]).build()`**,
  which returns `(name, args, options)` for `element_create`. Port the `build()`
  arg assembly.

Two **deliberate divergences** (keep ttkbootstrap's simpler shape, note why):

- Use a **constructor `children=[...]` kwarg**, not bootstack's fluent
  `.children([...])`. bootstack's `children()` parents siblings positionally
  (`elements[i-1]`), which is fragile; the kwarg form is unambiguous and reads as
  the tree it builds.
- Keep `statespec`/`state_map` as **validating** helpers (loud failure on unknown
  tokens — the Workstream D seam). bootstack's state maps are plain
  `(state, value)` lists with no validation; ttkbootstrap adds the check.

## Acceptance test — proof

### `create_scale_assets` (assets): ~64 lines → ~22

The `make_thumb` closure, the six `_get_or_create_image` calls with hand-built
keys, and every `Image.new` / `.resize(LANCZOS)` / `PhotoImage` disappear:

```python
def create_scale_assets(self, colorname=DEFAULT, size=14):
    size = self.scale_size(size)
    a = self.assets
    if self.is_light_theme:
        disabled = self.colors.border
        track = self.colors.bg if colorname == LIGHT else self.colors.light
    else:
        disabled = self.colors.selectbg
        track = Colors.update_hsv(self.colors.selectbg, vd=-0.2)
    normal = self.colors.primary if colorname in (DEFAULT, "") \
        else self.colors.get(colorname)
    pressed = Colors.update_hsv(normal, vd=-0.1)
    hover = Colors.update_hsv(normal, vd=0.1)
    h_size, v_size = self.scale_size((40, 5)), self.scale_size((5, 40))
    return (
        a.circle(normal,   size),
        a.circle(pressed,  size),
        a.circle(hover,    size),
        a.circle(disabled, size),
        a.rect(track, h_size),
        a.rect(track, v_size),
    )
```

The state-color *math* stays (that's the builder's real content); the **plumbing**
is gone. Each `a.circle(c, size)` keys on `("circle", c, (size,size), None, 0)` —
no hand-written key, no purity hazard.

### `create_radiobutton_style` (style): ~67 lines → ~18

```python
def create_radiobutton_style(self, colorname=DEFAULT):
    sn = StyleName("TRadiobutton", colorname)
    disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
    off, on, disabled, on_disabled = self.create_radiobutton_assets(sn.colorname)
    image_element(self.style, f"{sn.ttk_style}.indicator", default=on,
                  states={"disabled selected": on_disabled,
                          "disabled": disabled,
                          "!selected": off},
                  width=self.scale_size(20), border=self.scale_size(4), sticky=W)
    state_map(self.style, sn.ttk_style, foreground={"disabled": disabled_fg})
    self.style._build_configure(sn.ttk_style)
    layout(self.style, sn.ttk_style,
           El("Radiobutton.padding", sticky=NSEW, children=[
               El(f"{sn.ttk_style}.indicator", side=LEFT),
               El("Radiobutton.focus", side=LEFT, children=[
                   El("Radiobutton.label", sticky=NSEW)])]))
    self.style._register_ttkstyle(sn.ttk_style)
```

The 30-line layout pyramid → 5 readable lines; the positional statespecs → a named
dict; the colorname/element dance → one `StyleName`. **Both targets pass: shorter
and clearer.** The `create_radiobutton_assets` companion uses `a.circle` for the
off/disabled states and `a.image(size, draw_on, light_outline, on_fill,
on_indicator, off_border)` for the two concentric-circle "on" states — its key
parts now sit beside the draw.

## Public exposure

The toolkit is public (dogfooded internally + the headline "build your own style"
API). Re-export plan:

- `style/__init__.py` re-exports `Assets`, `image_element`, `layout`, `El`,
  `statespec`, `state_map`, `StyleName` (alongside the existing surface), so
  `from ttkbootstrap.style import Assets, layout, El` works.
- Top-level `ttkbootstrap` re-exports the same names for custom-style authoring
  (the import block at `__init__.py:59`). Keep `import ttkbootstrap` warning-free.
- The submodules `style.assets` / `style.layout` are the canonical homes;
  `style.engine._get_or_create_image` stays private.

## Layering / import safety

`assets.py` and `layout.py` sit **above** `engine.py` in the package layering
(they consume `Style`), **below** `bootstyle.py` is not required — they are leaves
that nothing in the core imports at module top-level:

- `assets.py` top-level imports: `from math import ceil` (or reuse), PIL bits
  (`Image, ImageDraw, ImageTk, Resampling`). It needs a `Style` **instance** at
  call time (passed in), not the class at import time → **no top-level edge to
  `engine`**, so no cycle. Mirror the split's function-local-back-edge discipline
  if a class import is ever needed.
- `layout.py` top-level imports: `tkinter` constants only; it calls methods on the
  `style` instance passed in. No engine import.
- `builders_ttk.py` gains `from .assets import Assets` and
  `from .layout import layout, El, image_element, statespec, state_map, StyleName`
  — these are **downward** (builders → toolkit-leaves that don't import builders),
  import-safe. Verify with the standalone-import cycle guard from the split.

**Carry the PEP 649 annotation force-evaluation sweep** (split design doc's
notable finding): the dev interpreter is 3.14, where a missing annotation-only
import imports clean and only `NameError`s on `__annotations__` access. Run the
sweep over the two new modules + the migrated builders.

## The one open decision — pixel fidelity of migrated builders

The shape recipes are **good defaults, not bit-exact replicas** of today's draws.
Concrete divergences the recipes would introduce:

- Scale thumb draws ellipse `(0,0,95,95)` on a 100-px canvas — a deliberate ~5%
  margin. `a.circle` draws full-bleed unless given an inset.
- Radio/check use a `134`-px canvas with `[1,1,133,133]` insets and a fixed
  oversample ratio; recipes use a uniform `oversample` factor.

These are **sub-pixel anti-aliasing / edge differences**, not color changes. PR 2's
purity tests assert *which color a key pixel is* (robust to AA), not whole-image
equality — so they would still pass. The question is whether to:

- **(A) Accept sub-pixel AA drift** (recommended) — same latitude Workstream E
  already takes on theme-palette drift; keeps the recipes clean (no per-site
  inset/oversample knobs leaking the old magic numbers back in). Add an optional
  `inset=`/`oversample=` only where a specific widget visibly regresses.
- **(B) Preserve pixels exactly** — recipes grow `inset`/absolute-canvas params so
  each migrated builder reproduces its current draw byte-for-byte. Faithful, but
  drags wart #1's magic constants into the public API and dilutes the "clearer"
  win.

Recommend **(A)**, with a pre-migration check that `tests/widget_styles/
test_image_cache.py` (and any visual assertion) tests *color-at-pixel*, not image
equality — and a spot visual diff on scale + radio + check before merge.

A second, smaller scope question (lower stakes): **land Tier 1 in one PR, or split
assets vs layout?** **LOCKED: one PR** — they're co-designed, the acceptance test
spans both, and the migration of a builder touches both at once. It's larger than
the pure split but every changed builder is regression-netted by the existing
style-value + image-cache suites.

### RESOLVED — bootstack's snap-at-the-source pipeline dissolves the (A)/(B) split

User guidance (2026-06-25): *"bootstack figured out a way to keep from doing
sub-pixel adjustments by rounding the scaling and also some other tricks. Might be
worth a look there to avoid having to re-invent the wheel."* Mined bootstack
(`src/bootstack`); it confirms the steer and gives us a **better** answer than
either (A) or (B): don't *manage* drift, **eliminate it at the source** by snapping
sizes to whole/even pixels before rendering. With that pipeline the recipes produce
crisper assets than today's hand-fit canvases, and "fidelity" stops being a knob.

The four mechanisms to port verbatim into `Assets` (file refs into bootstack):

1. **Round the DPI factor, never truncate** (`_runtime/utility.py:250-268`,
   `scale_icon_size` → `max(base, round(base * ui_scale))`). ttkbootstrap's current
   `scale_size` (`builders_ttk.py:72`) uses `ceil` — already rounds *up*, but the
   real fix is the next step.
2. **Even-pixel snap the final size before keying/rendering**
   (`_core/images.py:364`, `style/utility.py:516`):
   `size = size if size % 2 == 0 else size + 1`. This is the trick that kills the
   half-pixel LANCZOS blur at fractional DPI (125 %, 150 %). The snap happens inside
   the recipe, so the cache key uses the snapped size → identical logical sizes
   dedupe and land crisp.
3. **Adaptive supersample, then snap the draw origin to oversample multiples**
   (`_core/images.py:393-406`): `3×` for `<32 px`, `2×` for `<64 px`, `1×` for
   `≥64 px`; draw origin rounded to a multiple of the oversample factor so the glyph
   lands on whole pixels after downscale. Replaces the per-builder magic canvases
   (`100`/`134`/`226`) with one principled factor.
4. **LANCZOS downscale + `UnsharpMask` to restore edge crispness**
   (`_core/images.py:459-461`, `style/utility.py:137`):
   `img.resize(size, LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.6,
   percent=60, threshold=0))`. The sharpen is what makes the snapped result read
   crisper than the current bare-LANCZOS output.

**Decision (LOCKED): adopt bootstack's snapped pipeline** (a stronger form of (A)).
The migrated assets will differ from today at the pixel level — *by being sharper
and DPI-stable* — not by drifting color. PR 2's purity tests assert color-at-pixel
(robust to this), so they pass; add a spot visual diff on scale/radio/check to
confirm the quality is equal-or-better. No per-recipe `inset`/`oversample` knobs
leak into the public API — option (B) is dropped. The recipe owns the snap +
adaptive-oversample + unsharp internally; callers pass only the logical size.

One caveat to carry into implementation: a few existing draws encode a deliberate
margin in their canvas (scale thumb's `(0,0,95,95)` on a 100-px canvas ≈ 5 % inset).
Where a recipe's full-bleed default changes a widget's *visual weight* (not just its
AA), reproduce the margin as a documented constant inside that recipe's default —
not as a public knob.

## PR scope & sequencing

One PR (`feat/2.0-pr5-toolkit`), per the recommendation above:

1. Add `style/assets.py` (`Assets` + recipes + `image`) and `style/layout.py`
   (`layout`/`El`/`image_element`/`statespec`/`state_map`/`StyleName`).
2. Re-export from `style/__init__.py` and top-level `ttkbootstrap`.
3. Migrate the **two acceptance-test builders** (`create_scale_*`,
   `create_radiobutton_*`) first as the proof; land them, confirm suite + visual.
4. Migrate the remaining asset/layout sites opportunistically (separate commits
   within the PR, or a fast-follow PR if the diff gets large) — the recipes are
   the same shapes repeated, so this is mechanical once the two proofs land.
5. New tests: recipe key-completeness (same inputs → same name; one differing
   color → different name), **even-size snap** (an odd logical size and the
   next even one resolve to the same image/key; the rendered size is even),
   `El`→ttk-tuple lowering (matches the hand-written nested form), `statespec`
   validation (good + raises-on-typo), `StyleName` (`DEFAULT/""`→PRIMARY,
   `.TS→.S`, color-prefix). Keep `import ttkbootstrap` warning-free.

Tier 2 (`state_colors` from ramp steps; composite recipes) is deferred to after
Workstream E, as the plan sequences it.

## Verification plan

- `python -m pytest -q` → still **61 passed** plus the new toolkit tests.
- Acceptance: the two migrated builders are shorter (line count) and pass the
  existing style-value + `test_image_cache.py` assertions unchanged.
- Cache invariant preserved: a theme round-trip still holds `_image_cache` flat
  (the recipe keys are theme-independent by construction).
- Snapped pipeline (ported from bootstack): rendered asset sizes are even; a spot
  visual diff on scale/radio/check confirms equal-or-better crispness vs today
  (sharper, DPI-stable — not color drift). `test_image_cache.py` color-at-pixel
  assertions pass unchanged.
- Standalone-import cycle guard for `style.assets` / `style.layout`; PEP 649
  annotation force-evaluation sweep over the new modules + migrated builders.
- `import ttkbootstrap` warning-free; the new public names import from both
  `ttkbootstrap` and `ttkbootstrap.style`.
