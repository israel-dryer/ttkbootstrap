---
title: DataSource
---

# DataSource

A **DataSource** is the data layer behind ttkbootstrap's data-aware
widgets. It owns the records — loading, filtering, sorting, paging,
mutating, and tracking selection — while the widget owns rendering and
input. The same `ListView` or `TableView` can be backed by an
in-memory store, a SQLite database, or a CSV file by swapping the
DataSource and nothing else.

This guide covers what the abstraction does, the three built-in
implementations, the methods every DataSource exposes, and how to
build a custom one.

---

## Why a DataSource

Without a DataSource, a list or table widget mixes three concerns:
where the data lives, how it is filtered and sorted, and how it is
drawn. That mix is fine for a 50-row demo and painful for anything
larger — switching from a Python list to a database means rewriting
the widget code.

A DataSource separates those concerns:

- **Storage** — memory, SQLite, file, REST API, anything you can
  read records from — is the DataSource's responsibility.
- **View configuration** — pagination, filter, sort — is set on the
  DataSource and applied uniformly regardless of backend.
- **Rendering and selection input** — is the widget's responsibility.

The widget calls a fixed set of methods (`get_page`, `total_count`,
`update_record`, `select_record`, ...) and the DataSource handles
storage. Switching backends is a one-line change.

---

## Built-in implementations

| Class | Storage | Persists across runs | Filter/sort engine |
|-------|---------|----------------------|--------------------|
| `MemoryDataSource` | Python list in memory | No | Python predicates |
| `SqliteDataSource` | SQLite file or `:memory:` | Yes (when given a file path) | Native SQL |
| `FileDataSource` | CSV / JSON / JSONL on disk | Read-only by default | Inherits MemoryDataSource |

All three implement the same `DataSourceProtocol`, so application
code that takes a DataSource works with any of them.

---

## MemoryDataSource

Stores records as a list of dictionaries in process memory. Use it
for small to medium datasets (up to a few tens of thousands of
records) where data does not need to survive an application restart.

```python
from ttkbootstrap.datasource import MemoryDataSource

ds = MemoryDataSource(page_size=20)

ds.set_data([
    {"name": "Alice", "age": 30, "department": "Engineering"},
    {"name": "Bob", "age": 25, "department": "Sales"},
    {"name": "Charlie", "age": 35, "department": "Engineering"},
])

page = ds.get_page(0)  # first 20 records (or fewer if total < 20)
```

`set_data` accepts either a sequence of dictionaries or a sequence of
primitives. Primitives are auto-wrapped as `{"text": str(value)}`.
Each loaded record is given an integer `id` (auto-assigned if
missing) and a `selected` field (`0` by default).

!!! link "API Reference"
    See [MemoryDataSource](../reference/data/MemoryDataSource.md).

---

## SqliteDataSource

Stores records in a SQLite database — either a file on disk or an
in-memory database. Use it when data must persist across runs, when
the dataset is too large for in-memory storage, or when you want
SQL-native filter and sort performance.

```python
from ttkbootstrap.datasource import SqliteDataSource

# File-backed: created automatically if it does not exist
ds = SqliteDataSource("employees.db", page_size=50)

# Or in-memory (the default), for SQL semantics without persistence
ds = SqliteDataSource(":memory:", page_size=50)

ds.set_data([
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
])

ds.set_filter("age >= 25")
ds.set_sort("name ASC")
page = ds.get_page(0)
```

`set_data` infers the table schema from the first record, drops any
existing table, and bulk-inserts the rows. Subsequent
`create_record` / `update_record` / `delete_record` calls go through
SQL `INSERT` / `UPDATE` / `DELETE`. The `id` column is set as the
primary key.

!!! warning "Filter/sort fragments are interpolated"
    `set_filter` and `set_sort` paste their string argument directly
    into the generated SQL. Treat them as author-controlled query
    fragments, not as a place to put end-user input. For
    user-supplied filter terms, build the WHERE clause yourself with
    parameterized queries against `ds.conn`.

!!! link "API Reference"
    See [SqliteDataSource](../reference/data/SqliteDataSource.md).

---

## FileDataSource

