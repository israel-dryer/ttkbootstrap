---
title: TableView
icon: fontawesome/solid/table
---

# TableView

`TableView` displays tabular data with sorting, filtering, and paging.

In ttkbootstrap v2, `TableView` is a composite widget built on `TreeView` and `SqliteDataSource` that provides:

- **Data-driven display** backed by in-memory SQLite
- **Sorting** (single or multiple columns)
- **Filtering** with column-specific filters
- **Paging** (standard pagination or virtual scrolling)
- **Search** with multiple modes (equals, contains, starts with, ends with, SQL)
- **Editing** with add/update/delete dialogs
- **Exporting** to CSV and XLSX
- **Grouping** by column
- **Row alternation** (striped rows)
- **Context menus** for headers and rows
- **Events** for selection, clicks, and data changes

Use `TableView` for data grids, admin panels, or any tabular display with built-in data management.

> _Image placeholder:_
> `![TableView](../_img/widgets/tableview/overview.png)`
> Suggested shot: table with sorting, filtering, and paging controls.

---

## Basic usage

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import SqliteDataSource

app = ttk.App()

data = [
    {"name": "Alice", "email": "alice@example.com", "role": "Admin"},
    {"name": "Bob", "email": "bob@example.com", "role": "User"},
    {"name": "Charlie", "email": "charlie@example.com", "role": "User"},
]

table = ttk.TableView(
    app,
    columns=[
        {"key": "name", "text": "Name"},
        {"key": "email", "text": "Email"},
        {"key": "role", "text": "Role"},
    ],
    rows=data,
)
table.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

---

## Common options

### `columns`

Define columns with text labels, keys, widths, and alignment.

```python
columns = [
    {"key": "id", "text": "ID", "width": 50},
    {"key": "name", "text": "Name", "width": 150},
    {"key": "email", "text": "Email", "width": 200},
    {"key": "role", "text": "Role", "width": 100},
]

table = ttk.TableView(app, columns=columns, rows=data)
```

Column options:
- `key`: Data field name
- `text`: Display heading
- `width`: Column width in pixels
- `minwidth`: Minimum width
- `anchor`: Text alignment (`w`, `center`, `e`)

### `rows` or `datasource`

Provide data as a list of dictionaries or use a custom `SqliteDataSource`.

```python
# Using rows
table = ttk.TableView(app, columns=columns, rows=data)

# Using datasource
datasource = SqliteDataSource(data=data, page_size=50)
table = ttk.TableView(app, columns=columns, datasource=datasource)
```

### `paging`

Control pagination behavior.

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    paging={
        "mode": "standard",  # or "virtual"
        "page_size": 50,
        "xscroll": True,
        "yscroll": True,
    },
)
```

Paging options:

- `mode`: `"standard"` (pagination) or `"virtual"` (virtual scrolling)
- `page_size`: Rows per page
- `page_index`: Starting page (0-based)
- `cache_size`: Number of pages to cache
- `xscroll`: Show horizontal scrollbar
- `yscroll`: Show vertical scrollbar

Disable paging:

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    paging={"enabled": False},
)
```

### `selection`

Control row selection behavior.

```python
# Single selection (default)
table = ttk.TableView(app, columns=columns, rows=data, selection={"mode": "single"})

# Multiple selection
table = ttk.TableView(app, columns=columns, rows=data, selection={"mode": "multiple"})

# No selection
table = ttk.TableView(app, columns=columns, rows=data, selection={"mode": "none"})
```

---

## Sorting

### Enable sorting

```python
# Single column sorting (default)
table = ttk.TableView(app, columns=columns, rows=data, sorting="single")

# Multiple column sorting
table = ttk.TableView(app, columns=columns, rows=data, sorting="multiple")

# Disable sorting
table = ttk.TableView(app, columns=columns, rows=data, sorting="none")
```

Users can click column headers to sort. With `sorting="multiple"`, hold Shift to sort by multiple columns.

---

## Filtering

### Enable filtering

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    filtering={
        "enabled": True,
        "header_menu_filtering": True,
        "row_menu_filtering": True,
    },
)
```

Right-click column headers to access filter options.

### Clear filters

```python
table.clear_filter()
```

---

## Search

### Enable search bar

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    search={
        "enabled": True,
        "mode": "standard",  # or "advanced"
        "event": "enter",    # or "input"
    },
)
```

Search options:

- `mode`: `"standard"` (simple search) or `"advanced"` (with search mode dropdown)
- `event`: `"enter"` (search on Enter key) or `"input"` (search on every keystroke)

Search modes (in advanced mode):

- EQUALS
- CONTAINS
- STARTS WITH
- ENDS WITH
- SQL

---

## Editing

### Enable add/update/delete

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    editing={
        "adding": True,
        "updating": True,
        "deleting": True,
        "form": {},  # Optional form configuration
    },
)
```

When enabled, toolbar buttons appear for adding, editing, and deleting rows.

### Get selected records

```python
selected = table.get_selected_records()
for record in selected:
    print(record)
```

---

## Exporting

### Enable export

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    exporting={
        "enabled": True,
        "formats": ["csv", "xlsx"],
        "export_all_mode": "all",  # or "page"
        "allow_export_selected": True,
    },
)
```

