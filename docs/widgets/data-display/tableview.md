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

title: TableView
---

# TableView

`TableView` displays **tabular data** with rows and columns.

It is suitable for datasets where users need to scan, sort, and select structured records.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

tv = ttk.TableView(
    app,
    coldata=["Name", "Status"],
    rowdata=[("Item A", "Ready"), ("Item B", "Pending")],
)
tv.pack(fill="both", expand=True)

app.mainloop()
```

---

## Core concepts

- Column definitions

- Row data

- Selection model

---

## Features

- Sorting

- Row selection

- Scrollbars

- Optional headers and footers

---

## Events

TableView emits events for selection, activation, and edits (if enabled).

---

## When should I use TableView?

Use TableView when:

- data is multi-column

- rows are uniform and comparable

Prefer **ListView** when:

- data is simple or visually rich per row

---

## Related widgets

- **TreeView**

- **ListView**

- **ContextMenu**

---

## Reference

- **API Reference:** `ttkbootstrap.TableView`

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

- [`ttkbootstrap.TableView`](../../reference/widgets/TableView.md)