Loads records from a CSV, TSV, JSON, or JSONL file. Inherits from
`MemoryDataSource`, so once loaded it behaves identically — the
difference is the loading strategy and the column transformation
pipeline.

```python
from ttkbootstrap.datasource import FileDataSource

ds = FileDataSource("employees.csv", page_size=20)
ds.load()                  # parse the file once
page = ds.get_page(0)
```

### Loading strategies

`FileDataSource` chooses a loading strategy based on file size, or
you can pin one explicitly:

| Strategy | Behavior |
|----------|----------|
| `"eager"` | Parse the entire file into memory upfront. |
| `"chunked"` | Load in batches (good for medium files; supports progress callbacks). |
| `"lazy"` | Re-parse the file on each page request (smallest memory footprint). |
| `"hybrid"` | Index in memory, fetch records on demand. |
| `"auto"` | Pick a strategy from estimated row count (default). |

Loading and column-transformation behavior are configured through
`FileSourceConfig`:

```python
from ttkbootstrap.datasource import FileDataSource, FileSourceConfig

config = FileSourceConfig(
    loading_strategy="lazy",
    encoding="utf-8",
    column_renames={"emp_id": "id"},
    column_types={"age": int},
)

ds = FileDataSource("large_file.csv", config=config)
ds.load()
```

!!! link "API Reference"
    See [FileDataSource](../reference/data/FileDataSource.md) and
    [FileSourceConfig](../reference/data/FileSourceConfig.md).

---

## Filtering

Filters use a SQL-like WHERE syntax. `set_filter` replaces the
current filter; passing the empty string clears it.

```python
ds.set_filter("age > 30")
ds.set_filter("department = 'Engineering'")
ds.set_filter("name CONTAINS 'son'")
ds.set_filter("age >= 25 AND department = 'Sales'")
ds.set_filter("")   # clear
```

Supported operators (note: spelling is singular — `set_filter`, not
`set_filters`):

| Operator | Example |
|----------|---------|
| `=`, `!=` | `status = 'active'` |
| `>`, `>=`, `<`, `<=` | `age >= 18` |
| `CONTAINS` | `name CONTAINS 'john'` |
| `STARTSWITH` | `email STARTSWITH 'admin'` |
| `ENDSWITH` | `file ENDSWITH '.txt'` |
| `LIKE` | `name LIKE 'J%'` (`%` = any chars, `_` = one char) |
| `IN` | `status IN ('active', 'pending')` |
| `AND`, `OR` | `age > 25 AND active = true` |

`MemoryDataSource` parses the WHERE clause into a Python predicate
and applies it on every page request. `SqliteDataSource` passes the
fragment through to SQL — meaning the same syntax works, but
`SqliteDataSource` also accepts any expression valid in a SQLite
WHERE clause.

`total_count()` reflects the filtered row count, not the underlying
table size.

---

## Sorting

`set_sort` accepts a SQL-like ORDER BY clause. Multi-column sorts
are comma-separated.

```python
ds.set_sort("name ASC")
ds.set_sort("age DESC")
ds.set_sort("department ASC, salary DESC")
ds.set_sort("")   # clear
```

`MemoryDataSource` performs a stable sort on the in-memory list
honoring the columns in order. `SqliteDataSource` passes the clause
to `ORDER BY` directly.

---

## Pagination

Pages are zero-indexed and `page_size` records wide:

```python
# Set page size at construction
ds = MemoryDataSource(page_size=25)

# Random access — also updates the current page
records = ds.get_page(0)
records = ds.get_page(2)

# Sequential navigation — uses the internal cursor
records = ds.next_page()
records = ds.prev_page()

# Bounds checks
if ds.has_next_page():
    ds.next_page()

# Total record count, respecting the active filter
total = ds.total_count()

# Index-based access (used by virtualized widgets)
slice_records = ds.get_page_from_index(start_index=10, count=5)
```

`next_page()` and `prev_page()` advance an internal cursor;
`get_page(n)` jumps to page `n` and updates that cursor. Pages
beyond the end return an empty list — they do not raise.
`get_page_from_index` ignores `page_size` entirely and is the
right call for widgets that virtualize their own row range
(`ListView` uses it for windowed scrolling).

---

## CRUD operations

