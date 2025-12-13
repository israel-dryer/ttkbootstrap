---
title: SizeGrip
icon: fontawesome/solid/up-right-and-down-left-from-center
---


# SizeGrip

`SizeGrip` provides the little drag handle usually placed in a window corner to let users resize the containing surface. The ttkbootstrap wrapper adds `bootstyle`/`surface_color` support so the indicator stays in sync with rest of the theme.

---

## Overview

Highlights:

- Wraps `ttk.Sizegrip` while exposing `bootstyle`, `surface_color`, and `style_options` tokens for consistent coloring.
- Honors `cursor`, `name`, and other native options so you can place it inside toolbars, status bars, or bottom-right corners.
- Since it inherits from `TTKWrapperBase`, it behaves like a regular widget in `pack`, `grid`, or `place`.

Typically used in resizable windows or panes to indicate drag handles while respecting your design system’s colors.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

container = ttk.Frame(app, padding=16)
container.pack(fill="both", expand=True)

ttk.SizeGrip(container, bootstyle="secondary").pack(side="right", anchor="se")

app.mainloop()
```

---

## Styling tips

- `bootstyle` controls the colors of the grip lines; choose `secondary`, `muted`, or more expressive tokens like `primary-soft` to keep it visible.
- Combine with `surface_color` when you place the grip over darker or lighter backgrounds.
- Use `style_options` if you need to forward extra builder tokens (e.g., custom thickness or animations).

---

## When to use SizeGrip

Add a SizeGrip to resizable dialogs, panes, or custom toplevel panels where you want to signal the edges are drag-resizable. For non-window layouts, prefer plain `Frame` borders or `PanedWindow`.
