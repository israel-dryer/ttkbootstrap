# Corner Radius Refactor

## Problem

ttkbootstrap uses PNG images for widget backgrounds (buttons, inputs, etc.) with rounded corners.
Because tkinter has no real transparency, rounded corners are faked: the image corners are filled
with the parent background color. This means any widget placed *inside* another widget (e.g. the
`-`/`+` spin buttons inside a `NumericEntry` field) clips the rounded corner area of the outer
widget, producing a visible rectangular cutout.

The current default-density assets use a **large corner radius** (border=16 at 2×, ~8px logical).
The compact-density assets use a **smaller corner radius** (border=14 at 2×, ~7px logical). The
smaller radius is tight enough that it is not visibly clipped.

## Solution

Re-export **all** default-density assets with the same smaller corner radius used by the compact
assets. This keeps the radii visually consistent across all widget sizes and densities and
eliminates the clipping problem without any code hacks.

No spacing workarounds or `button_height` overrides are needed — the new images will have the
correct natural sizes and the existing style builders will work as-is.

## Asset Exports Required

All images are exported from Figma at **2× resolution** (`default_dpi = 2.0` in manifest.toml).

### Target corner radius
Use the same radius as the existing compact assets: **border = 14 at 2×** for standalone
buttons/inputs, **border = 8 at 2×** for button-group segments.

### Button

| Manifest key        | Current file              | New file                  | Size (2×) | Border (2×) |
|---------------------|---------------------------|---------------------------|-----------|-------------|
| `button_default`    | `button-default.png`      | `button-default.png`      | 88×88     | 14          |

> The existing `button-default.png` (88×88, border=16) needs to be replaced with a new export
> at the same 88×88 size but with the smaller radius.

### Button Group — Default density (6 files)

| Manifest key                              | Current file                                   | Size (2×) | Border (2×) |
|-------------------------------------------|------------------------------------------------|-----------|-------------|
| `button_group_horizontal_before_default`  | `button-group-horizontal-before-default.png`   | 72×72     | 10          |
| `button_group_horizontal_center_default`  | `button-group-horizontal-center-default.png`   | 72×72     | 8,10,10,10  |
| `button_group_horizontal_after_default`   | `button-group-horizontal-after-default.png`    | 72×72     | 8,10,10,10  |
| `button_group_vertical_before_default`    | `button-group-vertical-before-default.png`     | 72×72     | 10          |
| `button_group_vertical_center_default`    | `button-group-vertical-center-default.png`     | 72×72     | 10,8,10,10  |
| `button_group_vertical_after_default`     | `button-group-vertical-after-default.png`      | 72×72     | 10,8,10,10  |

> Re-export each with the smaller radius matching the compact variants.
> Keep the 72×72 size so default buttons remain taller than compact.

### Input (Entry / Combobox / Spinbox)

| Manifest key     | Current file         | New file             | Size (2×) | Border (2×) |
|------------------|----------------------|----------------------|-----------|-------------|
| `input_default`  | `input-default.png`  | `input-default.png`  | 88×88     | 14          |

> Same approach as `button_default` — same size, smaller radius.
> `input_after_default` and `input_before_default` are flat rectangles (no rounded corners),
> so they do **not** need to be updated.

### Navigation buttons

The `nav_button_default` and `nav_icon_button_default` assets use a different proportional
indicator bar for each density, so they are intentionally kept as separate files.
These are **not** part of this refactor; update separately if needed.

## Manifest Changes (after new assets are ready)

Only the `border` values need updating in `manifest.toml` — the file names and sizes stay the same.

```toml
[images.button_default]
file = "button-default.png"
width = 88
height = 88
border = 14        # was 16
padding = 0

[images.input_default]
file = "input-default.png"
width = 88
height = 88
border = 14        # was 16
padding = 0

# Button group default entries: change border from 10/[8,10,10,10] → 8
[images.button_group_horizontal_before_default]
border = 8         # was 10

[images.button_group_horizontal_center_default]
border = 8         # was [8, 10, 10, 10]

# ... and so on for all 6 button_group_*_default entries
```

## Code Changes (after manifest is updated)

No style-builder code changes are required. The existing builders read the image and its metadata
(including border) from the manifest at runtime. Updating the manifest is sufficient.

The only field.py spacing fix that **was** explored (unifying `field_padding` to 4 for both
densities) turned out to be unnecessary with properly-sized assets. Leave `field_padding` as-is.

## Branch

`refactor/consistent-corner-radius` (branched from `release/v2`)

## Current State

Branch is clean. Waiting for new Figma exports before making any code or manifest changes.