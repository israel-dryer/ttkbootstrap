---
title: DataSource
---

# DataSource

This guide explains how to use ttkbootstrap's DataSource system for managing data with pagination, filtering, sorting, and CRUD operations.

---

## Overview

A **DataSource** is a unified interface for managing tabular data. It provides:

- **Pagination** — retrieve data in pages
- **Filtering** — SQL-like WHERE syntax
- **Sorting** — SQL-like ORDER BY syntax
- **CRUD** — create, read, update, delete records
- **Selection** — track selected records
- **Export** — CSV export

DataSources decouple data management from widgets, making it easy to switch between in-memory, database, or file-backed storage.

---

## Built-in DataSource types

ttkbootstrap provides three DataSource implementations:

| Type | Best for |
|------|----------|
| `MemoryDataSource` | Small to medium datasets, temporary data |
| `SqliteDataSource` | Large datasets, persistence, SQL queries |
| `FileDataSource` | Loading from CSV, JSON, JSONL files |

---

## MemoryDataSource

Stores all data in memory. Fast and simple for small datasets.

!!! link "API Reference"
    See [MemoryDataSource](../reference/data/MemoryDataSource.md) for full API details.

```python
from ttkbootstrap.datasource import MemoryDataSource

# Create datasource with page size
ds = MemoryDataSource(page_size=10)

# Load data
ds.set_data([
    {"name": "Alice", "age": 30, "department": "Engineering"},
    {"name": "Bob", "age": 25, "department": "Sales"},
    {"name": "Charlie", "age": 35, "department": "Engineering"},
])

# Get first page
page = ds.get_page(0)
```

Records are automatically assigned an `id` field if not present, and a `selected` field for tracking selection state.

---

## SqliteDataSource

Stores data in a SQLite database. Ideal for large datasets or when persistence is needed.

!!! link "API Reference"
    See [SqliteDataSource](../reference/data/SqliteDataSource.md) for full API details.

```python
from ttkbootstrap.datasource import SqliteDataSource

# Create with database file (or ":memory:" for in-memory)
ds = SqliteDataSource("data.db", page_size=50)

# Load data (creates table with inferred schema)
ds.set_data([
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
])

# Filter and sort use native SQL
ds.set_filter("age >= 25")
ds.set_sort("name ASC")
page = ds.get_page(0)
```

---

## FileDataSource

Loads data from CSV, JSON, or JSONL files with configurable loading strategies.

!!! link "API Reference"
    See [FileDataSource](../reference/data/FileDataSource.md) and [FileSourceConfig](../reference/data/FileSourceConfig.md) for full API details.

```python
from ttkbootstrap.datasource import FileDataSource

# Load from CSV
ds = FileDataSource("employees.csv", page_size=20)
ds.load()

# Get data
page = ds.get_page(0)
```

### Loading strategies

FileDataSource supports multiple loading strategies for different file sizes:

| Strategy | Description |
|----------|-------------|
| `"eager"` | Load all data into memory (fast access, high memory) |
| `"lazy"` | Load on-demand per page (slow access, low memory) |
| `"chunked"` | Load in configurable batches (balanced) |
| `"auto"` | Automatically select based on file size |

```python
from ttkbootstrap.datasource import FileDataSource, FileSourceConfig

config = FileSourceConfig(
    loading_strategy="lazy",
    encoding="utf-8",
)

ds = FileDataSource("large_file.csv", config=config)
ds.load()
```

---

## Filtering

Apply SQL-like WHERE filters to narrow down records:

```python
ds.set_filter("age > 30")
ds.set_filter("department = 'Engineering'")
ds.set_filter("name CONTAINS 'son'")
ds.set_filter("age >= 25 AND department = 'Sales'")
```

### Supported operators

| Operator | Example |
|----------|---------|
| `=`, `!=` | `status = 'active'` |
| `>`, `>=`, `<`, `<=` | `age >= 18` |
| `CONTAINS` | `name CONTAINS 'john'` |
| `STARTSWITH` | `email STARTSWITH 'admin'` |
| `ENDSWITH` | `file ENDSWITH '.txt'` |
| `LIKE` | `name LIKE 'J%'` (% = any chars, _ = one char) |
| `IN` | `status IN ('active', 'pending')` |
| `AND`, `OR` | `age > 25 AND active = true` |

### Clearing filters

```python
ds.set_filter("")  # Clear filter
```

---

## Sorting

Apply SQL-like ORDER BY sorting:

```python
ds.set_sort("name ASC")
ds.set_sort("age DESC")
ds.set_sort("department ASC, salary DESC")  # Multi-column
```

### Clearing sort

```python
ds.set_sort("")  # Clear sort
```

---

## Pagination

Navigate through data in pages:

```python
# Get specific page (0-indexed)
page = ds.get_page(0)
page = ds.get_page(2)

# Navigate
next_records = ds.next_page()
prev_records = ds.prev_page()

# Check navigation
if ds.has_next_page():
    ds.next_page()

# Get total count (respects filter)
total = ds.total_count()

# Get records by index range
records = ds.get_page_from_index(start_index=10, count=5)
```

