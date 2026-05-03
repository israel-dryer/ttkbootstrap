---
title: TableView
---

# TableView

`TableView` is a **sortable, filterable, paginated grid** for flat
tabular records. Rows live in a SQLite-backed data source — an
in-memory database is created automatically when you pass `rows=` —
and the widget renders one page at a time into a styled `TreeView`.
Headers double as sort triggers, a search bar drives WHERE-clause
filtering, an optional column-level filter dialog narrows the page
down to chosen values, and CRUD operations open a generated
[FormDialog](../dialogs/formdialog.md) when editing is enabled.

Unlike [ListView](listview.md) (a virtualized list of rich rows) and
[TreeView](treeview.md) (the underlying hierarchical
control), TableView is built around **column-aligned scanning and
comparison**: heading clicks sort, status labels show the active
filter and sort, and the footer pager moves through pages of
configurable size. It is the right choice when the dataset is
multi-column, uniform, and likely to grow past what fits on screen.

<figure markdown>
![tableview](../../assets/dark/widgets-tableview.png#only-dark)
![tableview](../../assets/light/widgets-tableview.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

tv = ttk.TableView(
    app,
    columns=["Name", "Status", "Owner"],
    rows=[
        ("Quarterly report", "Ready",   "Alice"),
        ("Cover photo",      "Pending", "Bob"),
        ("Theme song",       "Ready",   "Carol"),
    ],
)
tv.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

`columns=` accepts plain strings (used as both heading and key) or
dicts (`{"text": ..., "key": ..., "width": ...}`). `rows=` accepts a
list of dicts or row-shaped sequences — sequences are zipped against
`columns` in order. The widget loads the data into an in-memory
`SqliteDataSource` and renders the first page.

---

## Data model

TableView is a thin view over a `SqliteDataSource`. Records flow in
through one of two channels:

- **`rows=[...]`** — a list of dicts (or row-shaped sequences). The
  widget creates an in-memory SQLite table and writes the rows into
  it at construction time.
- **`datasource=...`** — a pre-built `SqliteDataSource` (or any
  source that exposes the same `set_filter` / `set_sort` /
  `get_page` / `total_count` / `create_record` / `update_record` /
  `delete_record` surface). Use this when the table backs an
  on-disk SQLite file or a long-lived in-memory store shared with
  other widgets.

### Column definitions

Each entry in `columns=` is either a string (used verbatim as the
heading text **and** the record key) or a dict with these fields:

| Field           | Purpose                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| `text`          | Heading text shown above the column.                                                                 |
| `key`           | Record-dict key. Defaults to `text` if omitted.                                                      |
| `width`         | Initial column width in pixels (default `120`).                                                      |
| `minwidth`      | Minimum width when the user resizes (default `column_min_width`, fallback `40`).                     |
| `anchor` / `align` | Cell anchor (`"w"`, `"center"`, `"e"`). Inferred from data type if omitted.                       |
| `dtype` / `type`   | SQL/Python type hint used for anchor inference and the edit-form editor.                          |
| `editor`        | Editor widget class to use in the edit form for this column.                                         |
| `editor_options`| Kwargs passed to the editor.                                                                         |
| `readonly`      | Make the column non-editable in the form (default `False`).                                         |
| `required`      | Mark the field required in the form (default `False`).                                              |

Numeric columns auto-anchor right (`"e"`); text columns anchor left
(`"w"`). When dtype is omitted, the widget samples up to 20 rows to
infer it.

### Mutating data through the widget

```python
tv.insert_rows([{"Name": "Receipts.zip", "Status": "Ready", "Owner": "Alice"}])
tv.update_rows([{"id": 7, "Status": "Done"}])     # id required
tv.delete_rows([7])                                # ids or full record dicts
tv.set_data(new_rows)                              # replace entire dataset
```

Each method routes through the datasource, refreshes the visible
page, and emits the matching virtual event (see [Events](#events)).
External callers updating the underlying SQLite store directly
should call `tv.go_to_page(tv._current_page)` (or any pager method)
afterwards to invalidate the page cache.

---

## Common options

| Option                      | Purpose                                                                                                  |
| --------------------------- | -------------------------------------------------------------------------------------------------------- |
| `columns`                   | Column definitions (list of strings or dicts).                                                           |
| `rows`                      | Initial data (list of dicts or sequences). Loaded into a fresh in-memory `SqliteDataSource`.             |
| `datasource`                | Pre-built `SqliteDataSource`. Mutually exclusive with auto-load via `rows=`.                             |
| `selection_mode`            | `"none"`, `"single"` (default), or `"multi"`. Maps to ttk `selectmode` `"none"` / `"browse"` / `"extended"`. |
| `allow_select_all`          | Allow `select_all()` to select every visible row (default `True`).                                       |
| `sorting_mode`              | `"single"` (default) or `"none"` to disable header-click sorting.                                        |
| `enable_search`             | Show the toolbar search box (default `True`).                                                            |
| `search_mode`               | `"standard"` or `"advanced"` (adds a mode dropdown for EQUALS / CONTAINS / STARTS WITH / ENDS WITH / SQL). |
| `search_trigger`            | `"enter"` (default) or `"input"` (live search on every keystroke).                                       |
| `enable_header_filtering`   | Show "Filter…" in the column header context menu (default `True`).                                       |
| `enable_row_filtering`      | Show filter actions in the row context menu (default `True`).                                            |
| `paging_mode`               | `"standard"` (pager footer) or `"virtual"` (lazy-append on scroll past 85 %).                            |
| `page_size`                 | Rows per page (default `25`).                                                                            |
| `page_cache_size`           | Pages held in the LRU cache (default `3`).                                                               |
| `show_vscrollbar`           | Vertical scrollbar (default `True`).                                                                     |
| `show_hscrollbar`           | Horizontal scrollbar; columns become natural-width when enabled (default `False`).                       |
| `enable_adding`             | Show an Add button in the toolbar (default `False`).                                                     |
| `enable_editing`            | Open an edit `FormDialog` on row double-click and via the row menu (default `False`).                    |
| `enable_deleting`           | Add Delete to the row menu and the edit dialog (default `False`).                                        |
| `form_options`              | Kwargs forwarded to the generated `FormDialog` (`col_count`, `min_col_width`, `scrollable`, `resizable`). |
| `enable_exporting`          | Show an Export dropdown in the toolbar (default `False`). See [Events](#events) for the wiring caveat.   |
| `export_scope`              | `"page"` (default) or `"all"`.                                                                           |
| `striped`                   | Alternate row background colors (default `False`).                                                       |
| `striped_background`        | Surface token for the alt rows (default `"background[+1]"`).                                             |
| `allow_grouping`            | Show "Group by this column" in header context menu (default `False`).                                    |
| `show_table_status`         | Show filter / sort / group status labels in the footer (default `True`).                                 |
| `show_column_chooser`       | Show a column-chooser button in the toolbar (default `False`).                                           |
| `context_menus`             | `"none"`, `"headers"`, `"rows"`, or `"all"` (default).                                                   |
| `column_auto_width`         | Resize columns to fit the widest visible cell on each page load (default `False`).                       |
| `column_min_width`          | Global minimum column width in pixels (default `40`).                                                    |

```python
tv = ttk.TableView(
    app,
    columns=[
        {"text": "Name",   "key": "name",   "width": 200},
        {"text": "Status", "key": "status", "width": 120},
        {"text": "Amount", "key": "amount", "dtype": "REAL", "width": 100},
    ],
    rows=records,
    selection_mode="multi",
    enable_adding=True,
    enable_editing=True,
    enable_deleting=True,
    striped=True,
    paging_mode="virtual",
    page_size=50,
)
```

---

## Behavior

**Header sorting.** A left-click on any column heading toggles its
sort order ascending → descending. Sort state is **single-column** —
clicking a different heading replaces the current sort. The active
sort column is shown with a chevron icon in the heading. Disable
with `sorting_mode="none"`.

**Search.** The toolbar search box generates a SQL `WHERE` fragment
across all string columns. Standard mode uses `LIKE '%term%'`
(CONTAINS) by default; advanced mode adds a SelectBox letting the
user pick **EQUALS**, **CONTAINS**, **STARTS WITH**, **ENDS WITH**,
or **SQL** (in which case the entered text is used verbatim as the
WHERE clause). With `search_trigger="enter"` the filter applies on
Return; `"input"` re-runs on every keystroke.

**Column filtering.** When `allow_grouping` or
`enable_header_filtering` is on, right-clicking a header offers
"Filter…", which opens a [FilterDialog](../dialogs/filterdialog.md)
populated with the column's distinct values. Selecting a subset
narrows the page to those rows.

**Paging.** Standard mode shows a footer pager (« ‹ › ») and a
"Page N of M" label that doubles as a Go-To-Page entry. Virtual
mode hides the pager and lazily appends the next page when the
scroll position passes 85 % of the visible region — useful for
streaming or very large datasets where the user expects continuous
scrolling rather than discrete pages.

**Selection.** Click semantics follow ttk:

- `"none"` — clicks fire `<<RowClick>>` only; selection state is
  not tracked.
- `"single"` — a click on row R replaces any prior selection.
- `"multi"` — Ctrl+click toggles, Shift+click extends, plain
  click replaces.

`select_all()` selects every visible row in the current page.
`deselect_all()` clears the selection.

**Editing.** When `enable_editing=True`, a row double-click opens a
`FormDialog` populated from the column definitions; submitting
calls `update_record` on the datasource, refreshes the page, and
fires `<<RowUpdate>>`. When `enable_adding=True`, a toolbar Add
button opens the same dialog with empty fields. When
`enable_deleting=True`, a Delete button is added to the edit
dialog and a Delete entry is added to the row context menu — both
fire `<<RowDelete>>`. Per-column editing is customized via the
`editor` / `editor_options` / `readonly` / `required` keys on each
column dict.

**Grouping.** `allow_grouping=True` adds "Group by" to the header
menu; `set_grouping(key)` programmatically groups by a column,
inserting parent rows for each distinct value. `expand_all()` /
`collapse_all()` operate on group rows; `clear_grouping()` flattens
the view.

**Hide / show.** `hide_columns([i, j])` removes columns from the
displayed set without dropping the underlying data;
`unhide_columns([i, j])` restores them. `hide_rows([iid])` /
`unhide_rows()` work the same way for rows. `show_column_chooser=True`
adds a toolbar button that opens a dialog for toggling visibility.

**Context menus.** `context_menus="all"` (default) wires both
header and row right-click menus. The header menu offers sorting,
filtering, hiding, and grouping; the row menu offers sort by
selection, filter by value, move up/down/top/bottom, edit, and
delete.

**Status labels.** With `show_table_status=True` (default), the
footer displays `Filter: …`, `Sort: …`, and `Group: …` labels that
reflect the current state, plus the page entry / page count.

---

## Events

| Event                       | When                                                    | `event.data`                                              |
| --------------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| `<<SelectionChange>>`       | The Treeview selection changed.                         | `{"records": list[dict], "iids": list[str]}`              |
| `<<RowClick>>`              | A row was left-clicked (button release in the rows region). | `{"record": dict, "iid": str}`                       |
| `<<RowDoubleClick>>`        | A row was double-clicked.                               | `{"record": dict, "iid": str}`                            |
| `<<RowRightClick>>`         | A row was right-clicked (before the menu opens).        | `{"record": dict, "iid": str}`                            |
| `<<RowInsert>>`             | `insert_rows(...)` succeeded, or the Add form was confirmed. | `{"records": list[dict]}`                            |
| `<<RowUpdate>>`             | `update_rows(...)` succeeded, or the Edit form was confirmed. | `{"records": list[dict]}`                           |
| `<<RowDelete>>`             | `delete_rows(...)` succeeded, the Delete row menu fired, or Delete was clicked in the edit form. | `{"records": list[dict]}` |
| `<<RowMove>>`               | A row was reordered via `move_rows(...)` or the row menu's move-up / -down / -top / -bottom. | `{"records": list[dict]}` |

For each event there's a paired `on_*` / `off_*` helper:

```python
tv.on_selection_changed(lambda e: print(e.data["records"]))
tv.on_row_double_click(lambda e: print("dbl:", e.data["record"]))
tv.on_row_inserted(lambda e: print("inserted:", e.data["records"]))
```

The `on_*` helpers return a Tk bind ID; pass it to `off_*` to detach
a specific listener.

!!! warning "Export events fire on the inner Treeview, not on `self`"
    `enable_exporting=True` adds an Export dropdown that emits
    `<<TableViewExportAll>>`, `<<TableViewExportSelection>>`, or
    `<<TableViewExportPage>>` (carrying the row list as
    `event.data`). These events are generated on
    **`tv._tree`** (the internal `TreeView`) — not on `tv` — and
    there are no `on_export_*` helpers. To consume them today,
    bind to the private inner widget; a public API is pending.

---

## Performance guidance

TableView fetches one page at a time and caches up to
`page_cache_size` recent pages, so flipping between adjacent pages
is cheap. A few patterns to watch:

- **Use virtual paging for streaming or "infinite-scroll" UX.**
  `paging_mode="virtual"` appends rows on scroll instead of
  swapping pages, which feels more natural for log-style data.
  Standard paging is better when users navigate by page number or
  the dataset is fixed-size.
- **Avoid `column_auto_width=True` on wide datasets.** It iterates
  the visible page and measures each cell with `tkfont.Font.measure`
  on every page load — fine for tens of columns and dozens of rows,
  expensive for hundreds of columns or large pages.
- **Batch external mutations through `set_data(rows)`.** Calling
  `insert_rows` / `update_rows` in a tight loop fires a virtual
  event and a page reload per call. If you're loading a thousand
  rows from outside the widget, replace the dataset in one shot.
- **Cache invalidation has a cost.** Every CRUD call clears the
  page cache and re-fetches the current page. The cache is sized
  for navigation, not for hot-loop mutations.

For datasets large enough that the search/filter SQL itself
becomes the bottleneck, supply a custom `datasource=` whose
backing table has indexes on the searched columns.

!!! danger "SQL injection contract"
    `set_filters(where)`, the advanced search "SQL" mode, and
    `tv.set_sorting(key)` interpolate their inputs **directly**
    into SQL. The framework does not parameterize them — they're
    intended for trusted code paths only. Never wire a free-form
    user input into these APIs without sanitization.

---

## When should I use TableView?

Use `TableView` when:

- records are **strongly column-shaped** and users need to scan,
  sort, or filter by column
- the dataset is large enough to need paging, virtual scrolling, or
  search
- you want built-in CRUD via a generated form, with row-level
  delete and column-level filtering

Prefer:

- [ListView](listview.md) — when each record is best shown as a
  rich row (icon, title, body text) rather than a row of cells, or
  when the data is flat and the user reads top-to-bottom
- [TreeView](treeview.md) — when records nest
  hierarchically (folder structures, parent/child relationships).
  TableView is built on TreeView but exposes only flat rows plus
  optional grouping.
- A simple `Frame` of `Label`s — for short, static tabular content
  (handful of rows, no sorting or filtering) where the toolbar and
  pager would just be noise.

---

## Related widgets

- **[ListView](listview.md)** — virtualized flat list with rich
  row layouts
- **[TreeView](treeview.md)** — the underlying
  hierarchical tree widget TableView builds on
- **[FormDialog](../dialogs/formdialog.md)** — the dialog
  TableView opens for add/edit
- **[FilterDialog](../dialogs/filterdialog.md)** — the dialog
  used by per-column "Filter…"
- **[ContextMenu](../actions/contextmenu.md)** — the header
  and row right-click menus

---

## Reference

- **API reference:** `ttkbootstrap.TableView`
- **Related guides:**
  [Tables and lists](../../guides/tables-and-lists.md),
  [DataSource](../../guides/datasource.md),
  [Design System](../../design-system/index.md)
