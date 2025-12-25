---
title: ColorChooser
---

# ColorChooser

`ColorChooser` is a **color picker dialog** for selecting a color and returning the chosen value.

Use it when you want a standard "pick a color -> OK/Cancel" flow for theming, drawing tools, labels, or settings.

---

## Quick start

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

## When to use

Use `ColorChooser` when:

- users pick a color occasionally

- an explicit confirm/cancel flow is appropriate

### Consider a different control when...

- users need to pick a color from the screen - use [ColorDropper](colordropper.md) instead

- users frequently change colors and need immediate feedback - use inline color swatches instead

---

## Examples & patterns

### Common options

- `title` - dialog title

- `initial` - starting color

- `format` (hex/rgb) if supported

### Value model

Color chooser dialogs typically return:

- a committed color value (hex string or rgb tuple), or

- `None` when cancelled

---

## Behavior

- OK commits the color

- Cancel closes without committing

- Enter confirms, Escape cancels (typical)

---

## Additional resources

### Related widgets

- [ColorDropper](colordropper.md) - pick a color from the screen

- [Dialog](dialog.md) - base dialog API

- [MessageBox](messagebox.md) - confirmations/alerts

### API reference

!!! link "API Reference"
    `ttkbootstrap.ColorChooser`