When enabled, an export button appears in the toolbar.

---

## Grouping

### Enable grouping

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    allow_grouping=True,
)
```

Right-click a column header and select "Group by Column" to group rows by that column.

---

## Row alternation

### Enable striped rows

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    row_alternation={
        "enabled": True,
        "color": "background[+1]",
    },
)
```

Note: Row alternation is disabled when grouping is active.

---

## Context menus

### Control context menus

```python
# Enable all context menus (default)
table = ttk.TableView(app, columns=columns, rows=data, context_menus="all")

# Enable only header context menus
table = ttk.TableView(app, columns=columns, rows=data, context_menus="headers")

# Enable only row context menus
table = ttk.TableView(app, columns=columns, rows=data, context_menus="rows")

# Disable all context menus
table = ttk.TableView(app, columns=columns, rows=data, context_menus="none")
```

---

## Column options

### Auto-width columns

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    column_auto_width=True,
)
```

Columns automatically size to fit visible content.

### Minimum column width

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    column_min_width=60,
)
```

### Show column chooser

```python
table = ttk.TableView(
    app,
    columns=columns,
    rows=data,
    show_column_chooser=True,
)
```

Adds a button to show/hide columns.

---

## Status display

### Show table status

```python
# Show status (default)
table = ttk.TableView(app, columns=columns, rows=data, show_table_status=True)

# Hide status
table = ttk.TableView(app, columns=columns, rows=data, show_table_status=False)
```

The status area shows active filters, sort order, and pagination controls.

---

## Events

### `on_selection_changed(...)` and `off_selection_changed(...)`

Triggered when row selection changes.

```python
def handle_selection(event):
    data = event.data
    print(f"Selected {len(data['records'])} records")
    print(f"IIDs: {data['iids']}")

table.on_selection_changed(handle_selection)
```

To unbind:

```python
bind_id = table.on_selection_changed(handle_selection)
table.off_selection_changed(bind_id)
```

Event data:
- `records`: List of selected record dictionaries
- `iids`: List of selected item IDs

### `on_row_click(...)` and `off_row_click(...)`

Triggered when a row is clicked.

```python
def handle_click(event):
    data = event.data
    print(f"Clicked: {data['record']}")
    print(f"IID: {data['iid']}")

table.on_row_click(handle_click)
```

To unbind:

```python
bind_id = table.on_row_click(handle_click)
table.off_row_click(bind_id)
```

Event data:
- `record`: The clicked record dictionary
- `iid`: The item ID

### `on_row_double_click(...)` and `off_row_double_click(...)`

Triggered when a row is double-clicked.

```python
def handle_double_click(event):
    data = event.data
    print(f"Double-clicked: {data['record']}")

table.on_row_double_click(handle_double_click)
```

To unbind:

```python
bind_id = table.on_row_double_click(handle_double_click)
table.off_row_double_click(bind_id)
```

### `on_row_right_click(...)` and `off_row_right_click(...)`

Triggered when a row is right-clicked.

```python
def handle_right_click(event):
    data = event.data
    print(f"Right-clicked: {data['record']}")

table.on_row_right_click(handle_right_click)
```

To unbind:

```python
bind_id = table.on_row_right_click(handle_right_click)
table.off_row_right_click(bind_id)
```

### Data modification events

Use `on_row_inserted(...)`, `on_row_updated(...)`, `on_row_deleted(...)`, and `on_row_moved(...)` methods.

```python
def handle_insert(event):
    print(f"Inserted: {event.data['records']}")

def handle_update(event):
    print(f"Updated: {event.data['records']}")

def handle_delete(event):
    print(f"Deleted: {event.data['records']}")

def handle_move(event):
    print(f"Moved: {event.data['records']}")

table.on_row_inserted(handle_insert)
table.on_row_updated(handle_update)
table.on_row_deleted(handle_delete)
table.on_row_moved(handle_move)
```

Each has a corresponding `off_*` method:

```python
table.off_row_inserted(bind_id)
table.off_row_updated(bind_id)
table.off_row_deleted(bind_id)
table.off_row_moved(bind_id)
```

---

## Methods

### `reload()`

Refresh the table from the datasource.

```python
table.reload()
```

### `clear_filter()`

Remove all active filters.

```python
table.clear_filter()
```

### `get_selected_records()`

Get the currently selected records.

```python
records = table.get_selected_records()
```

### Access the datasource

```python
datasource = table.datasource

# Get all data
all_data = datasource.get_all()

# Add records
datasource.insert([{"name": "Dave", "email": "dave@example.com", "role": "User"}])

# Update the table
table.reload()
```

---

## When should I use TableView?

Use `TableView` when:

- building data grids with sorting, filtering, and paging
- creating admin panels or management interfaces
- displaying database query results
- you need built-in editing and exporting

Prefer other widgets when:

- **TreeView** — for simple tables without filtering/paging features
- **SelectBox** — for dropdown selection from a list
- **Form** — for data entry with validation

---

## Related widgets

- **TreeView** — low-level table/tree control
- **Form** — data entry with validation
- **SelectBox** — dropdown selection