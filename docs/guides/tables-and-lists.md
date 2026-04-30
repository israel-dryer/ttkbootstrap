---
title: Tables & Lists
---

# Tables & Lists

ttkbootstrap ships three widgets for displaying record-shaped data —
`TableView` for spreadsheet-style multi-column data, `ListView` for
virtualized rich lists, and `TreeView` for hierarchies. This guide
explains when to pick each one and how to wire them up.

This guide covers:

- **Choosing between TableView, ListView, and TreeView**
- **Loading and refreshing data**
- **Selection, click, and edit events**
- **Filtering, sorting, and grouping** in TableView
- **Custom rows** in ListView
- **DataSource integration** for both

---

## Choosing the right widget

| Data shape | Use |
|---|---|
| Multi-column records the user needs to compare, sort, or filter | `TableView` |
| Flat list of items with rich layouts (icon + title + caption + badge) | `ListView` |
| Very long datasets where only some rows are visible at a time | `ListView` (virtual scrolling) |
| Parent/child or tree-shaped data | `TreeView` |
| Small static lists (under ~20 items) | A plain `Frame` of `Label`s |

Quick rule of thumb: if your data fits in a spreadsheet, use `TableView`;
if each row is a card or a chat message, use `ListView`; if items
contain other items, use `TreeView`.

---

## TableView

`TableView` is a sortable, filterable, paginated table. It accepts a
list of column definitions and a list of rows (dicts):

```python
import ttkbootstrap as ttk

app = ttk.App(title="Tables", size=(800, 500))

table = ttk.TableView(
    app,
    columns=[
        {"key": "name", "text": "Name"},
        {"key": "role", "text": "Role"},
        {"key": "tenure", "text": "Years"},
    ],
    rows=[
        {"name": "Alice", "role": "Engineer", "tenure": 4},
        {"name": "Bob", "role": "Designer", "tenure": 2},
        {"name": "Carol", "role": "Engineer", "tenure": 7},
    ],
)
table.pack(fill="both", expand=True, padx=12, pady=12)

app.mainloop()
```

Columns may be plain strings (`["Name", "Role"]`) when you don't need a
key/title split.

### Loading and updating data

`TableView` is backed by an in-memory `SqliteDataSource` by default. The
public methods accept lists of dicts:

```python
table.set_data(rows)                          # replace all rows
table.insert_rows([{"name": "Dan", "email": "dan@example.com"}])  # append
table.update_rows([{"id": 3, "name": "Dani"}])  # update by id
table.delete_rows([3, 5])                     # delete by id (or row dict)
```

To persist data to disk or share it between widgets, build a
`SqliteDataSource` yourself and pass it as `datasource=`:

```python
from ttkbootstrap.datasource import SqliteDataSource

ds = SqliteDataSource("employees.db", page_size=50)
ds.set_data(rows)

table = ttk.TableView(app, datasource=ds, columns=[...])
```

See the [DataSource guide](datasource.md) for filtering, sorting, and
pagination on the source itself.

### Selection and click events

```python
table.on_selection_changed(lambda e: print(e.data["records"]))
table.on_row_click(lambda e: print("Clicked", e.data["record"]))
table.on_row_double_click(lambda e: open_detail(e.data["record"]))
```

Read the current selection through properties:

```python
selected = table.selected_rows    # list[dict]
visible  = table.visible_rows     # list[dict] — what's rendered now
```

Selection mode is configured at construction:

```python
table = ttk.TableView(app, ..., selection_mode="multi")  # "single" | "multi" | "none"
```

### Filtering, sorting, grouping

These are first-class on `TableView`:

```python
# SQL-style WHERE clause
table.set_filters("role = 'Engineer' AND tenure >= 3")
table.clear_filters()

# Sort by a column
table.set_sorting("tenure", ascending=False)
table.clear_sorting()

# Group rows by a column
table.set_grouping("role")
table.expand_all()                 # or expand_group("Engineer")
table.clear_grouping()
```

