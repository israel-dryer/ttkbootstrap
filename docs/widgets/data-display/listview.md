---
title: ListView
---

# ListView

`ListView` is a **virtual scrolling list** for displaying large datasets efficiently.

It renders only the visible rows (plus a small overscan), making it suitable for thousands of records while still supporting selection, deletion, dragging, and custom row layouts.

---

## Basic usage

### Simple list

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

---

## Data model

`ListView` works with either:

- `items=[...]` — a simple list of dicts (or primitives), or
- `datasource=...` — a custom data source implementing the `DataSourceProtocol`

### Required fields

Records are expected to have a stable identifier:

- `id` — unique record id (required for selection/deleting/moving)

The default `ListItem` also recognizes:

- `title` — main heading
- `text` — body text
- `caption` — small caption text
- `icon` — icon spec shown on the left
- `badge` — small text on the right

---

## Selection

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

---

## Deleting and dragging

Enable item actions:

```python
lv = ListView(
    app,
    items=data,
    enable_deleting=True,
    enable_dragging=True,
)
```

When enabled, rows expose UI affordances and `ListView` emits events:

- `<<ItemDelete>>`, `<<ItemDeleteFail>>`
- `<<ItemDragStart>>`, `<<ItemDrag>>`, `<<ItemDragEnd>>`

---

## Alternating rows, separators, and scrollbars

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

---

## Events

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

---

## Public API

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

## Custom row layouts

Use `row_factory` to supply your own `ListItem`-compatible row widget.

```python
def make_row(master, **kwargs):
    return ttk.ListItem(master, **kwargs)  # or your custom widget

lv = ListView(app, datasource=my_source, row_factory=make_row)
```

!!! tip "Row factory"
    If you need a fully custom row template, implement a widget that provides an `update_data(record)` method and honors the selection/focus conventions you want.

---

## When should I use ListView?

Use `ListView` when:

- you need to display a long list efficiently (virtual scrolling)
- rows can include rich content (icon/title/text/badge)
- you need selection, deletion, or drag reordering

Prefer `TableView` when:

- data is strongly column-based and users compare fields across rows

Prefer `TreeView` when:

- your data is hierarchical

---

## Related widgets

- **ListItem** — the default row widget used by ListView
- **TableView** — tabular record display
- **TreeView** — hierarchical record display
- **Scrollbar / ScrollView** — scrolling containers

---

## Reference

- **API Reference:** `ttkbootstrap.ListView`
