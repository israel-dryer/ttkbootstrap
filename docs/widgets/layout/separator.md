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

title: Separator
---

# Separator

`Separator` is a **layout utility** for creating a subtle visual divider between regions.

It wraps `ttk.Separator` and is used to separate content sections without adding heavy visual noise—common in
forms, panels, tool areas, and menus.

<!--
IMAGE: Separator horizontal and vertical
Suggested: Horizontal separator between form sections; vertical separator between sidebar + content
Theme variants: light / dark
-->

---

## Overview

Separators are best used sparingly to:

- separate groups of controls

- distinguish header/content/footer regions

- divide side-by-side panes (vertical separators)

---

## Basic usage

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

## Common options

### `orient`

- `"horizontal"` (default)

- `"vertical"`

```python
ttk.Separator(app, orient="horizontal")
ttk.Separator(app, orient="vertical")
```

### `bootstyle` / `style`

If your theme exposes separator variants, apply them via `bootstyle` or `style`.

```python
ttk.Separator(app, bootstyle="secondary")
```

---

## Behavior

- Separators do not receive focus and are not interactive.

- Use geometry manager options (`fill`, `padx`, `pady`) to control length and spacing.

---

## When should I use Separator?

Use `Separator` when:

- you need a light visual break between groups

- whitespace alone doesn’t provide enough structure

Avoid separators when:

- spacing and alignment already clearly indicate grouping

- too many lines would add visual clutter

---

## Related widgets

- **Frame** — group related controls into regions

- **LabelFrame** — labeled container grouping

- **PanedWindow** — resizable split regions (if applicable)

---

## Reference

- **API Reference:** `ttkbootstrap.Separator`

---

## Additional resources

### Related widgets

- [Frame](frame.md)

- [LabelFrame](labelframe.md)

- [PanedWindow](panedwindow.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Separator`](../../reference/widgets/Separator.md)