---

## CRUD operations

### Create

```python
new_id = ds.create_record({
    "name": "Diana",
    "age": 28,
    "department": "Marketing"
})
```

### Read

```python
record = ds.read_record(record_id=1)
if record:
    print(record["name"])
```

### Update

```python
success = ds.update_record(record_id=1, updates={"age": 31})
```

### Delete

```python
success = ds.delete_record(record_id=1)
```

---

## Selection management

Track which records are selected:

```python
# Select/unselect individual records
ds.select_record(record_id=1)
ds.unselect_record(record_id=1)

# Select/unselect all
ds.select_all()
ds.select_all(current_page_only=True)
ds.unselect_all()
ds.unselect_all(current_page_only=True)

# Get selected records
selected = ds.get_selected()
count = ds.selected_count()
```

---

## CSV export

Export records to CSV:

```python
# Export all records
ds.export_to_csv("all_data.csv", include_all=True)

# Export only selected records
ds.export_to_csv("selected.csv", include_all=False)
```

---

## Using with widgets

DataSources integrate with data-aware widgets like ListView:

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import MemoryDataSource

app = ttk.App()

# Create datasource
ds = MemoryDataSource(page_size=20)
ds.set_data([
    {"name": "Alice", "role": "Developer"},
    {"name": "Bob", "role": "Designer"},
])

# Use with ListView
listview = ttk.ListView(app, datasource=ds)
listview.pack(fill="both", expand=True)

app.mainloop()
```

---

## Creating a custom DataSource

To create a custom DataSource, extend `BaseDataSource` and implement the required abstract methods.

!!! link "API Reference"
    See [BaseDataSource](../reference/data/BaseDataSource.md) and [DataSourceProtocol](../reference/data/DataSourceProtocol.md) for full API details.

### Using BaseDataSource

```python
from ttkbootstrap.datasource import BaseDataSource

class RedisDataSource(BaseDataSource):
    """Custom datasource backed by Redis."""

    def __init__(self, redis_client, page_size=10):
        super().__init__(page_size)
        self.redis = redis_client
        self._data = []
        self._filter = ""
        self._sort = ""

    def set_data(self, records):
        # Store in Redis
        for i, record in enumerate(records):
            self.redis.hset(f"record:{i}", mapping=record)
        return self

    def set_filter(self, where_sql=""):
        self._filter = where_sql

    def set_sort(self, order_by_sql=""):
        self._sort = order_by_sql

    def get_page(self, page=None):
        if page is not None:
            self._page = page
        # Fetch from Redis and apply pagination
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

    # Implement remaining CRUD and selection methods...
```

### Using hooks

`BaseDataSource` provides hooks for extending behavior:

```python
class AuditedDataSource(BaseDataSource):
    """DataSource with audit logging."""

    def _before_create(self, record):
        record["created_at"] = datetime.now().isoformat()
        return record

    def _after_create(self, record_id, record):
        logging.info(f"Created record {record_id}")

    def _before_update(self, record_id, updates):
        updates["updated_at"] = datetime.now().isoformat()
        return updates

    def _after_delete(self, record_id, success):
        if success:
            logging.info(f"Deleted record {record_id}")
```

Available hooks:

| Hook | Called |
|------|--------|
| `_before_create(record)` | Before creating a record |
| `_after_create(record_id, record)` | After creating a record |
| `_before_update(record_id, updates)` | Before updating a record |
| `_after_update(record_id, updates, success)` | After updating a record |
| `_before_delete(record_id)` | Before deleting a record |
| `_after_delete(record_id, success)` | After deleting a record |

### Using the protocol directly

For maximum flexibility, implement `DataSourceProtocol` directly:

```python
from ttkbootstrap.datasource import DataSourceProtocol

class APIDataSource:
    """DataSource backed by a REST API."""

    page_size: int = 20

    def set_data(self, records):
        # POST to API
        ...

    def get_page(self, page=None):
        # GET from API with pagination
        ...

    # Implement all protocol methods...
```

---

## Summary

- Use **MemoryDataSource** for small, temporary datasets
- Use **SqliteDataSource** for large datasets or persistence
- Use **FileDataSource** for loading from CSV/JSON files
- **Filtering** uses SQL-like WHERE syntax
- **Sorting** uses SQL-like ORDER BY syntax
- Extend **BaseDataSource** for custom backends
- Use **hooks** for audit logging, validation, or side effects

---

## API reference

For complete API documentation, see:

- [DataSource API Reference](../reference/data/index.md) — all datasource classes and types
- [MemoryDataSource](../reference/data/MemoryDataSource.md)
- [SqliteDataSource](../reference/data/SqliteDataSource.md)
- [FileDataSource](../reference/data/FileDataSource.md)
- [BaseDataSource](../reference/data/BaseDataSource.md)
- [DataSourceProtocol](../reference/data/DataSourceProtocol.md)

---

## Next steps

- [ListView](../widgets/composites/listview.md) — data-aware list widget
- [TableView](../widgets/composites/tableview.md) — data-aware table widget
