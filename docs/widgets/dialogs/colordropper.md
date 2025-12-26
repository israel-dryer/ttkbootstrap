---
title: ColorDropper
---

# ColorDropper

`ColorDropper` is a **screen color picker** that lets users sample a color from anywhere on the screen.

It's useful for design tools, theme editors, and workflows where the desired color already exists in the UI.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

color = ttk.ColorDropper().show()
print("color:", color)  # hex / rgb / None

app.mainloop()
```

---

## When to use

Use `ColorDropper` when:

- users need to match a color already on screen

- sampling is faster than choosing from palettes

### Consider a different control when...

- users need to browse/select from a palette with previews - use [ColorChooser](colorchooser.md) instead

---

## Examples & patterns

### Value model

A color dropper produces:

- the sampled color value (hex/rgb), or

- `None` if cancelled

---

## Behavior

Common interaction pattern:

- activating the dropper enters "pick mode"

- moving the cursor previews the sampled color (implementation-dependent)

- clicking commits the sample

- Escape cancels

---

## Additional resources

### Related widgets

- [ColorChooser](colorchooser.md) - palette-based color dialog

- [Dialog](dialog.md) - base dialog API

### API reference

- [`ttkbootstrap.ColorDropper`](../../reference/dialogs/ColorDropper.md)