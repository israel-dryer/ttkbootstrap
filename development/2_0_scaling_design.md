# ttkbootstrap 2.0 — Scaling and asset-geometry normalization

**Status:** implemented and visually approved on 2026-06-29
**Branch:** `refactor/2.0-scaling`, from `2.0` at `fa1cede8`
**Draft PR:** #1083 against `2.0`
**Date:** 2026-06-29

## Decision summary

Replace the current scaling formulas with one root-bound service. Every
measurement has an explicit unit and crosses a unit boundary once:

1. Builder and public size inputs are **logical UI units** at baseline density.
2. Tk-facing geometry and final image dimensions are **physical pixels**.
3. Raster-template dimensions are **source-image pixels** and never imply UI
   size by themselves.

Logical units convert to physical pixels with round-half-up. Manifest assets
carry an explicit logical target size instead of deriving widget geometry from
source density. Final image dimensions are not forced even: pixel-grid snapping
is a rendering concern and must not enlarge ttk layout geometry.

The scale thumb changed from 14 logical pixels immediately before #1081 to
22px at 100%. Visual review confirmed that 22px is the correct logical baseline;
the smaller 14px thumb is not being restored. For the other manifest-backed
widgets, the recommended baseline is the geometry shipped in and visually
approved with #1081. Historical procedural dimensions remain audit evidence,
not an implicit reason to revert approved raster geometry.

## Scope and invariants

In scope:

- platform baselines and root DPI-factor detection;
- `utility.scale_size()` and `StyleBuilderTTK.scale_size()`;
- one service used by builders, `Assets`, icons, and recolored rasters;
- procedural asset dimensions, radii, strokes, and render-grid alignment;
- manifest source size, logical size, border, and padding semantics;
- Window DPI initialization order;
- hard-coded geometry in ttk and legacy-tk style builders;
- automated and human checks at 100%, 125%, 150%, and 200%.

Out of scope:

- color ramps and builder state-color helpers;
- bootstyle grammar changes;
- live per-monitor rescaling after a window moves between displays;
- a new public DPI-management API;
- font-system redesign, window-geometry semantics, or application widget
  padding outside the style builders;
- color, state, element-name, layout, or generated-style-name changes.

Implementation must preserve public names and call signatures, generated ttk
style names, lazy per-theme construction, cache purity, and warning-free
imports. Visual changes are limited to geometry corrections approved from this
design.

## Current-state findings

### Independent and inconsistent formulas

- `utility.scale_size(widget, size)` divides Tk scaling by a fixed non-macOS
  baseline and truncates with `int`.
- `StyleBuilderTTK.scale_size(size)` selects an Aqua/non-Aqua baseline and
  uses `ceil`.
- `Assets.recolor()` repeats baseline selection, divides by manifest
  `default_dpi`, rounds half up, and then forces width and height even.

The same logical value can therefore round down, round up, or round up again to
an even number depending on its consumer.

### Procedural assets and icons

`Assets.circle`, `rounded_rect`, `image`, and `icon` currently require
already-scaled final pixels, then force each dimension to the next even integer.
`rect` does not. Public `Icon()` does not scale its default or user size,
while internal builders pre-scale before `Assets.icon`. This contract makes
missed and double scaling easy.

### Recolored rasters

The manifest records source width/height and a global 2x density. The renderer
infers logical size from source pixels. That relationship must be explicit,
not assumed. For the slider, visual review confirmed that the 44px source is
a 2x source for a 22px logical thumb.

Border and padding are also recorded as source pixels and rounded separately.
Image dimensions are even-snapped while metadata is not, so they do not share
one geometry policy.

### Window initialization

`Window` enables Windows DPI awareness before constructing `Tk`, applies an
explicit `scaling=` value after root creation, and constructs `Style` last.
That order is correct. The missing part is one root-bound object reused by all
later scaling consumers.

### Bootstack lessons

Useful mechanisms to port:

- 96-DPI Windows/Linux and 72-DPI macOS baselines;
- separate UI and source-image scale concepts;
- logical and source-measurement helpers;
- DPI-scaled icons;
- adaptive supersampling, render-origin alignment, LANCZOS, and sharpening.

Do not port bootstack's process-global `_ScalingState`. ttkbootstrap is tied to
one Tk root, so scale belongs to that root/interpreter. Bootstack also mixes
truncation, round, early source rounding, and layout-affecting even snaps; those
parts should be normalized rather than copied.

## Unit model

### Logical UI units (`lu`)

Theme-authored dimensions at baseline density: padding, borders, indicators,
progressbar thickness, icon frames, radii, and ttk layout spacing. At 100%,
`1 lu = 1 px`. Logical units are not Tk points; font point sizes remain under
Tk's font scaling.

