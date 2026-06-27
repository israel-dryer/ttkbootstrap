# ttkbootstrap 2.0 — Icon-Rendered Assets Design (Workstream I, Tier 1.5)

> Design pass (2026-06-27). Pairs with `development/2_0_plan.md` (Workstream I),
> `development/2_0_toolkit_design.md` (PR 5 toolkit this builds on),
> `development/2_0_engine_design.md` (PR 2 `_get_or_create_image` chokepoint),
> and `development/2_0_handoff.md` (session state). Supersedes the hand-drawn
> glyph half of the held PR 6. Line refs are point-in-time against the `2.0`
> branch — verify before relying.

## Why this exists

The PR 6 fast-follow migrated the asset builders onto the PR 5 toolkit, but the
hand-drawn **glyph** assets (checkmark, calendar, arrows, sizegrip) still looked
poor — the user confirmed they "don't look great." Root cause: we hand-stroke
glyph shapes onto an oversampled canvas and downscale, and our glyph text draws
carry a hand-tuned `font_offset` fudge because PIL's `getbbox` mis-reports the
ink box of full-bleed icon fonts. Sub-pixel-correct glyph rendering is a solved
problem in the sibling **bootstack** project; we adopt its mechanism natively.

**The decision (LOCKED with the user, 2026-06-27):** render glyph-shaped widget
assets from the **Bootstrap Icons** font, vendored into ttkbootstrap, using
bootstack's metrics-based fit-and-center renderer. Keep the geometric recipes
(`circle`/`rect`/`rounded_rect`) for the pure-geometric assets. This is a
**blend**: bootstack's render pipeline + ttkbootstrap-icons' name-mapping
ergonomics, owned and vendored by us — **no new pip dependency**, no coupling to
either project's packaging.

## The quality win, precisely

