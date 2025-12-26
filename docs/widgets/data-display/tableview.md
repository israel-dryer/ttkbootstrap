---
title: TableView
---

# TableView

`TableView` displays **tabular data** with rows and columns.

It is suitable for datasets where users need to scan, sort, and select structured records.

---

## Quick start

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

## When to use

Use TableView when:

- data is multi-column

- rows are uniform and comparable

- users need to scan, sort, or filter structured records

### Consider a different control when...

- **Data is simple or visually rich per row** — use [ListView](listview.md) instead

- **Your data is hierarchical** — use [TreeView](treeview.md) instead

- **You only need to display a single value** — use [Label](label.md) or [Badge](badge.md)

---

## Appearance

### Styling

TableView supports theming through ttkbootstrap:

```python
ttk.TableView(app, bootstyle="primary")
```

!!! link "Design System"
    See [Design System](../../design-system/index.md) for color tokens and theming guidelines.

---

## Examples & patterns

### Core concepts

- **Column definitions** — define the structure and headers of the table

- **Row data** — the actual data records displayed

- **Selection model** — how rows are selected

### Column definitions

```python
tv = ttk.TableView(
    app,
    coldata=[
        {"text": "Name", "width": 150},
        {"text": "Status", "width": 100},
        {"text": "Date", "width": 120},
    ],
    rowdata=data,
)
```

### Features

- Sorting — click column headers to sort

- Row selection — single or multi-select

- Scrollbars — automatic scrolling for large datasets

- Optional headers and footers

### Common options

- `coldata` — column definitions (list of strings or dicts)

- `rowdata` — list of row tuples or lists

- `height` — number of visible rows

- `bootstyle` — color theme

---

## Behavior

### Events

TableView emits events for selection, activation, and edits (if enabled):

- `<<TreeviewSelect>>` — selection changed

- `<<TreeviewOpen>>` — row expanded (if hierarchical)

- `<<TreeviewClose>>` — row collapsed

### Selection

```python
tv.view.selection()  # Get selected items
tv.view.selection_set(item_id)  # Select an item
```

---

## Reactivity

TableView can be updated dynamically:

```python
# Refresh data
tv.build_table_data(coldata=new_columns, rowdata=new_rows)
```

!!! link "Signals"
    See [Signals](../../capabilities/signals/signals.md) for reactive programming patterns.

---

## Additional resources

### Related widgets

- [TreeView](treeview.md) — hierarchical record display

- [ListView](listview.md) — virtual scrolling list

- [ContextMenu](../navigation/contextmenu.md) — right-click menus

### Framework concepts

- [Design System](../../design-system/index.md) — colors, typography, and theming

- [Signals](../../capabilities/signals/signals.md) — reactive data binding

- [DataSource](../../guides/datasource.md) — data management with filtering, sorting, pagination

### API reference

- [`ttkbootstrap.TableView`](../../reference/widgets/TableView.md)