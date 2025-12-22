---
title: ColorChooser
---

# ColorChooser

`ColorChooser` is a **color picker dialog** for selecting a color and returning the chosen value.

Use it when you want a standard “pick a color → OK/Cancel” flow for theming, drawing tools, labels, or settings.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

color = ttk.ColorChooser(
    title="Choose a color",
    initial="#3b82f6",
).show()

print("color:", color)  # hex / rgb / None
app.mainloop()
```

---

## Value model

Color chooser dialogs typically return:

- a committed color value (hex string or rgb tuple), or
- `None` when cancelled

---

## Common options

- `title`
- `initial` (starting color)
- `format` (hex/rgb) if supported

---

## Behavior

- OK commits the color
- Cancel closes without committing
- Enter confirms, Escape cancels (typical)

---

## When should I use ColorChooser?

Use `ColorChooser` when:

- users pick a color occasionally
- an explicit confirm/cancel flow is appropriate

Prefer **ColorDropper** when:

- users need to pick a color from the screen

Prefer inline color swatches when:

- users frequently change colors and need immediate feedback

---

## Related widgets

- **ColorDropper** — pick a color from the screen
- **Dialog** — base dialog API
- **MessageBox** — confirmations/alerts

---

## Reference

- **API Reference:** `ttkbootstrap.ColorChooser`
