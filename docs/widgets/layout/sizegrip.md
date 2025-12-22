---
title: Sizegrip
---

# Sizegrip

`Sizegrip` is a small **resize handle** that indicates a window (or pane) can be resized.

It wraps `ttk.Sizegrip` and is typically placed in the bottom-right corner of a resizable window, status bar, or footer.

<!--
IMAGE: Sizegrip in a status bar (bottom-right)
Theme variants: light / dark
-->

---

## Overview

Use `Sizegrip` to:

- provide a visual affordance for resizing
- match platform expectations in desktop apps

On many platforms, users can resize windows by dragging the window border even without a sizegrip, so this widget is mainly
a UX hint.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

content = ttk.Frame(app, padding=20)
content.pack(fill="both", expand=True)

status = ttk.Frame(app, padding=(8, 4))
status.pack(fill="x", side="bottom")

grip = ttk.Sizegrip(status)
grip.pack(side="right")

app.mainloop()
```

---

## Common options

`Sizegrip` typically doesn’t require additional configuration. Layout is controlled by geometry manager options such as
`side=`, `anchor=`, `padx=`, and `pady=`.

---

## Behavior

- The sizegrip is not focusable and is not intended for keyboard interaction.
- Dragging the grip resizes the toplevel window in standard ttk implementations.

---

## When should I use Sizegrip?

Use `Sizegrip` when:

- your UI includes a status bar/footer and you want an explicit resize affordance
- your users expect classic desktop window cues

Skip it when:

- your UI already makes resizing obvious (or resizing is disabled)

---

## Related widgets

- **Frame** — common container for status bars/footers
- **PanedWindow** — resizable split regions

---

## Reference

- **API Reference:** `ttkbootstrap.Sizegrip`
