---
title: ColorChooser
icon: fontawesome/solid/palette
---

# ColorChooser

`ColorChooser` is a comprehensive color selection widget with multiple selection modes (spectrum, themed swatches, standard palette) plus precise value inputs for **HSL**, **RGB**, and **Hex**. It includes a live preview and integrates with the screen **ColorDropper** when available.

<!--
IMAGE: ColorChooser overview
Suggested: ColorChooser with Advanced/Themed/Standard tabs visible, preview boxes (Current/New), and value inputs
Theme variants: light / dark
-->

---

## Basic usage

Embed `ColorChooser` directly in a window:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.colorchooser import ColorChooser

app = ttk.App()

chooser = ColorChooser(app, initial_color="#00FF00", padding=10)
chooser.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

Use the dialog wrapper (`ColorChooserDialog`) and read the result:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog

app = ttk.App()

dlg = ColorChooserDialog(master=app, title="color.chooser", initial_color="#3366FF")
dlg.show()

if dlg.result:
    print(dlg.result.hex)   # "#RRGGBB"
    print(dlg.result.rgb)   # (r, g, b)
    print(dlg.result.hsl)   # (h, s, l)

app.mainloop()
```

<!--
IMAGE: ColorChooserDialog modal
Suggested: Modal dialog showing ColorChooser with OK/Cancel and dropper icon in footer
-->

---

## What problem it solves

Many apps need both:

- **Browsing** colors (palette + theme tokens)
- **Precision** (exact hex/RGB/HSL values)

`ColorChooser` combines both workflows into a single, consistent UI:

- Spectrum-based picking (hue/saturation + luminance)
- Themed swatches derived from the current ttkbootstrap theme (`primary`, `secondary`, etc.)
- Standard palette with common colors and shades
- Editable numeric inputs (H/S/L and R/G/B) and a Hex entry
- Live “New” preview alongside the “Current” color

---

## Core concepts

### Tabs: Advanced, Themed, Standard

The chooser exposes three selection surfaces:

- **Advanced**: interactive spectrum for hue/saturation + luminance slider
- **Themed**: swatches from your current theme’s palette keys
- **Standard**: a fixed palette of common colors + shades

<!--
IMAGE: Tab behaviors
Suggested: Three screenshots (Advanced/Themed/Standard) showing different selection surfaces
-->

---

### Live preview: Current vs New

The preview area shows:

- **Current**: the initial color when the chooser opened
- **New**: the color you are actively selecting

Preview labels automatically choose a readable foreground color based on contrast.

---

### Value inputs stay in sync

The widget keeps all color models synchronized:

- editing **Hex** updates RGB and HSL
- editing **RGB** updates Hex and HSL
- editing **HSL** updates Hex and RGB

Inputs are applied on spinner increment/decrement or on **Enter** in the field.

!!! tip "Use Enter for Hex"
    The Hex entry commits on **Enter**. For RGB/HSL spinners, both **Enter** and the increment/decrement controls commit changes.

---

## Common options & patterns

### Choosing a good initial color

If you don’t pass `initial_color`, the chooser defaults to the theme’s background color. When you’re editing an existing setting, pass the current value:

```python
chooser = ColorChooser(app, initial_color=current_hex)
```

---

### Integrating theme colors

The “Themed” tab is built from your active theme palette keys:

- `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`

This makes it easy to pick brand-consistent colors without memorizing hex values.

<!--
IMAGE: Themed swatches
Suggested: Themed swatch grid with shades and a highlighted selection
-->

---

## ColorDropper integration

When used through `ColorChooserDialog`, a small dropper button appears in the footer (platform permitting). Clicking it opens `ColorDropperDialog` and feeds the selected screen color back into the chooser.

- Not shown on **macOS** (Tk “aqua”) due to screen-grab limitations.
- When a screen color is selected, the chooser updates its Hex value and syncs all models.

!!! note "Dropper availability"
    The dropper is available in the dialog footer on Windows/Linux, and intentionally hidden on macOS.

---

## Events

### Dialog result event

`ColorChooserDialog` emits `<<DialogResult>>` with:

```python
event.data = {"result": ColorChoice | None, "confirmed": bool}
```

Bind with helper methods:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog

app = ttk.App()

dlg = ColorChooserDialog(master=app)

def on_result(payload):
    print(payload)

funcid = dlg.on_dialog_result(on_result)
dlg.show()

# later
dlg.off_dialog_result(funcid)

app.mainloop()
```

!!! tip "Use QueryBox for one-liners"
    If you want a one-line API, use `QueryBox.get_color(...)`, which uses the same underlying chooser dialog.

---

## UX guidance

- Prefer the **Themed** tab for brand-consistent palettes.
- Prefer **Advanced** for precise selection when browsing by hue/luminance.
- Always show the selected color as **hex** somewhere in your UI so users can copy it.

!!! tip "Best of both worlds"
    A good workflow is: pick a base color in Advanced → fine-tune with numeric inputs → copy hex.

---

## When to use / when not to

**Use ColorChooser when:**

- Users may browse or fine-tune colors
- You want theme-aware palettes plus precision inputs
- You need hex/rgb/hsl output in one place

**Avoid ColorChooser when:**

- You only need a quick “sample from screen” (use `ColorDropper`)
- You need a tiny inline picker (use a compact color button/control)
- You need macOS screen sampling (dropper is not available)

---

## Related widgets

- **ColorDropper** — pick a color from any screen pixel
- **QueryBox.get_color(...)** — one-line color selection
- **Dialog** — the base dialog system used by `ColorChooserDialog`
- **Toast** — great for “Copied #RRGGBB” confirmation after selection
