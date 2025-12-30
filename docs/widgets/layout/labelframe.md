---
title: LabelFrame
---

# LabelFrame

`LabelFrame` is a **layout container** that groups related widgets under a **visible label**.

It wraps `ttk.Labelframe`, participates in ttkbootstrap styling, and is ideal for labeled sections (settings groups,
form clusters, option panels) where the title improves scanability.

<!--
IMAGE: Labeled group box
Suggested: LabelFrame titled "Network" containing a few related controls
Theme variants: light / dark
-->

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

group = ttk.LabelFrame(app, text="Network", padding=16)
group.pack(fill="x", padx=20, pady=20)

ttk.CheckButton(group, text="Use proxy").pack(anchor="w")
ttk.Entry(group).pack(fill="x", pady=(8, 0))

app.mainloop()
```

---

## When to use

Use `LabelFrame` when:

- the grouped controls benefit from a section title

- the title should be visually attached to the region

**Consider a different control when:**

- you want grouping without a label -- use [Frame](frame.md)

- the label belongs in surrounding layout (e.g., page header) -- use [Frame](frame.md) with a separate [Label](../data-display/label.md)

---

## Appearance

### Styling

Use `LabelFrame` when the label should be part of the visual grouping.

For more "modern card" layouts where the label is separate, you may prefer:

- a `Frame` with a `Label` above it

- a `Frame` styled as a card, with header content

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

### `color` / `style`

Apply semantic styling (or a specific style name).

```python
ttk.LabelFrame(app, text="Group", color="secondary")
ttk.LabelFrame(app, text="Group", style="Card.TLabelframe")
```

---

## Examples & patterns

### `text`

Sets the group label.

```python
ttk.LabelFrame(app, text="Appearance")
```

### `labelanchor`

Controls where the label appears relative to the frame.

```python
ttk.LabelFrame(app, text="Network", labelanchor="n")   # top (common)
ttk.LabelFrame(app, text="Network", labelanchor="w")   # left
ttk.LabelFrame(app, text="Network", labelanchor="s")   # bottom
```

### `padding`

Inner spacing for the content region.

```python
ttk.LabelFrame(app, text="Options", padding=(16, 12))
```

---

## Behavior

- LabelFrames are **containers only** (no interactive behavior).

- Use `text=` (or a label widget, if your implementation supports it) to describe the group.

- Content layout works the same as `Frame` (pack/grid inside the container).

- A `LabelFrame` is like a `Frame`, but with an integrated label:

    - the label provides context for the grouped controls

    - the border/outline visually separates the region

    - content is packed/gridded inside the container like any other frame

---

## Additional resources

### Related widgets

- [Frame](frame.md) -- general-purpose container

- [Separator](separator.md) -- divider between labeled regions

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- [`ttkbootstrap.LabelFrame`](../../reference/widgets/LabelFrame.md)