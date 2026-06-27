# Vendored Bootstrap Icons

ttkbootstrap renders glyph-shaped widget assets (the checkbutton/radiobutton/
switch indicators, combobox/spinbox arrows, the date-entry button, the sizegrip)
from the **Bootstrap Icons** font, bundled here so there is **no extra pip
dependency**. The renderer is `ttkbootstrap.style.icons.IconRenderer`; the public
surface is `ttkbootstrap.Icon` (atom) and `ttkbootstrap.style.icon_element`
(per-state sugar).

## Contents

| file | what it is |
|---|---|
| `bootstrap.ttf` | the icon font — ~2078 named glyphs, internal font Version 1.0 |
| `glyphmap.json` | `name -> codepoint` (the *name* mapping) |
| `icon_metrics.json` | `name -> [left, top, width, height]` ink bbox in em-fractions (the *alignment* data) |
| `LICENSE` | the Bootstrap Icons MIT license |

`bootstrap.ttf` and `glyphmap.json` are the upstream Bootstrap Icons release
assets; `icon_metrics.json` is generated from them (see below).

## Provenance & license

- **Source:** Bootstrap Icons — https://icons.getbootstrap.com /
  https://github.com/twbs/icons
- **License:** MIT (see `LICENSE` in this directory). © The Bootstrap Authors.
- These files were vendored via the sibling **bootstack** project, which bundles
  the same Bootstrap Icons release. Only the font + the two JSON maps are
  vendored — no upstream code.

## Regenerating the metrics

`icon_metrics.json` records each glyph's true *inked* bounding box (Pillow's
`font.getbbox()` under-reports the ink for full-bleed icon glyphs, which skews
sizing/centering). The box is color-independent and scales linearly with the
font size, so it is measured once per glyph at a high reference size and stored
as em-fractions. Regenerate it whenever `bootstrap.ttf` / `glyphmap.json` are
updated:

    python tools/generate_icon_metrics.py
