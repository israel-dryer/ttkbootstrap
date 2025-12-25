---
title: Frame
---

# Frame

`Frame` is a **basic layout container** for grouping widgets and creating structure.

It's a themed wrapper around `ttk.Frame`, so it participates in ttkbootstrap styling while behaving like a standard ttk container. Use `Frame` when you need a simple container without automatic layout management.

!!! tip "Prefer PackFrame or GridFrame for most layouts"
    For building layouts with automatic child management, use [PackFrame](packframe.md) (vertical/horizontal stacks with gap spacing) or [GridFrame](gridframe.md) (CSS Grid-like 2D layouts). These provide a more declarative, less error-prone layout experience.

<!--
IMAGE: Frame used for layout
Suggested: A simple form section inside a padded Frame (label + entry + button)
Theme variants: light / dark
-->

---

## Quick start

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

## When to use

Use `Frame` when:

- you need a basic container without automatic layout management
- you want padding around a cluster of widgets
- you want to apply a shared background/surface to a region
- you're manually managing child widgets with `pack()` or `grid()`

**Consider a different control when:**

- you want automatic vertical/horizontal stacking with gaps -> use [PackFrame](packframe.md)
- you need a 2D grid layout with auto-placement -> use [GridFrame](gridframe.md)
- the group needs a visible label (a titled section) -> use [LabelFrame](labelframe.md)

---

## Appearance

### Styling

`Frame` is commonly used to create "surface" regions:

- card-like blocks

- sidebar backgrounds

- header/footer regions

If your theme supports bordered/card styles, prefer named styles like `Card.TFrame` for consistency.

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

### `bootstyle` / `style`

Use `bootstyle` for semantic tokens, or `style=` for a concrete ttk style name.

```python
ttk.Frame(app, bootstyle="secondary")
ttk.Frame(app, style="Card.TFrame")
```

---

## Examples & patterns

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

---

## Behavior

- Frames are **containers only** (no click/selection behavior).

- Use the frame as the parent for widgets you want visually/structurally grouped.

- With `Frame`, you manually call `pack()` or `grid()` on each child widget.

- For automatic layout management, use [PackFrame](packframe.md) or [GridFrame](gridframe.md) instead.

- A `Frame` is not interactive; it exists to:

    - group related widgets
    - apply padding/margins around a region
    - host manual pack/grid layouts for a subsection of the UI
    - apply a shared visual surface (when styled)

---

## Additional resources

### Related widgets

- [PackFrame](packframe.md) -- frame with automatic pack-based layout (vertical/horizontal stacks)
- [GridFrame](gridframe.md) -- frame with automatic grid-based layout (2D grids with auto-placement)
- [LabelFrame](labelframe.md) -- a framed container with a label
- [Separator](separator.md) -- a visual divider between regions
- [PanedWindow](panedwindow.md) -- resizable split regions

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- **API Reference:** `ttkbootstrap.Frame`