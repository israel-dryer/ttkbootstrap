---
title: PanedWindow
icon: fontawesome/solid/columns
---


# PanedWindow

`PanedWindow` is a themed splitter container (horizontal or vertical) that lets you resize two or more subpanes while keeping bootstyle and surface tokens consistent with the rest of the app.

---

## Overview

Key behaviors:

- Wraps `ttk.Panedwindow` with `bootstyle`, `surface_color`, and `style_options` so the sash and background colors follow your theme.
- Honors regular options such as `orient`, `padding`, `width`, `height`, `cursor`, and `name`.
- Provides the same `add()`, `forget()`, and `paneconfig()` APIs as `ttk.Panedwindow` for managing the child panes and sash properties.
- You can also treat it as a normal `Frame` for geometry management (grid/pack/place) while it handles sash resizing between panes.

Use `PanedWindow` when you want resizable regions (file browsers, editors with sidebars, or dashboards with adjustable panels) that respect ttkbootstrap styling.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

paned = ttk.PanedWindow(app, orient="horizontal", bootstyle="secondary")
paned.pack(fill="both", expand=True, padx=16, pady=16)

left = ttk.Frame(paned, padding=16, bootstyle="white-space")
ttk.Label(left, text="Navigation").pack()
paned.add(left, weight=0)

right = ttk.Frame(paned, padding=16)
ttk.Label(right, text="Details").pack()
paned.add(right, weight=1)

app.mainloop()
```

---

## Sashes & styling

- `bootstyle` controls the sash fill and grab area colors; pair it with `surface_color` for the tracked background.
- `style_options` can feed extra builder tokens when you need bespoke treatments (e.g., `{"height": 300}` for thicker sash).
- Use `paneconfig()` to adjust `minsize`, `stretch`, or `pad` for each child pane after adding it.
- The widget respects theming events, so sash colors update automatically when the app theme changes.

---

## When to use PanedWindow

Pick `PanedWindow` when you need user-adjustable regions without reimplementing resizing logic. It bridges the gap between layout flexibility and themed aesthetics, especially for split view workflows.

Combine it with `Frame`, `LabelFrame`, or `Notebook` when each pane needs further structure.

---

## Related widgets

- `Frame` (panes' content holders)
- `Notebook` (tabbed panels)
- `LabelFrame` (grouped pane sections)