### Physical pixels (`px`)

Integer dimensions passed to Pillow, `PhotoImage`, ttk image elements, canvas
coordinates, and pixel-valued style options. A value already in physical pixels
must never pass through `scale_size` again.

Font metrics such as `linespace` are already physical. Screen coordinates and
the current public `Window(size=...)` contract are also physical/window-manager
coordinates and remain unchanged.

### Source-image pixels (`spx`)

Coordinates in a vendored PNG. They validate and address the bitmap but do not
define widget size. A manifest gives each asset a separate logical target size.
Any retained source border measurement must be labeled and converted without an
intermediate 1x rounding.

## Root-bound scaling service

Add a private leaf module, proposed as `style/scaling.py`, with no engine
import. `Style` creates or reuses the service after `ttk.Style.__init__`
establishes `master` and before the first theme builder runs.

Conceptual interface:

```python
class Scaling:
    root
    windowing_system
    baseline
    tk_scaling
    factor

    def logical(self, value): ...
    def source(self, value, *, source_scale): ...
    def image_size(self, logical_size): ...
    def render_origin(self, value, *, oversample): ...
```

The exact class name stays private. One instance is attached to the root so
`Style`, both style builders, `Assets`, icons, recoloring, and the public
utility observe the same scale. There is no global mutable scale.

`StyleBuilderTTK.scale_size()` remains as a convenience delegate.
`utility.scale_size(widget, size)` keeps its public two-argument signature and
delegates through the widget's root. Existing result shapes remain: scalar to
integer and tuple/list to list.

`Assets(style)` takes the service from `style`; it never redetects a
baseline. Cache keys continue to contain final physical dimensions, so equal
pixels deduplicate across themes.

The service reads current Tk scaling when converting rather than keeping an
independent value. `Window(scaling=...)` still sets Tk before `Style` exists.
Changing Tk scaling after styles are built remains unsupported because existing
ttk styles are not rebuilt; document that callers must set it before style
construction rather than adding live DPI rebuilding here.

## Baselines, detection, and rounding

### Baselines

- `win32` and `x11`: 96 DPI / 72 points = `4/3` pixels per point.
- `aqua`: 72 DPI / 72 points = `1.0`; Retina backing scale is not multiplied
  into Tk layout geometry.

Select by Tk's windowing system, not Python's OS name.

### Detection and initialization

1. On Windows, keep the pre-root best-effort system-DPI-awareness behavior.
   Prefer `SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)` when available,
   then fall back to `SetProcessDPIAware`, without raising if awareness was
   already fixed by the host process. Do not opt into per-monitor-v2 behavior
   in this workstream because live per-monitor rescaling is explicitly out of
   scope.
2. After root creation, `tk scaling` is authoritative. If unavailable, use
   `winfo_fpixels(1i) / 72`.
3. Explicit `Window(scaling=x)` remains a Tk pixels-per-point override and is
   applied before the service binds.
4. Linux and macOS retain the value configured by Tk/environment. Do not replace
   it with a device-global Windows percentage.

This avoids bootstack's process-global `GetScaleFactorForDevice(0)` assumption.
Live per-monitor changes remain out of scope.

### Factor normalization

Tk often reports nominal values with small error, such as `1.333989...`
instead of `4/3`. Compute `raw = tk_scaling / baseline`; if it is within
`0.005` of a quarter-step, normalize to that step. Otherwise retain the raw
factor. This makes 100/125/150/200% deterministic without rejecting custom
factors.

### Rounding

Positive logical geometry uses round-half-up at the final boundary:

```text
px = max(minimum, floor(lu * factor + 0.5))
```

Do not use banker rounding, truncation, or unconditional `ceil`. Zero stays
zero. Positive border/padding components can request a one-pixel minimum.
Negative values, where allowed, round symmetrically away from zero at the half.

Source conversion retains fractional precision until its final boundary:

```text
px = floor((spx / source_scale) * factor + 0.5)
```

Never round `spx / source_scale` first.

## Rendering and even snapping

**Proposed decision: even snapping must not affect layout geometry.** A requested
15px image remains 15px, not 16px. `PhotoImage` dimensions determine ttk
requested geometry and direct-widget image geometry, so changing the final
canvas is not a rendering-only detail.

Remove the current odd-to-next-even output rule from procedural assets, icons,
and recolored rasters. Keep:

- adaptive supersampling;
- draw-origin alignment to final-pixel boundaries in the oversampled canvas;
- parity-aware centering inside the exact final frame;
- LANCZOS downscale and existing tuned sharpening.