```python
# Create — returns the new record's id
new_id = ds.create_record({
    "name": "Diana",
    "age": 28,
    "department": "Marketing",
})

# Read — returns None if not found
record = ds.read_record(record_id=new_id)
if record:
    print(record["name"])

# Update — returns False if not found
ok = ds.update_record(record_id=new_id, updates={"age": 29})

# Delete — returns False if not found
ok = ds.delete_record(record_id=new_id)
```

The method names are `create_record`, `read_record`,
`update_record`, `delete_record` — there is no `insert_record` or
`get_data` alias.

---

## Selection

Each record carries a `selected` flag (`0` or `1`). The DataSource
provides methods to flip that flag and to enumerate the selected
set:

```python
# Single record
ds.select_record(record_id=1)
ds.unselect_record(record_id=1)

# Bulk
ds.select_all()
ds.select_all(current_page_only=True)
ds.unselect_all()
ds.unselect_all(current_page_only=True)

# Inspect
selected = ds.get_selected()           # list of record dicts
count = ds.selected_count()            # int

# Get only the selected rows on a specific page
page_of_selected = ds.get_selected(page=0)
```

The negative method is `unselect_*`, not `deselect_*`.

---

## CSV export

Both `MemoryDataSource` and `SqliteDataSource` can write the current
records out to CSV:

```python
ds.export_to_csv("all_data.csv")                       # all records
ds.export_to_csv("selected.csv", include_all=False)    # only selected
```

Filter and sort do *not* affect export — `export_to_csv` writes the
underlying records, not the filtered/sorted view.

---

## Connecting to a widget

Both `ListView` and `TableView` accept a `datasource=` keyword
argument:

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import MemoryDataSource

app = ttk.App()

ds = MemoryDataSource(page_size=20)
ds.set_data([
    {"name": "Alice", "role": "Developer"},
    {"name": "Bob", "role": "Designer"},
])

listview = ttk.ListView(app, datasource=ds)
listview.pack(fill="both", expand=True)

app.mainloop()
```

`TableView` is hard-wired to a SQLite-backed source (it uses
`SqliteDataSource` for its filter/sort/group features). If you do
not pass one, it constructs an in-memory SQLite source for you:

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import SqliteDataSource

app = ttk.App()

ds = SqliteDataSource("inventory.db", page_size=50)
ds.set_data([
    {"sku": "A001", "name": "Widget", "qty": 12},
    {"sku": "A002", "name": "Gadget", "qty": 7},
])

table = ttk.TableView(app, datasource=ds)
table.pack(fill="both", expand=True)

app.mainloop()
```

When the application changes filter, sort, or pages on the
DataSource, the widget needs to be told to re-read. `ListView` and
`TableView` both expose refresh methods (`reload()`, `refresh()`) —
see [Tables and lists](tables-and-lists.md) for the full integration
story.

---

## Building a custom DataSource

The simplest route is to subclass `BaseDataSource` and implement the
required abstract methods. The base class provides shared utilities
(type inference, literal coercion, validation) and a set of empty
hook methods for cross-cutting concerns.

### Required methods

A custom subclass must implement every abstract method on
`BaseDataSource`:

| Group | Methods |
|-------|---------|
| Data and view config | `set_data`, `set_filter`, `set_sort` |
| Pagination | `get_page`, `next_page`, `prev_page`, `has_next_page`, `total_count` |
| CRUD | `create_record`, `read_record`, `update_record`, `delete_record` |
| Selection | `select_record`, `unselect_record`, `select_all`, `unselect_all`, `get_selected`, `selected_count` |
| Export | `export_to_csv` |
| Index access | `get_page_from_index` |

### Skeleton

```python
from ttkbootstrap.datasource import BaseDataSource

class RedisDataSource(BaseDataSource):
    """DataSource backed by Redis hashes."""

    def __init__(self, redis_client, page_size=10):
        super().__init__(page_size)
        self.redis = redis_client
        self._where_sql = ""
        self._order_by_sql = ""

    # ----- data and view config -----

    def set_data(self, records):
        for i, record in enumerate(records):
            self.redis.hset(f"record:{i}", mapping=record)
        return self

    def set_filter(self, where_sql=""):
        self._where_sql = where_sql

    def set_sort(self, order_by_sql=""):
        self._order_by_sql = order_by_sql

    # ----- pagination -----

    def get_page(self, page=None):
        if page is not None:
            self._page = page
        start = self._page * self.page_size
        end = start + self.page_size
        return self._fetch_records()[start:end]

    def next_page(self):
        if self.has_next_page():
            self._page += 1
        return self.get_page()

    def prev_page(self):
        self._page = max(0, self._page - 1)
        return self.get_page()

    def has_next_page(self):
        return (self._page + 1) * self.page_size < self.total_count()

    def total_count(self):
        return len(self._fetch_records())

    # ... CRUD, selection, export, get_page_from_index left as exercises
```

