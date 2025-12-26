---
title: ListView
---

# ListView

`ListView` is a **virtual scrolling list** for displaying large datasets efficiently.

It renders only the visible rows (plus a small overscan), making it suitable for thousands of records while still supporting selection, deletion, dragging, and custom row layouts.

---

## Quick start

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.primitives.listview import ListView

app = ttk.App()

items = [
    {"id": 1, "title": "Item 1", "text": "Description 1"},
    {"id": 2, "title": "Item 2", "text": "Description 2"},
]

lv = ListView(app, items=items)
lv.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `ListView` when:

- you need to display a long list efficiently (virtual scrolling)

- rows can include rich content (icon/title/text/badge)

- you need selection, deletion, or drag reordering

### Consider a different control when...

- **Data is strongly column-based and users compare fields across rows** — use [TableView](tableview.md) instead

- **Your data is hierarchical** — use [TreeView](treeview.md) instead

- **You have a small, static list** — a simple frame with labels may suffice

---

## Appearance

### Alternating rows, separators, and scrollbars

Common presentation options:

- `alternating_row_mode="even" | "odd" | "none"`

- `alternating_row_color="background[+1]"`

- `show_separator=True`

- `show_scrollbar=True`

```python
lv = ListView(
    app,
    items=data,
    alternating_row_mode="even",
    show_separator=True,
    show_scrollbar=False,  # mousewheel only
)
```

!!! link "Design System"
    See [Design System](../../design-system/index.md) for color tokens and theming guidelines.

---

## Examples & patterns

### Selection + events

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.primitives.listview import ListView

app = ttk.App()

lv = ListView(
    app,
    items=[{"id": i, "title": f"Item {i}"} for i in range(2000)],
    selection_mode="multi",
    show_selection_controls=True,
)
lv.pack(fill="both", expand=True, padx=20, pady=20)

def on_sel(_):
    print("selected:", lv.get_selected())

lv.on_selection_change(on_sel)

app.mainloop()
```

### Data model

`ListView` works with either:

- `items=[...]` — a simple list of dicts (or primitives), or

- `datasource=...` — a [DataSource](../../guides/datasource.md) implementing the `DataSourceProtocol`

#### Required fields

Records are expected to have a stable identifier:

- `id` — unique record id (required for selection/deleting/moving)

The default `ListItem` also recognizes:

- `title` — main heading

- `text` — body text

- `caption` — small caption text

- `icon` — icon spec shown on the left

- `badge` — small text on the right

### Selection

Set `selection_mode` to control selection behavior:

- `"none"` — no selection

- `"single"` — one selected item

- `"multi"` — multiple selected items

Optional selection UI:

- `show_selection_controls=True` shows checkbox/radio affordances

- `select_by_click` controls whether clicking the row selects it

```python
lv = ListView(app, items=data, selection_mode="single", select_by_click=True)
```

### Deleting and dragging

Enable item actions:

```python
lv = ListView(
    app,
    items=data,
    enable_deleting=True,
    enable_dragging=True,
)
```

### Custom row layouts

Use `row_factory` to supply your own `ListItem`-compatible row widget.

```python
def make_row(master, **kwargs):
    return ttk.ListItem(master, **kwargs)  # or your custom widget

lv = ListView(app, datasource=my_source, row_factory=make_row)
```

!!! tip "Row factory"
    If you need a fully custom row template, implement a widget that provides an `update_data(record)` method and honors the selection/focus conventions you want.

### Common options

- `items` — list of data records

- `datasource` — custom data source

- `selection_mode` — `"none"`, `"single"`, or `"multi"`

- `show_selection_controls` — show checkbox/radio controls

- `enable_deleting` — allow item deletion

- `enable_dragging` — allow drag reordering

---

## Behavior

### Events

ListView generates virtual events for higher-level behaviors:

- `<<SelectionChange>>` — selection state changed

- `<<ItemClick>>` — row clicked/activated (payload includes record data)

- `<<ItemDelete>>` / `<<ItemDeleteFail>>`

- `<<ItemInsert>>` / `<<ItemUpdate>>`

- `<<ItemDragStart>>` / `<<ItemDrag>>` / `<<ItemDragEnd>>`

Preferred handlers:

```python
lv.on_selection_change(lambda e: print(lv.get_selected()))
lv.on_item_click(lambda e: print("clicked:", e.data))
```

### Public API

Common methods:

- `get_selected()`

- `clear_selection()`

- `select_all()` (multi only)

- `reload()`

- `insert_item(data)`

- `update_item(record_id, data)`

- `delete_item(record_id)`

- `scroll_to_top()`, `scroll_to_bottom()`

- `get_datasource()`

---

## Reactivity

ListView can work with reactive data sources:

```python
items = ttk.Signal([{"id": 1, "title": "Item 1"}])
lv = ListView(app, items=items)

# Add new item
items.set([*items.get(), {"id": 2, "title": "Item 2"}])
```

!!! link "Signals"
    See [Signals](../../capabilities/signals/signals.md) for reactive programming patterns.

---

## Additional resources

### Related widgets

- [ListItem](../primitives/listitem.md) — the default row widget used by ListView

- [TableView](tableview.md) — tabular record display

- [TreeView](treeview.md) — hierarchical record display

- [Scrollbar](../layout/scrollbar.md) — scrolling controls

- [ScrollView](../layout/scrollview.md) — scrolling containers

### Framework concepts

- [Design System](../../design-system/index.md) — colors, typography, and theming

- [Signals](../../capabilities/signals/signals.md) — reactive data binding

- [DataSource](../../guides/datasource.md) — data management with filtering, sorting, pagination

### API reference

- [`ttkbootstrap.ListView`](../../reference/widgets/ListView.md)