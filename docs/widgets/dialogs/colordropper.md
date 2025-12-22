---
title: ColorDropper
---

# ColorDropper

`ColorDropper` is a **screen color picker** that lets users sample a color from anywhere on the screen.

It’s useful for design tools, theme editors, and workflows where the desired color already exists in the UI.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

color = ttk.ColorDropper().show()
print("color:", color)  # hex / rgb / None

app.mainloop()
```

---

## Value model

A color dropper produces:

- the sampled color value (hex/rgb), or
- `None` if cancelled

---

## Behavior

Common interaction pattern:

- activating the dropper enters “pick mode”
- moving the cursor previews the sampled color (implementation-dependent)
- clicking commits the sample
- Escape cancels

---

## When should I use ColorDropper?

Use `ColorDropper` when:

- users need to match a color already on screen
- sampling is faster than choosing from palettes

Prefer **ColorChooser** when:

- users need to browse/select from a palette with previews

---

## Related widgets

- **ColorChooser** — palette-based color dialog
- **Dialog** — base dialog API

---

## Reference

- **API Reference:** `ttkbootstrap.ColorDropper`
