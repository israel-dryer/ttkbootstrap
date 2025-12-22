---
title: Frame
---

# Frame

`Frame` is a **layout container** for grouping widgets and creating structure.

It’s a themed wrapper around `ttk.Frame`, so it participates in ttkbootstrap styling while behaving like a standard ttk
container. Use `Frame` to build sections, padded regions, tool areas, and compositional “blocks” in your UI.

<!--
IMAGE: Frame used for layout
Suggested: A simple form section inside a padded Frame (label + entry + button)
Theme variants: light / dark
-->

---

## Overview

A `Frame` is not interactive; it exists to:

- group related widgets
- apply padding/margins around a region
- host grid/pack layouts for a subsection of the UI
- apply a shared visual surface (when styled)

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

section = ttk.Frame(app, padding=20)
section.pack(fill="both", expand=True)

ttk.Label(section, text="Account").pack(anchor="w")
ttk.Entry(section).pack(fill="x", pady=(8, 0))

app.mainloop()
```

---

## Common options

### `padding`

Apply inner spacing to the container.

```python
ttk.Frame(app, padding=20)
ttk.Frame(app, padding=(16, 12))
```

### `width` / `height`

Useful for fixed regions (tool palettes, sidebars). Note: geometry managers may still size the frame
based on content unless propagation is disabled.

```python
pane = ttk.Frame(app, width=240, height=400)
pane.pack_propagate(False)
```

### `bootstyle` / `style`

Use `bootstyle` for semantic tokens, or `style=` for a concrete ttk style name.

```python
ttk.Frame(app, bootstyle="secondary")
ttk.Frame(app, style="Card.TFrame")
```

---

## Behavior

- Frames are **containers only** (no click/selection behavior).
- Use the frame as the parent for widgets you want visually/structurally grouped.
- Combine with `pack`, `grid`, or your v2 layout abstractions (e.g., `PackFrame`, `GridFrame`) to build structure.

---

## Styling

`Frame` is commonly used to create “surface” regions:

- card-like blocks
- sidebar backgrounds
- header/footer regions

If your theme supports bordered/card styles, prefer named styles like `Card.TFrame` for consistency.

---

## When should I use Frame?

Use `Frame` when:

- you need a container for grouping and layout
- you want padding around a cluster of widgets
- you want to apply a shared background/surface to a region

Prefer **LabelFrame** when:

- the group needs a visible label (a titled section)

---

## Related widgets

- **LabelFrame** — a framed container with a label
- **Separator** — a visual divider between regions
- **PanedWindow** — resizable split regions (if used in your UI)

---

## Reference

- **API Reference:** `ttkbootstrap.Frame`
