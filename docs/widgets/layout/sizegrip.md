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

## Quick start

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

## When to use

Use `Sizegrip` when:

- your UI includes a status bar/footer and you want an explicit resize affordance

- your users expect classic desktop window cues

- you want to provide a visual affordance for resizing

- you want to match platform expectations in desktop apps

**Consider a different control when:**

- your UI already makes resizing obvious (or resizing is disabled)

---

## Appearance

On many platforms, users can resize windows by dragging the window border even without a sizegrip, so this widget is mainly
a UX hint.

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

---

## Examples & patterns

`Sizegrip` typically doesn't require additional configuration. Layout is controlled by geometry manager options such as
`side=`, `anchor=`, `padx=`, and `pady=`.

---

## Behavior

- The sizegrip is not focusable and is not intended for keyboard interaction.

- Dragging the grip resizes the toplevel window in standard ttk implementations.

---

## Additional resources

### Related widgets

- [Frame](frame.md) -- common container for status bars/footers

- [PanedWindow](panedwindow.md) -- resizable split regions

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- **API Reference:** `ttkbootstrap.Sizegrip`