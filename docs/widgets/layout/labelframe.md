---
title: LabelFrame
icon: fontawesome/solid/rectangle-list
---


# LabelFrame

`LabelFrame` is a themed group container that renders a title and border like `ttk.LabelFrame` but with bootstyle, surface color, and localization support for the embedded label.

---

## Overview

Key capabilities:

- Accepts `text`, `labelanchor`, `padding`, `relief`, `borderwidth`, `width`, and `height` just like native `ttk.LabelFrame`.
- Honors `bootstyle`, `surface_color`, and `style_options` so the frame slot matches your theme tokens.
- `localize="auto"` (or `True`) connects the label text to your localization catalog while still forcing defaults when needed.
- Works with grid/pack/place layouts the same way as `ttk.LabelFrame` but automatically synchronizes with ttkbootstrap colors.

Use `LabelFrame` when you need a titled fieldset or section that should stay consistent with your design system.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

frame = ttk.LabelFrame(app, text="User Info", padding=16, bootstyle="secondary")
frame.pack(fill="both", expand=True, padx=16, pady=16)

ttk.Label(frame, text="Name").grid(row=0, column=0, sticky="w")
ttk.Entry(frame).grid(row=0, column=1, sticky="ew")
ttk.Label(frame, text="Email").grid(row=1, column=0, sticky="w")
ttk.Entry(frame).grid(row=1, column=1, sticky="ew")

frame.columnconfigure(1, weight=1)

app.mainloop()
```

---

## Styling & localization

- `bootstyle` lets you select tonal treatments such as `primary`, `secondary-soft`, or `muted`.
- `surface_color` tweaks the background, while `style_options` passes extra builder tokens when you need them.
- `localize="auto"` uses the localization catalog when available; you can also pass `L("key")` or set `localize=False` for raw text.
- The `labelanchor` option controls whether the title sits on top, left, right, etc., and `padding` creates space within the frame.

---

## When to use LabelFrame

Prefer `LabelFrame` over `Frame` when the section benefits from a title or when you want semantic grouping in forms, dashboards, or settings panels. It still behaves like a frame in terms of geometry management.

Use `Frame` for bare containers or `Notebook`/`PanedWindow` when the layout needs tabs/splitters.

---

## Related widgets

- `Frame` (plain container)
- `Form` (grouped fields)
- `Label` (inline titles)
