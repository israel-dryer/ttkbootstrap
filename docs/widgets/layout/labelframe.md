---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: LabelFrame
---

# LabelFrame

`LabelFrame` is a **layout container** that groups related widgets under a **visible label**.

It wraps `ttk.Labelframe`, participates in ttkbootstrap styling, and is ideal for labeled sections (settings groups,
form clusters, option panels) where the title improves scanability.

<!--
IMAGE: Labeled group box
Suggested: LabelFrame titled “Network” containing a few related controls
Theme variants: light / dark
-->

---

## Overview

A `LabelFrame` is like a `Frame`, but with an integrated label:

- the label provides context for the grouped controls

- the border/outline visually separates the region

- content is packed/gridded inside the container like any other frame

---

## Basic usage

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

## Common options

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

### `bootstyle` / `style`

Apply semantic styling (or a specific style name).

```python
ttk.LabelFrame(app, text="Group", bootstyle="secondary")
ttk.LabelFrame(app, text="Group", style="Card.TLabelframe")
```

---

## Behavior

- LabelFrames are **containers only** (no interactive behavior).

- Use `text=` (or a label widget, if your implementation supports it) to describe the group.

- Content layout works the same as `Frame` (pack/grid inside the container).

---

## Styling

Use `LabelFrame` when the label should be part of the visual grouping.

For more “modern card” layouts where the label is separate, you may prefer:

- a `Frame` with a `Label` above it

- a `Frame` styled as a card, with header content

---

## When should I use LabelFrame?

Use `LabelFrame` when:

- the grouped controls benefit from a section title

- the title should be visually attached to the region

Prefer **Frame** when:

- you want grouping without a label

- the label belongs in surrounding layout (e.g., page header)

---

## Related widgets

- **Frame** — general-purpose container

- **Separator** — divider between labeled regions

---

## Reference

- **API Reference:** `ttkbootstrap.LabelFrame`

---

## Additional resources

### Related widgets

- [Frame](frame.md)

- [PanedWindow](panedwindow.md)

- [Scrollbar](scrollbar.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.LabelFrame`](../../reference/widgets/LabelFrame.md)