The filter syntax is the same as the underlying `SqliteDataSource` —
see [DataSource filtering](datasource.md#filtering) for the full list of
operators.

### Pagination

```python
table.next_page()
table.previous_page()
table.go_to_page(0)
```

Use `paging_mode="virtual"` to render a virtual scroll area instead of
pages.

### In-place editing

`TableView` can render an "Add / Edit / Delete" toolbar driven by a
[FormDialog](../widgets/dialogs/formdialog.md):

```python
table = ttk.TableView(
    app,
    columns=[...],
    rows=[...],
    enable_adding=True,
    enable_editing=True,
    enable_deleting=True,
)
```

The form fields are inferred from the column keys. Customize the dialog
with `form_options=`.

---

## ListView

`ListView` virtualizes the visible rows, so it stays fast for tens of
thousands of items. It expects a list of dicts (each with an `id`) or a
`DataSource`:

```python
from ttkbootstrap.widgets.composites.list import ListView

lv = ListView(
    app,
    items=[
        {"id": 1, "title": "Inbox", "text": "12 unread", "icon": "inbox"},
        {"id": 2, "title": "Sent",  "text": "Yesterday", "icon": "send"},
    ],
    selection_mode="single",
)
lv.pack(fill="both", expand=True)
```

`ListView` is imported directly from
`ttkbootstrap.widgets.composites.list`.

### Default row layout

When you don't supply a `row_factory`, `ListView` reads these fields
from each item dict:

| Field | Renders as |
|---|---|
| `icon` | Leading icon |
| `title` | Bold primary text |
| `text` | Secondary text |
| `caption` | Tertiary text |
| `badge` | Trailing badge |

### Selection and item events

```python
lv = ListView(app, items=items, selection_mode="multi")

lv.bind("<<SelectionChange>>", lambda e: print(lv.get_selected()))
lv.bind("<<ItemClick>>", lambda e: open_item(e.data["record"]))
```

Selection state lives on the underlying datasource — call
`lv.get_selected()` for the list of selected records, `lv.select_all()`
or `lv.clear_selection()` to drive it programmatically.

### CRUD

```python
lv.insert_item({"id": 99, "title": "New thing"})
lv.update_item(99, {"title": "Renamed thing"})
lv.delete_item(99)
lv.reload()
```

### Custom rows

For richer layouts, supply a `row_factory` that returns a `ListItem`
subclass. Each instance is reused as the user scrolls (the row pool is
recycled), so factories should be cheap and idempotent:

```python
from ttkbootstrap.widgets.composites.list import ListView, ListItem

class MessageRow(ListItem):
    def render(self, record):
        self.title.configure(text=record["subject"])
        self.text.configure(text=record["preview"])

lv = ListView(app, items=messages, row_factory=lambda parent: MessageRow(parent))
```

### Drag, remove, density

```python
lv = ListView(
    app,
    items=items,
    enable_dragging=True,        # drag-handle reordering
    enable_removing=True,        # per-row remove button
    striped=True,
    density="compact",
)
```

Drag and remove fire `<<ItemDragEnd>>` and `<<ItemDelete>>` events.

---

## TreeView

`TreeView` wraps `ttk.Treeview` for hierarchical data. Use it when items
have parents and children — file trees, document outlines, org charts:

```python
import ttkbootstrap as ttk

tree = ttk.TreeView(app, columns=("size",), show="tree headings")
tree.heading("size", text="Size")
tree.pack(fill="both", expand=True)

root = tree.insert("", "end", text="Project")
src  = tree.insert(root, "end", text="src")
tree.insert(src, "end", text="main.py", values=("4 KB",))
tree.insert(src, "end", text="utils.py", values=("2 KB",))
```

Selection and expand events use the standard Tk virtual events:

```python
tree.bind("<<TreeviewSelect>>", lambda e: print(tree.selection()))
tree.bind("<<TreeviewOpen>>",   lambda e: print("expanded", tree.focus()))
```

`TreeView` does **not** carry filtering, sorting, or pagination
machinery — that's `TableView`'s job. Use `TreeView` for the hierarchy,
not for table-style data dressed up with a tree column.

---

## DataSource integration

For anything beyond an in-memory list — persistence, background loading,
filtering against a database, sharing data between widgets — drive your
table or list from a `DataSource`:

```python
from ttkbootstrap.datasource import SqliteDataSource

ds = SqliteDataSource("app.db", page_size=100)
ds.set_data(rows)

table = ttk.TableView(app, datasource=ds, columns=cols)
```

`TableView` requires a `SqliteDataSource` (or a subclass) — its
filter/sort/group operations dispatch to SQL. `ListView` accepts any
object satisfying `DataSourceProtocol`, including custom backends:

```python
from ttkbootstrap.datasource import DataSourceProtocol
from ttkbootstrap.widgets.composites.list import ListView

class ApiDataSource:                   # implements DataSourceProtocol
    page_size = 50
    def total_count(self) -> int: ...
    def get_page_from_index(self, start, count) -> list[dict]: ...
    # ... rest of the protocol

lv = ListView(app, datasource=ApiDataSource())
```

The full DataSource API is documented in the
[DataSource guide](datasource.md).

---

## Patterns and tips

### Keep selection state in the datasource

Both `TableView` and `ListView` track selection on the underlying
datasource, which means selection survives reloads, page changes, and
filter swaps. Read it via `selected_rows` / `get_selected()` rather than
maintaining your own list.

### Refresh after external mutations

If you mutate rows outside the widget (e.g., a background worker writes
to the SQLite file), call `table.set_data(...)` or
`lv.reload()` to repaint.

### Don't fight virtual scrolling

`ListView` reuses row widgets as the user scrolls. Configure rows in
your `row_factory` once; do per-record work in the row's `render`
method, not in the factory.

### Pick `paging_mode` early

For `TableView`, `paging_mode="standard"` (pages with a footer) is
predictable for users; `paging_mode="virtual"` is smoother for very
large datasets but disables the page indicator. Decide once based on
the dataset shape — don't switch at runtime.

---

## Additional resources

- [TableView](../widgets/data-display/tableview.md) — full widget reference
- [ListView](../widgets/data-display/listview.md) — full widget reference
- [TreeView](../widgets/data-display/treeview.md) — hierarchical widget
- [DataSource guide](datasource.md) — filtering, sorting, custom backends
- [Forms guide](forms.md) — used by `TableView`'s built-in editor
