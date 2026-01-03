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
    columns=["Name", "Status"],
    rows=[("Item A", "Ready"), ("Item B", "Pending")],
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

### Striped rows

Enable alternating row colors for better readability:

```python
tv = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    striped=True,
    striped_background="background[+1]",  # custom alternating color
)
```

### Styling

TableView supports theming through ttkbootstrap:

```python
ttk.TableView(app, accent="primary")
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
    columns=[
        {"text": "Name", "key": "name", "width": 150},
        {"text": "Status", "key": "status", "width": 100},
        {"text": "Date", "key": "date", "width": 120},
    ],
    rows=data,
)
```

### Selection

Control selection behavior with `selection_mode`:

- `"none"` — no selection allowed

- `"single"` — one row at a time (default)

- `"multi"` — multiple rows can be selected

```python
tv = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    selection_mode="multi",
    allow_select_all=True,
)
```

### Editing

Enable inline editing, adding, and deleting:

```python
tv = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    enable_adding=True,
    enable_editing=True,
    enable_deleting=True,
)
```

### Filtering & search

Enable filtering and search capabilities:

```python
tv = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    enable_filtering=True,
    enable_header_filtering=True,
    enable_search=True,
    search_mode="standard",
    search_trigger="enter",  # or "input" for live search
)
```

### Paging

Configure pagination for large datasets:

```python
tv = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    paging_mode="standard",  # or "virtual" for virtual scrolling
    page_size=25,
    show_vscrollbar=True,
)
```

### Exporting

Enable data export functionality:

```python
tv = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    enable_exporting=True,
    export_scope="all",  # or "page"
    export_formats=("csv", "json"),
)
```

### Common options

**Core data:**

- `columns` — column definitions (list of strings or dicts)

- `rows` — list of row data

- `datasource` — optional custom data source

**Selection & sorting:**

- `selection_mode` — `"none"`, `"single"`, or `"multi"`

- `allow_select_all` — allow selecting all rows

- `sorting_mode` — `"single"` or `"none"`

**Filtering & search:**

- `enable_filtering` — enable filtering

- `enable_header_filtering` — filter controls in headers

- `enable_row_filtering` — per-row filtering

- `enable_search` — enable search box

- `search_mode` — `"standard"` or `"advanced"`

- `search_trigger` — `"enter"` or `"input"`

**Paging & scrolling:**

- `paging_mode` — `"standard"` or `"virtual"`

- `page_size` — rows per page

- `show_vscrollbar` — vertical scrollbar

- `show_hscrollbar` — horizontal scrollbar

**Editing:**

- `enable_adding` — allow adding rows

- `enable_editing` — allow inline editing

- `enable_deleting` — allow row deletion

**Exporting:**

- `enable_exporting` — enable export menu

- `export_scope` — `"page"` or `"all"`

- `export_formats` — tuple of format strings

**Appearance:**

- `striped` — alternating row colors

- `striped_background` — color for alternating rows

- `show_table_status` — show status bar

- `column_auto_width` — auto-size columns

---

## Behavior

### Events

TableView emits events for selection, activation, and edits:

- `<<RowClick>>` — row clicked

- `<<SelectionChange>>` — selection changed

- `<<RowEdit>>` — row edited

- `<<RowDelete>>` — row deleted

Preferred handlers:

```python
tv.on_row_click(lambda e: print("clicked:", e.data))
tv.on_selection_change(lambda e: print("selected:", tv.get_selected()))
```

### Public API

Common methods:

- `get_selected()` — get selected row data

- `reload()` — refresh table data

- `get_datasource()` — access underlying data source

---

## Reactivity

TableView can be updated dynamically:

```python
# Refresh data
tv.reload()
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