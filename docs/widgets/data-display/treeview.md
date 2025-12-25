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

title: TreeView
---

# TreeView

`TreeView` displays **hierarchical data** in an expandable tree structure.

It’s ideal for representing parent/child relationships like folders, categories, or outlines.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.Treeview(app)
tree.pack(fill="both", expand=True)

tree.insert("", "end", text="Root")
app.mainloop()
```

---

## Core concepts

- Items and parents

- Expand/collapse state

- Selection and focus

---

## Common patterns

- File browsers

- Category navigation

- Outline views

---

## When should I use TreeView?

Use TreeView when:

- data has a natural hierarchy

Prefer **TableView** when:

- data is flat and column-based

---

## Related widgets

- **TableView**

- **ListView**

- **ScrollView**

---

## Reference

- **API Reference:** `ttkbootstrap.TreeView`

---

## Additional resources

### Related widgets

- [Badge](badge.md)

- [FloodGauge](floodgauge.md)

- [Label](label.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.TreeView`](../../reference/widgets/TreeView.md)
