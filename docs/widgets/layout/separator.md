---
title: Separator
icon: fontawesome/solid/minus
---


# Separator

`Separator` is a thin visual divider that inherits ttkbootstrap’s theming so your layout lines (horizontal or vertical) keep the same colors as buttons, frames, and other primitives.

---

## Overview

Key capabilities:

- Wraps `ttk.Separator` so you can set `orient` (`horizontal` or `vertical`) without losing access to `bootstyle` or `surface_color`.
- Honors `style_options` for advanced styling tweaks such as `{"linecolor": "secondary"}` when you need subtle variations.
- Behaves like any ttk widget in grid/pack/place, letting you stretch, align, or inset separators between content blocks.
- Works well inside `Frame`, `LabelFrame`, `PanedWindow`, or toolbars to break up sections visually while staying on-theme.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

ttk.Label(app, text="Section A").pack(padx=16, pady=(16, 4))
ttk.Separator(app, bootstyle="secondary").pack(fill="x", padx=16)
ttk.Label(app, text="Section B").pack(padx=16, pady=(4, 16))

content = ttk.Frame(app)
content.pack(fill="both", expand=True, padx=16, pady=16)

ttk.Separator(content, orient="vertical", bootstyle="secondary").pack(side="left", fill="y", padx=(0, 12))
ttk.Label(content, text="Right side content").pack(side="left", expand=True)

app.mainloop()
```

---

## Styling and layout

- `bootstyle` controls the separator’s color tokens (`primary`, `muted`, `secondary` etc.).
- Use `surface_color` to adjust the background when placing separators over cards or pinned surfaces.
- `style_options` forwards tokens to the builder when you want even finer control (e.g., custom thickness or animation tokens provided by your theme).
- Because `Separator` is just a `ttk` widget, it participates in geometry managers (`grid`, `pack`, `place`) like any other control.

---

## When to use Separator

Use `Separator` to break up panels, align toolbars, or add breathing room between sections without resorting to extra padding. For multi-pane layouts, pair with `PanedWindow`; for cards, pair with `Frame` or `LabelFrame`.

If you need a more active divider or drag handle, consider `PanedWindow`; for purely decorative lines, a themed `Frame` with minimal height can also work.