Internal canvas coordinates may snap; final physical width/height may be odd.
Cache keys use the exact final dimensions. Tests explicitly prove odd intended
dimensions remain odd.

The coordinate contract is explicit: logical frame geometry converts to final
physical pixels first; an oversampled canvas then multiplies those dimensions
by the oversample factor. A final-pixel edge at coordinate `p` is therefore
`p * oversample` in draw-callback space. A helper that receives an already
oversampled coordinate may round it to the nearest multiple of `oversample`.
It must not round or enlarge the final image frame. This avoids the ambiguous
phrase `snap the origin`, which otherwise permits opposite implementations.

## Asset-geometry audit and approval table

These are frame/layout dimensions at nominal 100%, not necessarily visible ink:

| Asset | Immediately before #1081 | Current result | Finding / proposal |
|---|---:|---:|---|
| Checkbox | 20×20 | 18×18 | **Recommend 18×18**: retain the #1081 raster frame that passed visual review. |
| Radio | 20×20 | 18×18 | **Recommend 18×18**: retain the #1081 annulus that passed visual review. |
| Round/square switch | 32×20 image, 36 element width | 38×18 | **Recommend 38×18**: retain the approved raster frame; the old separate element width is not part of the new asset contract. |
| Scale thumb | 14×14 | 22×22 | Visual review approved **22×22** as the correct baseline. |
| Scale track | 40×5 | 12×6 inferred frame | Visual review approved **6 logical pixels** of cross-axis thickness; 12px is the repeat-tile length. |
| Standard progressbar | 10 thickness | 8 thickness | **Recommend 8**: retain the #1081 raster thickness that passed the corrected stretch/surface review. |
| Thin progressbar | did not exist | 4 thickness | New approved style; retain 4 unless review says otherwise. |
| Striped progressbar | 12 thickness | 12, then fractional-scale even snap | Baseline preserved; remove output even snap. |
| Scrollbar thumb | 28×9 | 18×8 | **Recommend 18×8**: #1081 intentionally changed to an arrowless thumb/native-trough contract and passed visual review; the old arrow-bearing geometry is not its baseline. |

This recommendation treats #1081's human light↔dark gate as approval of the
nominal geometry actually shown, including the follow-up progressbar and
scrollbar corrections. A new side-by-side gate is warranted only if that prior
approval did not cover size, or if the four-scale review exposes a concrete
alignment or hit-area problem. It is safer than silently restoring unrelated
dimensions from the superseded icon/procedural layouts.

The recolor design said scaled sizes would be preserved, but the manifest
inferred them from source pixels. Use a versioned manifest with separate units:

```json
{
  file: slider-handle.png,
  source_size: [44, 44],
  size: [22, 22],
  border: 0,
  padding: 0
}
```

`source_size` is `spx` and validates the file. `size`, `border`, and
`padding` are `lu`. Source scale may remain as provenance but no longer
determines widget geometry. Transforms rotate logical geometry and metadata with
the pixels.

The approved scale baseline is a 22px thumb and 6px track thickness. Historical
geometry remains useful for regression analysis, but does not override the
visually approved baseline.

## Assets, icons, and public contracts

To enforce “scale exactly once,” size-bearing toolkit calls should accept
logical units and let their bound service convert:

- `Assets.circle`, `rect`, `rounded_rect`, `image`, and `icon`;
- public `Icon` and `icon_element`;
- `Assets.recolor` through logical manifest metadata.

Names, signatures, return types, and cache behavior do not change. This corrects
the unit semantics of APIs introduced on the unreleased 2.0 branch. Internal
builders stop pre-scaling before these calls. Documentation says to pass logical
sizes directly and use `utility.scale_size` only when an external Tk/Pillow API
needs physical pixels.

`IconRenderer.render()` remains the low-level raster leaf and continues to take
an exact physical-pixel frame. Public `Icon()` and `Assets.icon()` perform the
single logical-to-physical conversion before calling it. Keeping this boundary
physical prevents the renderer from depending on a Tk root and preserves its
standalone import/test role.

For `icon_element()`, numeric `border`, `padding`, `width`, and `height` options
are logical units and cross the same boundary once. The lower-level generic
`image_element()` continues to accept final Tk geometry because manifest-backed
callers pass its already-scaled metadata directly.

Procedural radius, width, and similar geometry are logical too. Custom
`Assets.image` callbacks still draw on their supplied supersampled physical
canvas; that boundary is explicitly rendering-space.

The alternative is to preserve the current “already physical” toolkit size
contract and pre-scale at every caller. It is source compatible but cannot
prevent missed/double scaling. The logical-input contract is recommended and
requires explicit approval because it corrects current 2.0 documentation.

## Builder geometry audit

Classify each measurement:

