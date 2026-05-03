---
title: Tables & Lists
---

# Tables & Lists

ttkbootstrap ships three widgets for displaying record-shaped data:
`TableView` for spreadsheet-style multi-column data, `ListView` for
virtualized rich lists, and `TreeView` for hierarchies. They cover
overlapping ground but optimize for different shapes — picking the right
one up front avoids fighting the widget later.

This guide covers:

- [Choosing the right widget](#choosing-the-right-widget)
- [Selection at a glance](#selection-at-a-glance)
- [TableView](#tableview) — columnar data, filtering, sorting, grouping, in-place editing
- [ListView](#listview) — virtualized lists, custom rows, drag/remove
- [TreeView](#treeview) — hierarchical data
- [DataSource integration](#datasource-integration) — pagination, persistence, custom backends

---

## Choosing the right widget

Pick by **data shape**, then by **scale**:

| Data shape | Recommended widget |
|---|---|
| Multi-column records the user needs to compare, sort, or filter | [`TableView`](#tableview) |
| Flat list of items with rich layouts (icon + title + caption + badge) | [`ListView`](#listview) |
| Very long flat lists where only some rows are visible at once | [`ListView`](#listview) (virtual scrolling) |
| Parent/child or tree-shaped data | [`TreeView`](#treeview) |
| Small static lists (under ~20 items) | A plain `Frame` of `Label`s |

Quick rule of thumb: if your data fits in a spreadsheet, reach for
`TableView`; if each row is a card, message, or contact entry, reach for
`ListView`; if items contain other items, reach for `TreeView`.

`TableView` and `ListView` both delegate data management to a
[DataSource](#datasource-integration), so they can both handle very
large datasets. The split is about presentation, not capacity.

---

## Selection at a glance

| | Modes | Read selection | Programmatic |
|---|---|---|---|
| `TableView` | `"none"`, `"single"`, `"multi"` | `table.selected_rows` (list of dicts) | `select_rows(iids)`, `deselect_rows()`, `select_all()` |
| `ListView` | `"none"`, `"single"`, `"multi"` | `lv.get_selected()` (list of record IDs) | `select_all()`, `clear_selection()` |
| `TreeView` | `"browse"` (single), `"extended"` (multi), `"none"` (via `selectmode=`) | `tree.selection()` (tuple of iids) | `tree.selection_set(...)`, `selection_add(...)`, `selection_remove(...)` |

`TableView` returns full record dicts; `ListView` returns just the IDs
(call `get_datasource().read_record(rid)` to expand them); `TreeView`
returns Tk item iids and you supply the mapping back to your data.

---

## TableView

`TableView` is a sortable, filterable, paginated table backed by a
`SqliteDataSource`. Construct it with a list of column definitions and a
list of row dicts:

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

### Column definitions

Each column is either a plain string or a dict. Recognized dict keys:

| Key | Purpose |
|---|---|
| `key` | Field name in row dicts. Defaults to `text` when omitted. |
| `text` | Visible header text. Defaults to `key`. |
| `width` | Initial column width in pixels. |
| `minwidth` | Minimum column width during user resize. |

Plain-string columns are equivalent to `{"text": "Name"}` — fine for
quick prototypes but you'll want explicit `key`s once your row dicts
have more fields than columns.

### Loading and updating data

Row dicts pass straight through to the underlying datasource. The
public mutation API works in record-batches:

```python
table.set_data(rows)                                   # replace all rows
table.insert_rows([{"name": "Dan", "role": "PM"}])    # append (id auto-assigned)
table.update_rows([{"id": 3, "name": "Dani"}])         # update by id
table.delete_rows([3, 5])                              # by id, or by row dict containing 'id'
```

`insert_rows`, `update_rows`, and `delete_rows` fire `<<RowInsert>>`,
`<<RowUpdate>>`, and `<<RowDelete>>` so you can mirror changes
elsewhere in your UI.

To persist data to disk or share it across widgets, build a
`SqliteDataSource` yourself and pass it as `datasource=`:

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import SqliteDataSource

ds = SqliteDataSource("employees.db", page_size=50)
ds.set_data([{"name": "Alice", "role": "Engineer"}])

table = ttk.TableView(
    app,
    datasource=ds,
    columns=[{"key": "name", "text": "Name"}, {"key": "role", "text": "Role"}],
)
```

`TableView` requires a `SqliteDataSource` (or subclass) — its filtering,
sorting, and grouping operations dispatch to SQL. See the
[DataSource guide](datasource.md) for the full datasource API.

### Selection and click events

```python
table.on_selection_changed(lambda e: print(e.data["records"]))
table.on_row_click(lambda e: print("clicked", e.data["record"]))
table.on_row_double_click(lambda e: print("opened", e.data["record"]))
```

Selection mode is set at construction:

```python
table = ttk.TableView(app, selection_mode="multi")  # "single" | "multi" | "none"
```

Read the current selection through properties:

```python
selected = table.selected_rows   # list[dict] — selected records
visible  = table.visible_rows    # list[dict] — what's rendered now
```

The `<<RowClick>>`, `<<RowDoubleClick>>`, and `<<RowRightClick>>`
events all carry `event.data = {"record": dict, "iid": str}`.
`<<SelectionChange>>` carries `{"records": list[dict], "iids": list[str]}`.

### Filtering, sorting, grouping

These are first-class on `TableView`:

```python
# SQL-style WHERE clause
table.set_filters("role = 'Engineer' AND tenure >= 3")
table.clear_filters()

# Sort by a column
table.set_sorting("tenure", ascending=False)
table.clear_sorting()

# Group rows by a column (only when allow_grouping=True at construction)
table.set_grouping("role")
table.expand_all()
table.collapse_all()
table.clear_grouping()
```

Filter expressions use the same syntax as the underlying datasource —
see [DataSource filtering](datasource.md#filtering) for the full
operator list (`=`, `!=`, `>`, `>=`, `<`, `<=`, `LIKE`, `IN`, `CONTAINS`,
`STARTSWITH`, `ENDSWITH`, plus `AND`/`OR`).

A built-in search bar drives `set_filters` for you. Configure it with
the `enable_search`, `search_mode` (`"standard"` or `"advanced"`), and
`search_trigger` (`"enter"` or `"input"`) construction options.

### Pagination

Default mode is paged with a footer; the user pages explicitly:

```python
table.next_page()
table.previous_page()
table.first_page()
table.last_page()
table.go_to_page(0)
```

Pass `paging_mode="virtual"` to render a continuous scroll area instead
of pages. Use standard paging for predictable pagination UX; use virtual
scrolling for very large datasets where the user just wants to scan.

### In-place editing

`TableView` can render an Add / Edit / Delete toolbar driven by a
[FormDialog](../widgets/dialogs/formdialog.md):

```python
table = ttk.TableView(
    app,
    columns=[{"key": "name", "text": "Name"}, {"key": "email", "text": "Email"}],
    rows=[],
    enable_adding=True,
    enable_editing=True,
    enable_deleting=True,
)
```

Form fields are inferred from the column keys. Customize the dialog
layout, validators, and placeholders with `form_options=` — see the
[forms guide](forms.md) for the full schema.

### Other useful options

| Option | Effect |
|---|---|
| `striped=True` | Alternating row backgrounds |
| `show_column_chooser=True` | Toolbar button to hide/show columns |
| `allow_grouping=True` | Enables the grouping menu in the header context menu |
| `enable_exporting=True` | Adds a CSV export menu |
| `show_hscrollbar=True` | Horizontal scrollbar for wide tables |
| `density="compact"` (via Frame kwarg) | Tighter row spacing |

---

## ListView

`ListView` virtualizes the visible rows: it only builds widgets for
what's on screen, recycling them as the user scrolls. That makes it
fast even with tens of thousands of records. Each row is a
`ListItem` — an icon plus up to three lines of text plus a trailing
badge.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Lists", size=(420, 500))

lv = ttk.ListView(
    app,
    items=[
        {"id": 1, "title": "Inbox", "text": "12 unread", "icon": "inbox"},
        {"id": 2, "title": "Sent",  "text": "Yesterday", "icon": "send"},
        {"id": 3, "title": "Drafts", "text": "3 items", "icon": "file-earmark"},
    ],
    selection_mode="single",
)
lv.pack(fill="both", expand=True)

app.mainloop()
```

If you don't supply an `id` field, one is auto-assigned from the item
position; supply your own when you need stable IDs that survive a
reload.

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

Any field you omit is hidden — you can build a plain title-only list
with just `[{"title": "..."}, ...]`, or a chat-style list with all
five fields.

### Selection and item events

```python
lv = ttk.ListView(app, items=items, selection_mode="multi")

lv.on_selection_changed(lambda e: print(lv.get_selected()))
lv.on_item_click(lambda e: print("clicked", e.data["title"]))
```

`get_selected()` returns the list of selected record IDs — call
`lv.get_datasource().read_record(rid)` to fetch the full record from
the datasource if you need the other fields. `<<SelectionChange>>`
itself carries no data; query the list when the event fires.

`<<ItemClick>>` carries the full record dict as `event.data` — fields
like `e.data["title"]` resolve directly.

Drive selection programmatically with `lv.select_all()` (multi-select
only) and `lv.clear_selection()`.

### CRUD

```python
lv.insert_item({"title": "New thing"})         # id auto-assigned
lv.update_item(99, {"title": "Renamed"})       # by id
lv.delete_item(99)
lv.reload()                                    # refetch from datasource
```

Each method fires the matching `<<ItemInsert>>`, `<<ItemUpdate>>`, or
`<<ItemDelete>>` virtual event.

### Custom rows

For richer layouts than the five default fields, supply a
`row_factory`. The factory must accept a parent widget plus arbitrary
keyword arguments (`ListView` passes interaction settings through), and
return a `ListItem` subclass that overrides `update_data`:

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.list import ListItem

class MessageRow(ListItem):
    def update_data(self, record):
        # The base implementation handles selection/focus/standard fields.
        # Map your own field names onto the standard ones first, then defer.
        if record and "__empty__" not in record:
            record = dict(record)
            record["title"] = record.get("subject", "")
            record["text"] = record.get("preview", "")
            record["caption"] = record.get("sent_at", "")
        super().update_data(record)

app = ttk.App()
messages = [
    {"id": 1, "subject": "Lunch?", "preview": "Free at 12?", "sent_at": "10:14"},
    {"id": 2, "subject": "Re: Demo", "preview": "Looks great", "sent_at": "Yesterday"},
]

lv = ttk.ListView(
    app,
    items=messages,
    row_factory=lambda parent, **kw: MessageRow(parent, **kw),
)
lv.pack(fill="both", expand=True)
```

Because rows are recycled as the user scrolls, `update_data` is called
repeatedly with different records on the same widget. Keep it
side-effect-free: read fields out of `record`, push them into widgets,
return.

### Drag, remove, density

```python
lv = ttk.ListView(
    app,
    items=items,
    enable_dragging=True,        # drag-handle reordering
    enable_removing=True,        # per-row remove button
    striped=True,                # alternating row backgrounds
    density="compact",           # tighter row padding
    show_separator=True,         # separator line between items
)
```

Drag and remove fire `<<ItemDragEnd>>` and `<<ItemDelete>>`
respectively. `<<ItemDragEnd>>` carries
`{"moved": bool, "source_index": int, "target_index": int}`.

### Custom datasources

`ListView` also accepts any object satisfying `DataSourceProtocol` in
place of `items=`:

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import MemoryDataSource

ds = MemoryDataSource(page_size=20)
ds.set_data([{"title": f"Item {i}"} for i in range(10_000)])

lv = ttk.ListView(app, datasource=ds, selection_mode="single")
```

`SqliteDataSource` and `FileDataSource` work too. See
[DataSource integration](#datasource-integration) below.

---

## TreeView

`TreeView` wraps `ttk.Treeview` for hierarchical data — file trees,
document outlines, org charts. It's a low-level widget: you populate
it with `insert(parent, index, ...)` calls, and read selection with
the standard Tk `selection()` method.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Tree", size=(420, 400))

tree = ttk.TreeView(app, columns=("size",), show="tree headings")
tree.heading("#0", text="Name")
tree.heading("size", text="Size")
tree.pack(fill="both", expand=True)

root = tree.insert("", "end", text="Project", open=True)
src  = tree.insert(root, "end", text="src", open=True)
tree.insert(src, "end", text="main.py", values=("4 KB",))
tree.insert(src, "end", text="utils.py", values=("2 KB",))
tree.insert(root, "end", text="README.md", values=("1 KB",))

app.mainloop()
```

Set `selectmode="extended"` (or `"browse"` for single, `"none"` to
disable) to control selection.

Selection and expand events use the standard Tk virtual events:

```python
tree.bind("<<TreeviewSelect>>", lambda e: print(tree.selection()))
tree.bind("<<TreeviewOpen>>",   lambda e: print("expanded", tree.focus()))
tree.bind("<<TreeviewClose>>",  lambda e: print("collapsed", tree.focus()))
```

`TreeView` does **not** carry the filtering, sorting, search, paging,
or grouping machinery that `TableView` provides — that's `TableView`'s
job. Use `TreeView` for the hierarchy itself, not for table-style data
dressed up with a tree column.

For deeper customization (icons per node, custom headers, surface
colors), see the [TreeView reference](../widgets/data-display/treeview.md).

---

## DataSource integration

A **DataSource** is a pluggable backend that owns pagination, filtering,
sorting, selection, and CRUD. ttkbootstrap ships three built-in
implementations:

| Class | Best for |
|---|---|
| `MemoryDataSource` | Small to medium datasets, prototypes |
| `SqliteDataSource` | Large datasets, persistence, SQL queries |
| `FileDataSource` | Loading from CSV/JSON/JSONL files |

All of them implement `DataSourceProtocol`, and `ListView` accepts any
object that does. `TableView` is more constrained: its filter/sort/group
code dispatches to SQL, so it requires a `SqliteDataSource` (or a
subclass).

### Wiring a DataSource

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import SqliteDataSource

ds = SqliteDataSource("app.db", page_size=100)
ds.set_data([{"name": "Alice"}, {"name": "Bob"}])

# TableView requires a SqliteDataSource:
table = ttk.TableView(app, datasource=ds, columns=[{"key": "name", "text": "Name"}])

# ListView accepts any DataSourceProtocol:
lv = ttk.ListView(app, datasource=ds)
```

When you pass `rows=` (TableView) or `items=` (ListView) without an
explicit `datasource=`, the widget creates its own in-memory source
behind the scenes — you don't need a DataSource for casual use.

### Custom datasources

Implement `DataSourceProtocol` to back `ListView` with a database, an
HTTP API, a generator, or any other source:

```python
from ttkbootstrap.datasource import DataSourceProtocol

class ApiDataSource:                   # implements DataSourceProtocol
    page_size = 50
    def total_count(self) -> int: ...
    def get_page_from_index(self, start, count) -> list[dict]: ...
    # ...plus the rest of the protocol
```

The full protocol — including pagination, CRUD, selection, and filter
methods — is documented in the [DataSource guide](datasource.md).

### Pagination semantics

| Mode | Widget | Behavior |
|---|---|---|
| Standard paging | `TableView` (default) | Footer with page numbers; user clicks to advance |
| Virtual scroll | `TableView` (`paging_mode="virtual"`) | Continuous scroll, rows fetched as needed |
| Virtual scroll | `ListView` (always) | Only visible rows are built; scrolling fetches the next slice |

`page_size` on the datasource controls the chunk size in all three
cases. Tune it for the network/disk cost of fetching a page, not for
visual layout.

---

## Patterns and tips

### Keep selection state in the datasource

Both `TableView` and `ListView` track selection on the underlying
datasource, which means selection survives reloads, page changes, and
filter swaps. Read it via `selected_rows` / `get_selected()` rather
than maintaining a parallel list yourself.

### Refresh after external mutations

If you mutate rows outside the widget (a background worker writes to
the SQLite file, an API push updates a record), call
`table.set_data(...)` or `lv.reload()` to repaint. Don't poke the
private internals.

### Don't fight virtual scrolling

`ListView` reuses row widgets as the user scrolls. Build whatever
structure you need once in your `row_factory`, and do per-record work
in `update_data` — never in the factory. The factory runs once per
pool slot; `update_data` runs on every scroll.

### Pick `paging_mode` deliberately

For `TableView`, `paging_mode="standard"` is more predictable for users
(visible page indicator, explicit navigation). `paging_mode="virtual"`
is smoother for very large datasets but hides the page indicator.
Decide once based on the dataset shape — switching at runtime isn't
supported.

### Filter at the datasource, not in Python

`TableView.set_filters` and `SqliteDataSource.set_filter` push the
predicate to SQL. Don't pre-filter rows in Python and feed the result
to `set_data` — you'll lose the row IDs the widget uses for selection
tracking, and you'll re-do the work every time the user changes the
filter.

---

## Additional resources

- [TableView reference](../widgets/data-display/tableview.md) — full widget API
- [ListView reference](../widgets/data-display/listview.md) — full widget API
- [TreeView reference](../widgets/data-display/treeview.md) — full widget API
- [DataSource guide](datasource.md) — filtering, sorting, custom backends
- [Forms guide](forms.md) — used by `TableView`'s built-in editor
