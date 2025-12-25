---
title: FontDialog
---

# FontDialog

`FontDialog` is a **modal font picker** that lets users choose a font family, size, and style, then confirm or cancel.

Use it for editor-like features (rich text, labels, code editors) where users need a standard font selection experience.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FontDialog(title="Choose a font")
result = dlg.show()

print("font:", result)  # font string/object or None
app.mainloop()
```

---

## When to use

Use `FontDialog` when:

- font choice is part of a user customization workflow

- you want a standard modal picker

### Consider a different control when...

- font selection is a frequent, always-visible control (toolbars) - use inline font controls instead

---

## Examples & patterns

### Common options

- `title` - dialog title

- `initial_font` (if supported)

- preview sample text (if supported)

### Value model

Font dialogs typically return:

- a committed font spec (string, tuple, or object), or

- `None` when cancelled

---

## Behavior

- OK commits the selected font

- Cancel closes without committing

- Enter confirms, Escape cancels (typical)

---

## Additional resources

### Related widgets

- [Dialog](dialog.md) - base dialog API

- [FormDialog](formdialog.md) - structured multi-field input

- [MessageBox](messagebox.md) - confirmations/alerts

### API reference

!!! link "API Reference"
    `ttkbootstrap.FontDialog`