bootstack's `_ImageService._render_icon` (`bootstack/src/bootstack/_core/images.py:374`)
differs from a naive `draw.text` in exactly one decisive way: a **precomputed
`icon_metrics.json`** maps each glyph name → its normalized ink bounding box
`[left, top, width, height]` in em-fractions (generated offline at 512 px via the
glyph's alpha channel). At render time it **fits the true ink box to the target
frame and centers on the ink** — accurate for full-bleed glyphs, free of
`getbbox` skew, no per-glyph offset. Everything else in its pipeline —
even-pixel snap, adaptive 3×/2×/1× oversample, LANCZOS + `UnsharpMask(0.6, 60,
0)` — **is already what `style/assets.py:_render` does** (we ported it in PR 5).

So this feature is *mostly code we already have*. The genuinely new parts:
1. the glyph **fit-and-center** step (metrics lookup + font sizing), and
2. three **vendored assets**.

## Vendored assets (Bootstrap Icons, MIT)

Copied from `bootstack/src/bootstack/assets/icons/` into
`src/ttkbootstrap/assets/icons/`:

| asset | size | role |
|---|---|---|
| `bootstrap.ttf` | 447 KB | the 2078 glyphs |
| `glyphmap.json` | 54 KB | name → codepoint (the *mapping*) |
| `icon_metrics.json` | 109 KB | name → em-fraction ink bbox (the *alignment fix*) |

~610 KB of package data. Also vendor bootstack's `tools/generate_icon_metrics.py`
under `development/` (or `tools/`) so the metrics can be regenerated if the font
is ever updated. Record the Bootstrap Icons version + MIT license in a
`src/ttkbootstrap/assets/icons/LICENSE` / `README`. Add the assets dir to
`pyproject.toml` package-data so it ships in the wheel/sdist.

## Module layout — `style/icons.py` (new leaf)

A new submodule paralleling `assets.py`/`layout.py` in the package layering
(leaf; nothing in the core imports it at module top-level):

```python
# style/icons.py
class IconRenderer:
    """Lazy-loads the vendored font + glyphmap + metrics; renders one glyph to a
    PIL image using the metrics-based fit. Stateless except the cached assets."""
    _font_bytes = _glyphmap = _metrics = None   # class-level, loaded once

    @classmethod
    def render(cls, name, size, color) -> PIL.Image: ...   # the ported pipeline
```

- Top-level imports: PIL bits + `json`/`io`/`pathlib` only — **no engine edge**,
  so no import cycle (mirror the split's leaf discipline; verify with the
  standalone-import cycle guard).
- Reuses `assets.py:_render`/`_even`/`_oversample` for the snap/oversample/sharpen
  tail (factor those into a shared private spot if cleaner, or import them).

### Integration with the cache + the `Assets` facade

The glyph render routes through the **same** PR 2 chokepoint, so it dedupes and
evicts with every other asset:

```python
# on Assets (style/assets.py), beside circle/rect/rounded_rect:
def icon(self, name, size, color):
    """Render a Bootstrap Icons glyph as a cached widget asset.

    `size` is the final (DPI-scaled) pixel size; `color` is a resolved hex.
    Returns the Tcl image name (same contract as the shape recipes)."""
    size = _wh(size); size = (_even(size[0]), _even(size[1]))
    key = ("icon", name, size, color)
    return self.style._get_or_create_image(
        key, lambda: ImageTk.PhotoImage(IconRenderer.render(name, size, color)))
```

Key = `("icon", name, snapped_size, color)` — **theme-independent by
construction** (resolved color is in the key), exactly PR 2's invariant. Two
themes that resolve a glyph to the same color share one image.

## Public surface — RESOLVED (user, 2026-06-27): two layered helpers

Expose **both** the atom and a per-state map sugar, layered on the existing PR 5
toolkit (`a.icon` → `image_element` are already public/composable):

- **`Icon(name, size, color)` / `a.icon(...)`** — the atom: render one glyph to a
  cached Tk image. Re-exported from `ttkbootstrap` and `ttkbootstrap.style`.
  Bootstrap-only, **no provider pattern** (the multi-font abstraction in
  `ttkbootstrap_icons` 4.0 is out of 2.0 scope). Useful standalone (a button
  image, a label).
- **`icon_element(style, name, *, size, default, states, **options)`** — the
  `Style.map`-aligned sugar the user asked for, sitting **beside `image_element`**
  in the toolkit. It renders each per-state spec via `a.icon` and assembles a
  validated ttk image element (same first-match-wins `statespec` grammar as
  `image_element`/`state_map`). One declarative call replaces *both* a
  `create_*_assets` method and its `image_element` wiring.

  **Per-state spec grammar** (RESOLVED — adapted from ttkbootstrap-icons'
  `StatefulIconMixin._parse_statespec`, with `name`/`color` independently
  optional). `default` and each `states` value is one of:
  - **bare string** → the icon *name*; color **follows the foreground** for that
    state (our indicators change the name per state, so the bare form is name).
  - **dict `{name?, color?}`** → `name` omitted = the `default` icon; `color`
    omitted = **follows the foreground** for that state.

  ```python
  icon_element(style, "MyStyle.indicator", size=20,
      default="check-square-fill",              # name; color follows foreground
      states={
          "selected": {"color": "primary"},     # default icon, recolored to accent
          "!selected": "square",                # name; follows foreground
          "disabled":  {"color": "#888"},       # default icon, dimmed
      })
  ```

  **"Follows the foreground" is resolved at build time** via
  `style.lookup(ttkstyle, "foreground", state=…)` — image elements are baked
  bitmaps, not live text, so an omitted color is materialized per state from the
  style's already-configured `foreground` map (call `icon_element` *after* the
  `state_map(..., foreground=…)` / `_build_configure`). `color` accepts a
  **bootstyle keyword or a hex** (resolved once against the active theme; no
  auto-follow on theme switch — that's the engine's repaint job, not the spec's).

**Scope boundary (why this is in-scope):** ttk's own statespec mechanism is the
state engine; `icon_element` feeds it per-state images — a pure styling concern. A
Python-side stateful `Icon` that re-renders on widget *events* (bootstack's
theme-following model) is widget-framework territory and stays **out** of 2.0.
"Map an icon per state" therefore maps onto ttk's element state map, not a runtime
object. Keep `icon_element` thin: render + validate + `element_create`, no state
of its own beyond `Style._image_cache`.

**We adopt ttkbootstrap-icons' spec *grammar* but deliberately drop its
*delivery*.** `StatefulIconMixin.map()` builds a **per-widget child style**, keeps
a `_widget_mappings` weakref registry, binds `<<ThemeChanged>>`, and re-renders
every mapped icon on theme switch. That is widget-instance stateful behavior — and
it is exactly the registry-plus-event machinery the 2.0 engine rewrite removed
(version-stamped repaint, no `Publisher`). `icon_element` instead builds the image
state-map on a **named style once**; the engine's theme walk repaints. Same
grammar, no second theme-follow path competing with the engine.

Lives in `style/icons.py` (or `layout.py` beside `image_element` — pick at impl
time for the cleanest import layering; it needs both `Assets.icon` and
`statespec`). Re-export from `style/__init__.py` + top-level `ttkbootstrap`.

## Visual language — LOCKED: flat / single-glyph

The user chose the **flat, single-glyph** aesthetic for the check/radio/switch
indicators (a deliberate modern refresh from today's two-tone filled look). One
glyph per state, rendered in the state color; where a glyph has an interior mark
(`-fill` variants, `record-circle`), the mark is a **transparent knockout** that
shows the widget background through it — which makes it automatically
theme-adaptive (primary square + light-bg check on light themes; primary square +
dark-bg check on dark themes). No two-glyph compositing.

### Per-family glyph + color map

Colors reference the existing builders' state-color math (kept as-is — the icon
swap changes *how the mark is drawn*, not *which color a state is*). `fg-muted` =
the existing `Colors.make_transparent(0.4, fg, bg)` border tone; `disabled` =
`make_transparent(0.3, fg, bg)`; `accent` = `colors.get(colorname)` (PRIMARY when
default).

| widget | state | glyph | color |
|---|---|---|---|
| **checkbutton** | off (`!selected`) | `square` | `fg-muted` |
| | on (`selected`) | `check-square-fill` | `accent` |
| | indeterminate (`alternate`) | `dash-square-fill` | `accent` |
| | disabled off | `square` | `disabled` |
| | disabled on | `check-square-fill` | `disabled` |
| | disabled alt | `dash-square-fill` | `disabled` |
| **radiobutton** | off (`!selected`) | `circle` | `fg-muted` |
| | on (`selected`) | `record-circle-fill` | `accent` |
| | disabled off | `circle` | `disabled` |
| | disabled on | `record-circle-fill` | `disabled` |
| **switch (round/square toggle)** | off (`!selected`) | `toggle-off` | `fg-muted` |
| | on (`selected`) | `toggle-on` | `accent` |
| | disabled off | `toggle-off` | `disabled` |
| | disabled on | `toggle-on` | `disabled` |

Notes:
- **Switch look — RESOLVED: one look.** Both `round-toggle` and `square-toggle`
  render `toggle-on`/`toggle-off`; `square-toggle` becomes a visual alias of
  round (Bootstrap's toggle is rounded). The two bootstyle keywords still resolve
  (back-compat) but produce the same indicator.
- **`LIGHT`-on-light edge case:** the current radio/check builders special-case
  `colorname == LIGHT and is_light_theme` (outline instead of filled, so a light
  mark is visible on a light bg). With the flat/knockout approach this mostly
  dissolves — but verify the `LIGHT` accent still reads; if not, fall back to the
  outline glyph (`check-square`/`circle`) for that one case.

### Other glyph-shaped assets (not check/radio/switch)

| builder | today | → icon |
|---|---|---|
| `create_date_button_assets` | hand-drawn calendar | `calendar` (or `calendar-event`) in `foreground` |
| `create_simple_arrow_assets` (combobox/spinbox) | 4 hand-drawn triangles | `chevron-down/up/left/right` (or `caret-*-fill`) |
| `create_sizegrip_assets` | hand-drawn dot grid | `grip-horizontal` / a corner grip glyph |

**Arrows — RESOLVED: chevron.** Use `chevron-down/up/left/right` — lighter,
modern open-arrow weight that matches the flat indicator aesthetic (over the
solid `caret-*-fill` triangles).

## What stays geometric (recipes, unchanged)

Not glyphs — keep the PR 5 recipes:
- **Tracks / troughs:** scale track, scrollbar trough, progressbar trough & bar
  → `rect` / `rounded_rect` (stretched; no glyph).
- **Progressbar stripes** → `image()` escape hatch (a fill pattern, no glyph).
- **Plain filled circles:** scale thumb → `circle` (trivially crisp, fully
  parametric by size/color; an icon adds nothing).
- **Plain pills:** round scrollbar thumb → `rounded_rect`.

## Acceptance proof (mirrors the toolkit doc's discipline)

With `icon_element`, `create_checkbutton_assets` **disappears entirely** — its
six hand-drawn composite draws (rounded body + glyph + `font_offset` fudge +
`font_variant` rescale) fold into one declarative state→icon map inside the style
method:

```python
def create_checkbutton_style(self, colorname=DEFAULT):
    sn = StyleName("TCheckbutton", colorname)
    size = self.scale_size(20)
    disabled = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)

    # foreground map FIRST, so icon specs that omit a color resolve against it
    self.style._build_configure(sn.ttkstyle, foreground=self.colors.fg)
    state_map(self.style, sn.ttkstyle, foreground={"disabled": disabled})

    icon_element(self.style, f"{sn.element}.indicator", size=size,
        default={"name": "check-square-fill", "color": sn.colorname},  # selected → accent
        states={
            "disabled selected":  "check-square-fill",   # name only → color follows fg(disabled)
            "disabled alternate": "dash-square-fill",     #   (free dimming — no color repeated)
            "disabled":           "square",
            "alternate":          {"name": "dash-square-fill", "color": sn.colorname},
            "!selected":          "square",               # off → color follows foreground
        },
        border=self.scale_size(4), sticky=W)
    layout(self.style, sn.ttkstyle, El("Checkbutton.padding", sticky=NSEW, children=[
        El(f"{sn.element}.indicator", side=LEFT, sticky=""),
        El("Checkbutton.focus", side=LEFT, sticky="", children=[
            El("Checkbutton.label", sticky=NSEW)])]))
    self.style._register_ttkstyle(sn.ttkstyle)
```

The disabled states just **name** the glyph — their color follows the
`foreground` map's `disabled` entry for free, no color repeated. No `Image.new`,
`getbbox`, `font_offset`, `font_variant`, or per-state closure anywhere — and the
separate assets method is gone. The `layout`/`El` +
`state_map` plumbing is the **unchanged** PR-5/PR-6 toolkit; icons + `icon_element`
swap the *asset source and its state wiring*. (`create_radiobutton_*` and the two
toggle builders collapse the same way; the arrow/calendar/sizegrip builders use a
plain `a.icon` since they have no state map.)

## Layering / import safety / gotchas

- `style/icons.py` is a leaf (PIL + stdlib only); `Assets.icon` lives in the
  existing `assets.py`. Run the **standalone-import cycle guard** and the
  **PEP 649 annotation force-evaluation sweep** (3.14) over `icons.py` + the
  migrated builders, per the split/toolkit docs.
- Asset path resolution: `Path(__file__).parent.parent / "assets" / "icons"`.
  Confirm it works from an installed wheel (package-data), not just the src tree.
- `import ttkbootstrap` must stay **warning-free** and must **not** load the font
  at import time — `IconRenderer` loads lazily on first `render`.
- Font load is from in-memory bytes (`ImageFont.truetype(io.BytesIO(...), size)`);
  cache `FreeTypeFont` per size like bootstack does.

## PR plan (PR 6 is HELD — these replace it)

1. **PR 6a — icon engine (no behavior change):** vendor the 3 assets + the
   regen tool + license; add `style/icons.py` (`IconRenderer`) and
   `Assets.icon`; public `Icon` if decision (1a); re-exports; tests (glyph
   renders; key completeness; even-snap; metrics-fit centering; color-in-key
   theme-independence; cycle guard; PEP 649 sweep; warning-free import).
   Touches **no** builders → suite stays green, nothing visually changes yet.
2. **PR 6b — migrate glyph builders + land the held geometric/layout cleanup:**
   check/radio/toggle×2/date/arrows/sizegrip onto `a.icon`; bring over PR 6's
   *geometric* recipe + `layout`/`El` + `image_element`/`state_map` migrations
   (separator, scrollbars, stripes, all 21 layout pyramids) that we want to keep.
   This is the visible change; gate on the visual spot-check below.

Splitting the engine from the migration keeps 6a fully test-netted and makes 6b
a focused, reviewable visual diff.

## Verification plan

- `python -m pytest -q` green after 6a (no builder change) and 6b.
- New `tests/widget_styles/test_icons.py`: a known glyph renders to a non-empty
  RGBA of the snapped even size; same `(name,size,color)` → same Tcl name;
  differing color → different name; a metrics-present glyph centers within
  tolerance; unknown glyph name fails loudly (validation).
- `test_image_cache.py` color-at-pixel assertions updated for the new keys; a
  theme round-trip still holds `_image_cache` flat.
- **The one headless gap (carried from PR 5):** a visual spot-check of
  check/radio/switch/combobox/spinbox/scale/date/sizegrip across a light↔dark
  theme round-trip — the suite asserts color-at-pixel, not appearance. This must
  be a human eyeball before 6b merges.

## PR 6a — IMPLEMENTED (icon engine, no builder change)

Landed on `feat/2.0-pr6a-icon-engine`; suite **89 passed** (was 75; +14 in
`tests/widget_styles/test_icons.py`). Engine only — no builders touched, nothing
visual in the library changed yet. Independently diff-reviewed (no leaks; cache /
leaf-layering invariants hold).

- **Vendored** `src/ttkbootstrap/assets/icons/` (`bootstrap.ttf` + `glyphmap.json`
  + `icon_metrics.json`) under MIT (LICENSE + README), the regen tool at
  `tools/generate_icon_metrics.py`, and `assets/icons/*` added to pyproject
  package-data (the `assets/*` glob does not recurse).
- **`style/icons.py`** (`IconRenderer` + `Icon` + `icon_element`): faithful port
  of bootstack's metrics fit-and-center, with ttkbootstrap-specific tuning below.
  Leaf module (PIL + stdlib + the two leaf toolkit modules; `Style` reached only
  function-locally). Unknown glyph **raises** (bootstack returns transparent).
- **`Assets.icon`** routes through `Style._get_or_create_image` with key
  `("icon", name, even-snapped size, resolved color)`. It takes an *already
  -resolved* color (like `circle`/`rect`); keyword resolution lives in
  `Icon`/`icon_element` (see the corrected composition example above).

### Render tuning — RESOLVED via the live visual spot-check (light↔dark)

The headless "one gap" spot-check was done on a Retina display, iterating on the
glyph crispness:

- **Supersample (icon-specific): 6× for <32 px, 3× for 32–63, 1× for ≥64** — richer
  than bootstack's 3/2/1 (and the geometric recipes', which are unchanged). The
  factor scales *inversely* with the size tier, so the supersampled canvas stays
  bounded (≤ ~186 px) and 6× costs the same as a 1× render of a 96 px icon
  (~0.15 ms warm; all images cache, so theme switches are free).
- **`UnsharpMask(0.5, 50, 0)` — gentle.** Curve smoothness comes from the
  supersample, *not* the sharpen; a hard sharpen (we tried 1.0/120) stair-stepped
  the thin rings. So: high supersample + light sharpen = smooth curves, defined
  straight strokes. (Tracked through 0.6/60 → 1.0/120 → 0.8/90 → **0.5/50 @ 6×**.)
- **Radio "on" → `record-circle-fill`** (updated in the table above), not the
  outline `record-circle`: it matches the `check-square-fill` knockout pattern and
  renders crisp (solid) instead of relying on a thin ring.

### Finding for PR 6b — the public custom-style path needs registration

A hand-built custom style applied to a ttkbootstrap widget via `style="X.TWidget"`
is **silently re-resolved as a bootstyle string** (→ base `TWidget`) unless the
style name was registered with `Style._register_ttkstyle(...)` —
`BootMixin.__init__` only honors `style=` when `style_exists_in_theme()` is True,
which keys on `_theme_styles` + `_style_registry` (both populated by
`_register_ttkstyle`). The real builders already call it; the design's public
mock #2 (`ttk.Checkbutton(app, style="Favorite.TCheckbutton")`) and the
`examples/icon_preview.py` demo did **not**, and silently fell back to the plain
indicator. **PR 6b / Tier-2 must give the public toolkit a non-private way to
register a hand-built style** (e.g. have the terminal `layout()` register the
style name, or add a public `register_style`), and the doc's mock #2 needs that
step. (`_register_ttkstyle` is private; users shouldn't need it.)

## Open decisions for sign-off
1. ~~Public surface~~ — **RESOLVED:** `Icon` atom + `icon_element` state-map sugar
   (see "Public surface" above).
2. ~~Switch look~~ — **RESOLVED:** one look (`toggle-on`/`toggle-off`).
3. ~~Arrows~~ — **RESOLVED:** chevron.
4. ~~API look-and-feel~~ — **RESOLVED:** `Icon` name; `color=` keyword-or-hex;
   per-state spec = bare-string(name) / dict `{name?, color?}` with omitted
   color following the foreground. See "Public surface" + "API feel".
5. (minor, defer to impl) calendar glyph: `calendar` vs `calendar-event`;
   sizegrip glyph choice.

Everything is locked except the two minor glyph picks (5), which can be settled
during PR 6b against the visual spot-check. **PR 6a is implemented (see the "PR 6a
— IMPLEMENTED" section); next is PR 6b.**

## API feel — mock usage (define before implementing)

These mocks exercise the **public** surface from a user's seat (not the internal
builders), to confirm it reads naturally before any code. The three ergonomic
levers are now **RESOLVED** (user, 2026-06-27) — shown inline below.

### 1. The atom — a single icon on a normal widget

```python
import ttkbootstrap as ttk

app = ttk.Window(themename="darkly")

# Icon(name, size=, color=) -> a Tk image usable directly as image=
gear = ttk.Icon("gear-fill", size=20, color="primary")
ttk.Button(app, text="Settings", image=gear, compound="left").pack()
```

**(a) RESOLVED — `color=` accepts a bootstyle keyword OR a hex.**
`color="primary"` resolves against the *active* theme at call time;
`color="#3498db"` passes through. Resolves **once** (no auto-follow on theme
switch — a re-render is the engine's job, or a new `Icon(...)` call). Auto
-following images are widget-framework scope (out of 2.0).

**(b) RESOLVED — class name is `Icon`** (cleaner at call sites than `IconImage`).

### 2. The state-map sugar — a custom widget style

```python
from ttkbootstrap.style import Style, icon_element, layout, El, state_map

style = Style.get_instance()

# A "favorite" checkbutton that shows a star instead of a check.
state_map(style, "Favorite.TCheckbutton", foreground={"disabled": "#888"})
icon_element(style, "Favorite.TCheckbutton.indicator", size=20,
    default={"name": "star-fill", "color": "warning"},  # selected → accent
    states={"!selected": "star"},                       # off → follows foreground
    border=4, sticky="w")
layout(style, "Favorite.TCheckbutton", El("Checkbutton.padding", sticky="nsew",
    children=[El("Favorite.TCheckbutton.indicator", side="left"),
              El("Checkbutton.focus", side="left",
                 children=[El("Checkbutton.label", sticky="nsew")])]))

ttk.Checkbutton(app, text="Favorite", style="Favorite.TCheckbutton").pack()
```

**(c) RESOLVED — per-state spec = bare string (name) or dict `{name?, color?}`.**
A bare string is the icon *name* (its color follows the foreground for that
state); a dict overrides `name` and/or `color`, each independently optional
(omitted `name` = the `default` icon, omitted `color` = follows foreground). See
the full grammar + rationale under "Public surface" above. Adapted from
ttkbootstrap-icons' `StatefulIconMixin` spec, minus its per-widget
theme-follow delivery.

### 3. Drop one icon into the existing toolkit (composition)

Icons compose with the PR-5 helpers — `a.icon` returns the same image-name
contract as `circle`/`rect`, so a hand-built `image_element` can mix them:

```python
from ttkbootstrap.style import Assets, image_element

a = Assets(style)
image_element(style, "MyStyle.indicator",
    default=a.icon("check-circle-fill", 20, "#28a745"),  # resolved hex
    states={"!selected": a.circle("#ccc", 20)})   # icon + geometric recipe, same call
```

`Assets.icon` takes an **already-resolved** color (a hex), exactly like the
sibling recipes `circle(fill, …)`/`rect(fill, …)` — the bootstyle-keyword
resolution lives one layer up, in the public `Icon`/`icon_element` (use
`Icon("check-circle-fill", 20, "success")` for the keyword form). This is the
proof that `icon_element` is *sugar*, not a silo: anything it does, you can also
assemble by hand from `a.icon` + `image_element`.

The surface ergonomics are now locked (a/b/c above) — implemented in PR 6a.
