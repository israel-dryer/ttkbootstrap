---
title: Separator
---

# Separator

`Separator` is a **layout utility** for creating a subtle visual divider between regions.

It wraps `ttk.Separator` and is used to separate content sections without adding heavy visual noise -- common in
forms, panels, tool areas, and menus.

<!--
IMAGE: Separator horizontal and vertical
Suggested: Horizontal separator between form sections; vertical separator between sidebar + content
Theme variants: light / dark
-->

---

## Quick start

### Horizontal separator

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Section A").pack(anchor="w", padx=20, pady=(20, 8))
ttk.Separator(app, orient="horizontal").pack(fill="x", padx=20, pady=8)
ttk.Label(app, text="Section B").pack(anchor="w", padx=20, pady=(8, 20))

app.mainloop()
```

### Vertical separator

```python
sep = ttk.Separator(app, orient="vertical")
sep.pack(side="left", fill="y", padx=8, pady=8)
```

---

## When to use

Use `Separator` when:

- you need a light visual break between groups

- whitespace alone doesn't provide enough structure

**Consider a different control when:**

- spacing and alignment already clearly indicate grouping

- too many lines would add visual clutter

---

## Appearance

Separators are best used sparingly to:

- separate groups of controls

- distinguish header/content/footer regions

- divide side-by-side panes (vertical separators)

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

### `color` / `style`

If your theme exposes separator variants, apply them via `color` or `style`.

```python
ttk.Separator(app, color="secondary")
```

---

## Examples & patterns

### `orient`

- `"horizontal"` (default)

- `"vertical"`

```python
ttk.Separator(app, orient="horizontal")
ttk.Separator(app, orient="vertical")
```

---

## Behavior

- Separators do not receive focus and are not interactive.

- Use geometry manager options (`fill`, `padx`, `pady`) to control length and spacing.

---

## Additional resources

### Related widgets

- [Frame](frame.md) -- group related controls into regions

- [LabelFrame](labelframe.md) -- labeled container grouping

- [PanedWindow](panedwindow.md) -- resizable split regions

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- [`ttkbootstrap.Separator`](../../reference/widgets/Separator.md)