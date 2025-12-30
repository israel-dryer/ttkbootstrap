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

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

btn = ttk.Button(app, text="Refresh")
btn.pack(padx=20, pady=20)

ttk.Tooltip(btn, text="Reload the current view")
app.mainloop()
```

---

## When to use

Use Tooltip when:

- the control meaning isn't obvious (especially icon-only UI)

- you want "learnable" UI without permanent labels

### Consider a different control when...

- the text is essential to completing the task — use labels or inline help

- you need to show notifications or feedback — use [Toast](./toast.md)

---

## Appearance

### Variants

Tooltips can be styled using the `color` parameter (if supported).

!!! link "Design System"
    See the [Colors & Styling](../../design-system/colors.md) guide for complete color options.

---

## Examples & patterns

### Common options

- `text` — the tooltip content

- `delay` — time before showing (in milliseconds)

- `wraplength` — max line width for text wrapping

- `color` — visual style (if supported)

---

## Behavior

- Appears on hover (and optionally focus)

- Disappears on leave or after a delay

- Should not steal focus or block interaction

---

## Additional resources

### Related widgets

- [Toast](./toast.md) — non-blocking notifications

- [MessageBox](../dialogs/messagebox.md) — blocking alerts and confirmations

### Framework concepts

- [Overlays](./index.md) — overview of overlay widgets

### API reference

- [`ttkbootstrap.Tooltip`](../../reference/widgets/Tooltip.md)