- **Scale once:** ttk padding, arrow padding/size, sash thickness, progressbar
  and floodgauge thickness, row padding, element dimensions, border/focus width,
  insertion-cursor width, and logical spacers.
- **Already physical:** font metrics and metadata returned by the service.
- **Tk-scaled elsewhere:** font point sizes.
- **Rendering space:** Pillow draw-callback coordinates.
- **Not measurements:** zero, `sticky`, `expand`, `side`, and booleans.

Current literals include `(10, 5)`, `(6, 5)`, `5`, and `(2, 2)`
paddings; 1/2px border and focus widths; 50px floodgauge thickness; Treeview
padding; toolbutton arrow geometry; and legacy-tk highlight/insert widths.
Convert them from logical units through the coordinator/service. Keep named
constants near recipes when a number carries widget-specific intent.

Add a structural test that flags new numeric geometry options in builders unless
they pass through scaling, are zero, come from font metrics/manifest metadata,
or carry an explicit physical-pixel annotation.

## Required test matrix

| Nominal scale | Factor | 22 lu | 20 lu | 6 lu | 1 lu |
|---:|---:|---:|---:|---:|---:|
| 100% | 1.00 | 22 | 20 | 6 | 1 |
| 125% | 1.25 | 28 | 25 | 8 | 1 |
| 150% | 1.50 | 33 | 30 | 9 | 2 |
| 200% | 2.00 | 44 | 40 | 12 | 2 |

Automated tests:

1. Aqua/non-Aqua baseline selection and floating-noise normalization.
2. Scalar/tuple/list conversion, result shape, zero/minimum behavior, and
   half-up boundaries at all four factors.
3. Source conversion without intermediate rounding.
4. Procedural rect, anti-aliased shape, and custom-image dimensions; odd
   results remain odd.
5. Icon frame dimensions and cache keys at all factors.
6. Every manifest asset's image dimensions, rotations, border, and padding
   against the approved logical table.
7. Recolor cache dedupe and theme-switch no-stale behavior.
8. Representative builder geometry: button and field padding/border, sash,
   progressbar/floodgauge thickness, and a legacy-tk width.
9. `Window(scaling=...)` applies before the first lazy style/asset build; the
   public utility and builder observe the same service.
10. Warning-free import, standalone imports, Python 3.10 parse, and Python 3.14
    annotation force evaluation.

Tests continue to use the shared `root` fixture, restore `tk scaling`, and
avoid a second Window. Factor-independent arithmetic can use a fake Tk adapter;
root-bound integration cases use unique assets/style names so lazy state does
not leak between parameter cases.

Human gate on Windows at 100/125/150/200%, one light and one dark theme:

- scale thumb/track alignment and drag hit area;
- checkbox, radio, and switches beside normal text;
- standard/thin/striped progressbars;
- standard/round scrollbars and minimum thumb length;
- buttons, entries, combobox/spinbox arrows, Notebook tabs, Treeview rows,
  panedwindow sash, date icon, and sizegrip;
- light↔dark switching at each factor with no geometry jump.

Record the approved logical table in tests so replacing a source asset cannot
silently change widget size.

## Implemented sequence

1. Add the private service and delegate both existing scale helpers.
2. Bind it in `Style` and preserve Window initialization order.
3. Normalize `Assets` and icon units; remove final even-size snapping while
   retaining render-grid alignment.
4. Version the recolor manifest with explicit source/logical geometry and apply
   the approved table.
5. Migrate hard-coded ttk and legacy-tk builder geometry once; add the structural
   guard.
6. Run the full headless/structural gates, then the four-scale human gate.

No color-ramp/helper work belongs in this branch.

Automated implementation results: focused scaling/toolkit/icon/recolor suite
68 passed; expected full suite 177 tests; local Python 3.12 result 176 passed
with the existing Tcl `nl.msg` environment failure; excluding localization 171
passed. Warning-free import, 36 fresh-process style imports, Python 3.10 grammar
for 88 source/test files, and 226 forced annotation targets pass. Human
light↔dark inspection passed at 100%, 125%, 150%, and 200% on 2026-06-29.

## Approved decisions

Approved by the user on 2026-06-29:

1. Size-bearing 2.0 `Assets`/Icon APIs accept logical UI units;
   `IconRenderer.render()` remains a physical-pixel leaf.
2. Layout-facing images keep their exact final dimensions. Rendering uses the
   explicit oversampled grid alignment above, with no final even-size snap.
3. The logical baseline table is locked: checkbox/radio 18×18, switches 38×18,
   scale thumb 22×22 and track tile 12×6, standard/thin/striped progressbar
   thickness 8/4/12, and scrollbar thumb 18×8 at 100%.
