---
title: FontDialog
---

# FontDialog

`FontDialog` is a **modal font picker** that lets users choose a font family, size, and style, then confirm or cancel.

Use it for editor-like features (rich text, labels, code editors) where users need a standard font selection experience.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FontDialog(title="Choose a font")
result = dlg.show()

print("font:", result)  # font string/object or None
app.mainloop()
```

---

## Value model

Font dialogs typically return:

- a committed font spec (string, tuple, or object), or
- `None` when cancelled

---

## Common options

- `title`
- `initial_font` (if supported)
- preview sample text (if supported)

---

## Behavior

- OK commits the selected font
- Cancel closes without committing
- Enter confirms, Escape cancels (typical)

---

## When should I use FontDialog?

Use `FontDialog` when:

- font choice is part of a user customization workflow
- you want a standard modal picker

Prefer inline font controls when:

- font selection is a frequent, always-visible control (toolbars)

---

## Related widgets

- **Dialog** — base dialog API
- **FormDialog** — structured multi-field input
- **MessageBox** — confirmations/alerts

---

## Reference

- **API Reference:** `ttkbootstrap.FontDialog`