### Hooks

`BaseDataSource` defines hook methods that subclasses can override
to add behavior around CRUD calls without reimplementing them.
Implementations of `create_record` / `update_record` / `delete_record`
are expected to call the matching hooks at the right time; the
built-in `MemoryDataSource` and `SqliteDataSource` do not currently
invoke them, so hooks only fire on subclasses that opt in.

```python
import logging
from datetime import datetime

class AuditedMemoryDataSource(MemoryDataSource):
    """MemoryDataSource that logs writes and stamps timestamps."""

    def create_record(self, record):
        record = self._before_create(record)
        record["created_at"] = datetime.now().isoformat()
        new_id = super().create_record(record)
        self._after_create(new_id, record)
        return new_id

    def _after_create(self, record_id, record):
        logging.info("created record %s", record_id)
```

Available hooks:

| Hook | Called |
|------|--------|
| `_before_create(record)` | Returns a (possibly modified) record before insert. |
| `_after_create(record_id, record)` | Side effects after insert. |
| `_before_update(record_id, updates)` | Returns a (possibly modified) updates dict before update. |
| `_after_update(record_id, updates, success)` | Side effects after update. |
| `_before_delete(record_id)` | Side effects before delete. |
| `_after_delete(record_id, success)` | Side effects after delete. |

### Implementing the protocol directly

If subclassing is the wrong shape — for example, a remote API client
where the page-size attribute and cursor model do not match — you
can implement `DataSourceProtocol` directly without inheriting from
`BaseDataSource`. The protocol is `@runtime_checkable`, so the only
requirement is that the methods exist with the right signatures.

```python
from ttkbootstrap.datasource import DataSourceProtocol

class APIDataSource:
    """DataSource backed by a paginated REST API."""

    page_size: int = 20

    def set_data(self, records):
        ...

    def get_page(self, page=None):
        ...

    # ... and all other protocol methods
```

!!! link "API Reference"
    See [BaseDataSource](../reference/data/BaseDataSource.md) and
    [DataSourceProtocol](../reference/data/DataSourceProtocol.md).

---

## Summary

- A DataSource decouples *where data lives* and *how it is filtered,
  sorted, and paged* from the widget that displays it.
- `MemoryDataSource` for transient in-process data;
  `SqliteDataSource` for persistence and SQL semantics;
  `FileDataSource` for CSV/JSON ingestion.
- All three speak the same protocol: `set_data`, `set_filter`,
  `set_sort`, `get_page`, `total_count`, the `*_record` CRUD
  methods, and the `*_record` / `*_all` selection methods.
- Filter spelling is `set_filter` (singular); the negative selection
  spelling is `unselect_*` (not `deselect_*`).
- Subclass `BaseDataSource` and implement the abstract methods to
  build a custom backend; use the `_before_*` / `_after_*` hooks
  for audit logging or transformations.

---

## API reference

- [DataSource API Reference](../reference/data/index.md) — index of all classes
- [MemoryDataSource](../reference/data/MemoryDataSource.md)
- [SqliteDataSource](../reference/data/SqliteDataSource.md)
- [FileDataSource](../reference/data/FileDataSource.md)
- [BaseDataSource](../reference/data/BaseDataSource.md)
- [DataSourceProtocol](../reference/data/DataSourceProtocol.md)

---

## Next steps

- [Tables and lists](tables-and-lists.md) — selection, CRUD, and
  filtering integrated end-to-end with TableView, ListView, and
  TreeView
- [ListView](../widgets/composites/listview.md) — data-aware list widget
- [TableView](../widgets/composites/tableview.md) — data-aware table widget
