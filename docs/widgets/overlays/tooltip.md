---
title: Tooltip
---

# Tooltip

`Tooltip` is a **contextual overlay** that appears on hover (or focus) to provide brief help or explanations.

Use tooltips for:

- icon-only buttons
- dense toolbars
- exposing extra detail without cluttering the UI

Tooltips should be short, readable, and optional.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

btn = ttk.Button(app, text="Refresh")
btn.pack(padx=20, pady=20)

ttk.Tooltip(btn, text="Reload the current view")
app.mainloop()
```

---

## Behavior

- Appears on hover (and optionally focus)
- Disappears on leave or after a delay
- Should not steal focus or block interaction

---

## Common options

- `text`
- `delay` (time before showing)
- `wraplength` (max line width)
- `bootstyle` (if supported)

---

## When should I use Tooltip?

Use Tooltip when:

- the control meaning isn’t obvious (especially icon-only UI)
- you want “learnable” UI without permanent labels

Avoid tooltips when:

- the text is essential to completing the task (use labels or inline help)

---

## Related widgets

- **Toast** — non-blocking notifications
- **MessageBox** — blocking alerts and confirmations

---

## Reference

- **API Reference:** `ttkbootstrap.Tooltip`
