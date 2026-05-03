---
title: ListView
---

# ListView

`ListView` is a **virtualized scrolling list** for flat record sets.
It builds a fixed pool of row widgets and recycles them as the user
scrolls, so a list of ten thousand records costs the same as a list
of fifty. Each row is a `ListItem` by
default — a row template with optional icon, title, body text,
caption, and trailing badge — and you can substitute any
`update_data(record)`-compatible widget through `row_factory`.

Unlike [TableView](tableview.md) (column-aligned record grids) and
[TreeView](treeview.md) (hierarchical rows that expand and
collapse), ListView is a **flat** list with rich row layouts.
Selection is record-based (`get_selected()` returns IDs, not row
indices), and the widget supports keyboard navigation, optional
drag reordering, and per-row remove buttons.

<figure markdown>
![listview](../../assets/dark/widgets-listview.png#only-dark)
![listview](../../assets/light/widgets-listview.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

items = [
    {"id": 1, "icon": "file-earmark-text", "title": "Quarterly report",
     "caption": "Updated 2 minutes ago"},
    {"id": 2, "icon": "file-earmark-image", "title": "Cover photo",
     "caption": "1.2 MB · PNG"},
    {"id": 3, "icon": "file-earmark-music", "title": "Theme song",
     "caption": "3:24 · MP3"},
]

lv = ttk.ListView(app, items=items, selection_mode="single", striped=True)
lv.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

`items=` accepts plain dicts (or primitives, which are wrapped into
`{"id": i, "value": ...}`); the widget builds an internal data
source for you. For database-backed or computed lists, supply your
own `datasource=` instead.

---

## Data model

ListView is a thin view over a **data source**. Records flow in
through one of two channels:

- **`items=[...]`** — a list of dicts (or primitives). Internally
  wrapped in a private `MemoryDataSource` that manages selection
  and CRUD. Records without an `id` are auto-numbered by their
  position in the list at construction time.
- **`datasource=...`** — a user-supplied object satisfying the
  `DataSourceProtocol` (see below). Use this for SQLite, REST,
  files, or any backing store that doesn't fit comfortably in
  memory.

### Record shape

The default `ListItem` recognizes these fields on each record:

| Field     | Purpose                                                  |
| --------- | -------------------------------------------------------- |
| `id`      | **Required.** Unique record identifier; selection,       |
|           | dragging, and CRUD all key on this.                      |
| `title`   | Main heading (top-most line, larger weight).             |
| `text`    | Body line below the title.                               |
| `caption` | Small caption line below `text`.                         |
| `icon`    | Theme-aware icon spec drawn on the left.                 |
| `badge`   | Trailing pill chip on the right.                         |

Custom row factories may consume any other fields. The widget
itself only cares about `id` (for selection bookkeeping).

### DataSourceProtocol

A `datasource=` object must provide:

```text
total_count() -> int
get_page_from_index(start, count) -> list[dict]
is_selected(record_id) -> bool
select_record(record_id) -> None
deselect_record(record_id) -> None
deselect_all() -> None
get_selected() -> list[record_id]
create_record(data) -> record_id
update_record(record_id, data) -> bool
delete_record(record_id) -> bool
reload() -> None
move_record(record_id, target_index) -> bool   # optional, used when
                                                # enable_dragging=True
```

A minimal in-memory implementation lives at
`ttkbootstrap.widgets.composites.list.listview.MemoryDataSource`
and is used automatically when you pass `items=`. The framework
also ships richer datasources under `ttkbootstrap.datasource`
(`MemoryDataSource`, `SqliteDataSource`, `FileDataSource`) — but
those extend `BaseDataSource`, whose selection API uses
`unselect_record` / `unselect_all` / no `is_selected`. ListView
calls `deselect_record` / `deselect_all` / `is_selected`, so
those classes do **not** satisfy `DataSourceProtocol` as-shipped.
See [Bugs surfaced during the docs review](#) for the open
mismatch; in the meantime, use `items=` for in-memory lists or
write a thin protocol adapter around `BaseDataSource`.

### Mutating data through the widget

The widget exposes CRUD methods that route through the data
source and refresh the visible rows:

```python
lv.insert_item({"title": "New file", "caption": "uploaded just now"})
lv.update_item(record_id=1, data={"caption": "Updated 1m ago"})
lv.delete_item(record_id=2)
lv.reload()              # re-fetch from the datasource
```

Each method emits the corresponding virtual event (see
[Events](#events)). For data driven from outside the widget
(e.g. a database row was added by another process), call
`reload()` to re-render against the current datasource state.

---

## Common options

| Option                    | Purpose                                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------------------- |
| `items`                   | Initial list of records (dicts or primitives). Mutually exclusive with `datasource`.               |
| `datasource`              | Custom `DataSourceProtocol` implementation.                                                        |
| `row_factory`             | Callable `(parent, **row_kwargs) -> Widget` that returns a custom row widget.                      |
| `selection_mode`          | `"none"` (default), `"single"`, or `"multi"`.                                                      |
| `show_selection_controls` | Show explicit checkbox/radio affordances on each row (default `False`).                            |
| `select_on_click`         | Whether clicking a row selects it. Defaults to `True` when `selection_mode != "none"`.             |
| `show_chevron`            | Show a trailing chevron on each row (purely visual).                                               |
| `enable_removing`         | Show a remove (×) button on each row; click fires `<<ItemDelete>>`.                                |
| `enable_dragging`         | Show a drag handle and enable row reordering via `move_record`.                                    |
| `striped`                 | Alternate row background colors (default `False`).                                                 |
| `striped_background`      | Surface token for the striped rows (default `"background[+1]"`).                                   |
| `show_separator`          | Draw a separator line between rows (default `True`).                                               |
| `scrollbar_visibility`    | `"always"` (default) or `"never"` (mousewheel-only).                                               |
| `enable_focus`            | Whether rows accept keyboard focus (default `True`).                                               |
| `enable_hover`            | Whether rows show a hover background (default `True`).                                             |
| `selected_background`     | Accent token used for the selected-row fill (default `"primary"`).                                 |
| `focus_color`             | Accent token for the focus indicator stripe.                                                       |
| `density`                 | `"default"` or `"compact"` — row height/padding.                                                   |

`selection_mode` controls both the visual affordance set on each
row and what `_on_item_selecting` does when a row fires its
selection event. Setting `selection_mode="single"` clears any
prior selection on each click; `"multi"` toggles. `"none"`
disables selection bookkeeping but still lets clicks fire
`<<ItemClick>>` so callers can implement custom activation.

```python
lv = ttk.ListView(
    app,
    items=data,
    selection_mode="multi",
    show_selection_controls=True,   # checkboxes
    enable_removing=True,           # × per row
    enable_dragging=True,           # drag handle per row
    striped=True,
    show_separator=False,
    scrollbar_visibility="never",   # mousewheel only
)
```

---

## Behavior

**Virtualization.** ListView measures the visible region on
`<Configure>` and builds a small pool of row widgets — one per
visible row plus a 2-row overscan. As the user scrolls, rows are
recycled (their data is replaced) rather than recreated. The
pool resizes itself when the widget is resized; row data is
fetched in pages of `visible_rows + overscan` from the
datasource's `get_page_from_index`.

**Selection.** Click semantics depend on `selection_mode`:

- `"none"` — clicks fire `<<ItemClick>>` only; no selection
  state is tracked.
- `"single"` — a click on row R deselects everything else and
  selects R; clicking the already-selected row leaves it
  selected (single-select can't be cleared by clicking again).
- `"multi"` — a click toggles R's selection without affecting
  other rows.

`show_selection_controls=True` adds a checkbox (multi) or radio
(single) on the leading edge of each row, which is the more
discoverable affordance for selection-heavy UIs.
`select_on_click=False` lets you decouple the two, e.g. show
checkboxes that drive selection while plain clicks fire
`<<ItemClick>>` for an "open" gesture.

**Keyboard navigation.** When `enable_focus=True`, the rows
participate in keyboard focus. `<Down>` and `<Up>` move focus
between rows and scroll the list to keep the focused row
visible. Selection still requires a click (or
`select_record(...)` from your code) — focus and selection are
independent states.

**Drag reordering.** `enable_dragging=True` shows a drag handle
on the left of each row and enables the drag/drop pipeline:
dragging shows a horizontal indicator at the prospective drop
position, auto-scrolls when the cursor approaches the top or
bottom edge, and on release calls `datasource.move_record(id,
target_index)`. The widget falls back to a
`get_page_from_index` + `set_data` cycle if your datasource
doesn't implement `move_record`.

**Mousewheel.** The widget binds platform-correct scroll events
on itself, the container, and every row (and recursively to
their children) — Aqua/Win get `<MouseWheel>`, X11 gets
`<Button-4>`/`<Button-5>`. Scrolls advance/retreat
`_start_index` by one row at a time.

**Visual states.** Rows reflect `selected`, `focus`, `hover`,
`disabled`, and `pressed` states through the `ListView.TFrame`
style. Striping is purely position-based — odd-indexed rows in
the pool get the `striped_background` surface — so the stripe
pattern is stable as you scroll, not tied to record IDs.

---

## Events

ListView emits the following virtual events. The payload column
shows what arrives at `event.data`; `None` means the listener
should call back into the widget (e.g. `get_selected()`) for
state.

| Event                  | When                                                  | `event.data`                                                              |
| ---------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------- |
| `<<SelectionChange>>`  | Selection set changed (click, `select_all`, `clear_selection`). | `None` — call `get_selected()`.                                |
| `<<ItemClick>>`        | A row was clicked.                                    | The clicked record (`dict`), enriched with `selected`/`focused`/`item_index`. |
| `<<ItemDelete>>`       | An item was removed via the row × button or `delete_item`. | `{'record_id': Any}` — the id of the deleted record.                |
| `<<ItemDeleteFail>>`   | The datasource raised during deletion.                | `{'record_id': Any, 'error': str}`.                                       |
| `<<ItemInsert>>`       | `insert_item(...)` succeeded.                         | `{'record': dict}` — the inserted record with its assigned id.            |
| `<<ItemUpdate>>`       | `update_item(...)` succeeded.                         | `{'record': dict}` — the partial update dict.                             |
| `<<ItemDragStart>>`    | A drag began.                                         | The dragged record + `source_index`.                                      |
| `<<ItemDrag>>`         | The drag cursor moved.                                | `{source_index, target_index, y_current, ...}`.                           |
| `<<ItemDragEnd>>`      | The drag was released.                                | `{source_index, target_index, moved, y_start, y_end, ...}`.               |

For each, an `on_*` / `off_*` helper pair is provided:

```python
lv.on_selection_changed(lambda e: print(lv.get_selected()))
lv.on_item_click(lambda e: print("clicked:", e.data["title"]))
lv.on_item_drag_end(lambda e: print(
    "moved" if e.data["moved"] else "no move",
    e.data["source_index"], "→", e.data["target_index"],
))
```

The helpers return a Tk bind ID; pass it back to `off_*` to
detach a specific listener. Note that `<<SelectionChange>>` carries
no payload — call `get_selected()` for the current selection. The
other CRUD events carry the relevant record data in `event.data`.

---

## Performance guidance

ListView's virtualization keeps render cost flat regardless of
record count, but a few patterns scale poorly:

- **Don't pass tens of thousands of records via `items=`.** The
  default `MemoryDataSource` builds an `id → index` map at
  `set_data` time and rebuilds it on every delete or move — fine
  for thousands, painful for hundreds of thousands. Move to a
  `datasource=` backed by SQLite or an external store for very
  large sets.
- **`select_all()` loads every record.** It calls
  `get_page_from_index(0, total)` and iterates, so the cost
  scales with `total_count()`. Avoid wiring it to a button on a
  list of 10⁵+ records, or implement a datasource-side bulk
  select.
- **Custom `row_factory` widgets are built once per visible
  slot, not once per record.** Heavy per-row construction
  amortizes well (the pool size is small), but heavy
  `update_data` work runs on every scroll tick — keep it cheap.
- **Striped backgrounds are applied per pool slot, not per
  record.** Switching `striped` or `striped_background` after
  construction iterates the pool, which is bounded by visible
  rows; cheap.

The widget refreshes its visible rows on every CRUD method,
selection event, and `<Configure>`. If you're driving many
updates from outside the widget (e.g. a streaming feed), batch
them at the datasource level and call `reload()` once per
batch.

---

## When should I use ListView?

Use `ListView` when:

- you need a **flat list** of records with rich rows (icon,
  title, body text, caption, badge)
- the list may grow large (hundreds to tens of thousands of
  rows) and rendering cost must stay constant
- you want built-in selection, keyboard navigation, drag
  reordering, or per-row remove

Prefer:

- [TableView](tableview.md) — when records are strongly
  column-shaped and users compare values across rows or sort by
  column
- [TreeView](treeview.md) — when records nest hierarchically
  (folders, categories, parent/child relationships)
- A simple `Frame` of `Label`s — for short, static lists
  (handful of rows, no selection) where the virtualization
  overhead isn't worth it

---

## Related widgets

- **`ListItem`** — the default row template ListView builds from
- **[TableView](tableview.md)** — column-aligned records
- **[TreeView](treeview.md)** — hierarchical records
- **[Scrollbar](../layout/scrollbar.md)** — the scrollbar
  ListView composes
- **[ScrollView](../layout/scrollview.md)** — generic scrolling
  container for non-record content

---

## Reference

- **API reference:** `ttkbootstrap.ListView`
- **Related guides:**
  [Tables and lists](../../guides/tables-and-lists.md),
  [DataSource](../../guides/datasource.md),
  [Design System](../../design-system/index.md)
