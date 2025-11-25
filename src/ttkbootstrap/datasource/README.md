# ttkbootstrap DataSource Module

A flexible, extensible data management system providing unified interfaces for working with data from various sources (memory, databases, files) with built-in support for pagination, filtering, sorting, and CRUD operations.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Built-in Implementations](#built-in-implementations)
- [Creating Custom DataSources](#creating-custom-datasources)
- [API Reference](#api-reference)
- [Examples](#examples)

## Architecture Overview

The datasource module is built on three key components:

### 1. DataSourceProtocol (types.py)

A Protocol (duck-typing interface) that defines the contract all datasources must follow. This enables type checking and IDE support without requiring inheritance.

```python
from typing import Protocol

class DataSourceProtocol(Protocol):
    page_size: int
    def set_data(self, records): ...
    def get_page(self, page=None): ...
    # ... other methods
```

### 2. BaseDataSource (base.py)

An abstract base class that provides:
- **Abstract method definitions** - Enforces implementation of required methods
- **Shared utility methods** - Common functionality like type inference and literal parsing
- **Hook methods** - Extension points for customization (e.g., `_before_create`, `_after_update`)

This is the **recommended base class** for creating custom datasources.

### 3. Concrete Implementations

Built-in datasources that inherit from `BaseDataSource`:
- **MemoryDataSource** - Fast in-memory storage
- **SqliteDataSource** - Persistent SQLite storage
- **FileDataSource** - File-based storage (CSV, JSON, JSONL, TSV)

## Built-in Implementations

### MemoryDataSource

Best for small to medium datasets that fit comfortably in memory.

```python
from ttkbootstrap.datasource import MemoryDataSource

ds = MemoryDataSource(page_size=20)
ds.set_data([
    {"name": "Alice", "age": 30, "city": "NYC"},
    {"name": "Bob", "age": 25, "city": "LA"},
])

ds.set_filter("age >= 25")
ds.set_sort("name ASC")
page = ds.get_page(0)
```

**Features:**
- SQL-like filtering (WHERE syntax)
- Multi-column sorting (ORDER BY syntax)
- O(1) ID lookups via internal index
- Automatic ID generation

### SqliteDataSource

Best for large datasets requiring persistence or SQL capabilities.

```python
from ttkbootstrap.datasource import SqliteDataSource

# Persistent database
ds = SqliteDataSource("mydata.db", page_size=50)
ds.set_data([...])

# In-memory database
ds = SqliteDataSource(":memory:", page_size=50)
```

**Features:**
- SQL-native filtering and sorting
- Persistent storage across sessions
- Efficient for large datasets
- Automatic schema inference

### FileDataSource

Best for loading data from files with preprocessing needs.

```python
from ttkbootstrap.datasource import FileDataSource, FileSourceConfig

# Simple CSV loading
ds = FileDataSource("data.csv")
ds.load()

# With transformations
config = FileSourceConfig(
    column_renames={'old_name': 'new_name'},
    column_types={'age': int, 'salary': float},
    row_filter=lambda r: r['status'] == 'active'
)
ds = FileDataSource("data.json", config=config)
ds.load()
```

**Features:**
- Supports CSV, TSV, JSON, JSONL
- Multiple loading strategies (eager, lazy, chunked, hybrid)
- Transformation pipeline
- Progress callbacks for large files

## Creating Custom DataSources

### Method 1: Inherit from BaseDataSource (Recommended)

This is the easiest and most common approach. You get utility methods for free and only need to implement storage-specific logic.

```python
from ttkbootstrap.datasource import BaseDataSource
from typing import Any, Dict, List, Optional

class RedisDataSource(BaseDataSource):
    """Custom datasource backed by Redis."""

    def __init__(self, redis_client, page_size=10):
        super().__init__(page_size)
        self.redis = redis_client
        self._key_prefix = "myapp:records:"

    def set_data(self, records):
        """Store records in Redis."""
        for record in records:
            record_id = record.get('id', self._generate_id())
            key = f"{self._key_prefix}{record_id}"
            self.redis.set(key, json.dumps(record))
        return self

    def get_page(self, page=None):
        """Retrieve a page of records."""
        if page is not None:
            self._page = page

        # Get all keys and paginate
        keys = self.redis.keys(f"{self._key_prefix}*")
        start = self._page * self.page_size
        end = start + self.page_size

        records = []
        for key in keys[start:end]:
            data = self.redis.get(key)
            records.append(json.loads(data))

        return records

    def create_record(self, record):
        """Create new record in Redis."""
        record_id = record.get('id', self._generate_id())
        record['id'] = record_id

        # Use hook for logging/validation
        record = self._before_create(record)

        key = f"{self._key_prefix}{record_id}"
        self.redis.set(key, json.dumps(record))

        # Use hook for post-creation tasks
        self._after_create(record_id, record)

        return record_id

    def read_record(self, record_id):
        """Read single record from Redis."""
        key = f"{self._key_prefix}{record_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def update_record(self, record_id, updates):
        """Update record in Redis."""
        record = self.read_record(record_id)
        if not record:
            return False

        updates = self._before_update(record_id, updates)
        record.update(updates)

        key = f"{self._key_prefix}{record_id}"
        self.redis.set(key, json.dumps(record))

        self._after_update(record_id, updates, True)
        return True

    def delete_record(self, record_id):
        """Delete record from Redis."""
        self._before_delete(record_id)
        key = f"{self._key_prefix}{record_id}"
        result = self.redis.delete(key) > 0
        self._after_delete(record_id, result)
        return result

    # Implement remaining abstract methods...
    # (set_filter, set_sort, next_page, prev_page, has_next_page,
    #  total_count, selection methods, export_to_csv, etc.)
```

### Method 2: Implement the Protocol (Advanced)

For maximum flexibility, implement the `DataSourceProtocol` without inheritance. This is useful when you need to integrate with existing classes or have complex inheritance requirements.

```python
from ttkbootstrap.datasource import DataSourceProtocol
from typing import List, Dict, Any, Optional

class APIDataSource:
    """Datasource that fetches data from a REST API."""

    def __init__(self, api_url: str, page_size: int = 10):
        self.api_url = api_url
        self.page_size = page_size
        self._page = 0
        self._cache = []

    def set_data(self, records):
        """Cache data locally."""
        self._cache = list(records)
        return self

    def get_page(self, page: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch page from API or cache."""
        if page is not None:
            self._page = page

        # Make API request with pagination
        response = requests.get(
            self.api_url,
            params={'page': self._page, 'per_page': self.page_size}
        )
        return response.json()['data']

    # Implement all other protocol methods...
```

### Using Utility Methods

The `BaseDataSource` provides several utility methods you can use:

```python
class MyDataSource(BaseDataSource):
    def process_record(self, raw_data: str):
        # Parse literals
        age = self._coerce_literal("25")  # Returns int 25
        active = self._coerce_literal("true")  # Returns bool True
        name = self._coerce_literal("'Alice'")  # Returns str "Alice"

        # Infer SQL types
        age_type = self._infer_type(25)  # Returns "INTEGER"
        name_type = self._infer_type("Alice")  # Returns "TEXT"

        # Validate records
        record = {"name": name, "age": age}
        self._validate_record(record)  # Raises ValueError if not dict

        return record
```

### Using Hook Methods

Hook methods let you add custom behavior without overriding core logic:

```python
class AuditedDataSource(BaseDataSource):
    def __init__(self):
        super().__init__()
        self.audit_log = []

    def _before_create(self, record):
        """Add timestamp before creating."""
        record['created_at'] = datetime.now().isoformat()
        return record

    def _after_create(self, record_id, record):
        """Log creation to audit trail."""
        self.audit_log.append({
            'action': 'CREATE',
            'record_id': record_id,
            'timestamp': datetime.now()
        })

    def _before_update(self, record_id, updates):
        """Add modified timestamp."""
        updates['modified_at'] = datetime.now().isoformat()
        return updates

    def _after_update(self, record_id, updates, success):
        """Log update to audit trail."""
        if success:
            self.audit_log.append({
                'action': 'UPDATE',
                'record_id': record_id,
                'changes': updates,
                'timestamp': datetime.now()
            })
```

## API Reference

### Required Methods (All Implementations)

#### Data & View Configuration
- `set_data(records)` - Load data into the datasource
- `set_filter(where_sql)` - Apply SQL-like WHERE filter
- `set_sort(order_by_sql)` - Apply SQL-like ORDER BY sorting

#### Pagination
- `get_page(page=None)` - Get records for specified page
- `next_page()` - Move to next page
- `prev_page()` - Move to previous page
- `has_next_page()` - Check if next page exists
- `total_count()` - Get total record count

#### CRUD Operations
- `create_record(record)` - Create new record, returns ID
- `read_record(record_id)` - Read single record by ID
- `update_record(record_id, updates)` - Update record fields
- `delete_record(record_id)` - Delete record by ID

#### Selection Management
- `select_record(record_id)` - Mark record as selected
- `unselect_record(record_id)` - Unmark record
- `select_all(current_page_only=False)` - Select all/page records
- `unselect_all(current_page_only=False)` - Unselect all/page records
- `get_selected(page=None)` - Get selected records
- `selected_count()` - Count selected records

#### Export
- `export_to_csv(filepath, include_all=True)` - Export to CSV

#### Index-based Access
- `get_page_from_index(start_index, count)` - Get records by index range

### Utility Methods (Inherited from BaseDataSource)

- `_infer_type(value)` - Infer SQL type from Python value
- `_is_mapping(x)` - Check if value is dict-like
- `_coerce_literal(s)` - Parse string literal to Python value
- `_validate_record(record)` - Validate record is a dictionary

### Hook Methods (Inherited from BaseDataSource)

Override these to add custom behavior:

- `_before_create(record)` - Called before creating record
- `_after_create(record_id, record)` - Called after creating record
- `_before_update(record_id, updates)` - Called before updating
- `_after_update(record_id, updates, success)` - Called after updating
- `_before_delete(record_id)` - Called before deleting
- `_after_delete(record_id, success)` - Called after deleting

## Examples

### Example 1: MongoDB DataSource

```python
from ttkbootstrap.datasource import BaseDataSource
from pymongo import MongoClient

class MongoDataSource(BaseDataSource):
    def __init__(self, connection_string, database, collection, page_size=10):
        super().__init__(page_size)
        self.client = MongoClient(connection_string)
        self.db = self.client[database]
        self.collection = self.db[collection]
        self._filter = {}
        self._sort = []

    def set_data(self, records):
        """Insert records into MongoDB."""
        if records:
            self.collection.insert_many(list(records))
        return self

    def set_filter(self, where_sql=""):
        """Convert SQL-like filter to MongoDB query."""
        # Simple implementation - in production, use a proper parser
        if "age >= 30" in where_sql:
            self._filter = {"age": {"$gte": 30}}
        else:
            self._filter = {}

    def set_sort(self, order_by_sql=""):
        """Convert SQL ORDER BY to MongoDB sort."""
        if "name ASC" in order_by_sql:
            self._sort = [("name", 1)]
        elif "age DESC" in order_by_sql:
            self._sort = [("age", -1)]
        else:
            self._sort = []

    def get_page(self, page=None):
        if page is not None:
            self._page = page

        skip = self._page * self.page_size
        cursor = self.collection.find(self._filter).sort(self._sort).skip(skip).limit(self.page_size)
        return list(cursor)

    def create_record(self, record):
        result = self.collection.insert_one(record)
        return result.inserted_id

    def read_record(self, record_id):
        return self.collection.find_one({"_id": record_id})

    def update_record(self, record_id, updates):
        result = self.collection.update_one({"_id": record_id}, {"$set": updates})
        return result.modified_count > 0

    def delete_record(self, record_id):
        result = self.collection.delete_one({"_id": record_id})
        return result.deleted_count > 0

    # ... implement remaining methods
```

### Example 2: Cached API DataSource

```python
from ttkbootstrap.datasource import BaseDataSource
import requests
from functools import lru_cache
from datetime import datetime, timedelta

class CachedAPIDataSource(BaseDataSource):
    def __init__(self, api_url, cache_ttl=300, page_size=10):
        super().__init__(page_size)
        self.api_url = api_url
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_time = {}

    def _is_cache_valid(self, key):
        """Check if cached data is still valid."""
        if key not in self._cache_time:
            return False
        age = datetime.now() - self._cache_time[key]
        return age < timedelta(seconds=self.cache_ttl)

    def get_page(self, page=None):
        if page is not None:
            self._page = page

        cache_key = f"page_{self._page}"

        # Return cached data if valid
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        # Fetch from API
        response = requests.get(
            f"{self.api_url}/records",
            params={'page': self._page, 'per_page': self.page_size}
        )
        data = response.json()

        # Cache the result
        self._cache[cache_key] = data
        self._cache_time[cache_key] = datetime.now()

        return data

    def create_record(self, record):
        # Invalidate cache on write
        self._cache.clear()
        self._cache_time.clear()

        response = requests.post(f"{self.api_url}/records", json=record)
        return response.json()['id']

    # ... implement remaining methods
```

### Example 3: Multi-Source DataSource

```python
from ttkbootstrap.datasource import BaseDataSource

class MultiSourceDataSource(BaseDataSource):
    """Aggregates data from multiple datasources."""

    def __init__(self, sources, page_size=10):
        super().__init__(page_size)
        self.sources = sources  # List of datasources
        self._aggregated_data = []

    def set_data(self, records):
        """Not applicable for multi-source."""
        raise NotImplementedError("Use add_source() instead")

    def add_source(self, datasource):
        """Add a datasource to aggregate."""
        self.sources.append(datasource)

    def _aggregate_data(self):
        """Combine data from all sources."""
        all_records = []
        for source in self.sources:
            source_records = source.get_page_from_index(0, source.total_count())
            all_records.extend(source_records)
        return all_records

    def get_page(self, page=None):
        if page is not None:
            self._page = page

        all_data = self._aggregate_data()
        start = self._page * self.page_size
        end = start + self.page_size
        return all_data[start:end]

    # ... implement remaining methods
```

## Best Practices

1. **Always call `super().__init__(page_size)`** in your `__init__` method
2. **Use hook methods** for cross-cutting concerns (logging, validation, caching)
3. **Inherit utility methods** instead of reimplementing them
4. **Handle errors gracefully** - return False/None for failures rather than raising
5. **Document your datasource** - explain what backend it uses and any special requirements
6. **Test thoroughly** - ensure all protocol methods work correctly
7. **Consider performance** - implement efficient filtering and pagination for large datasets

## Testing Your DataSource

```python
def test_custom_datasource():
    ds = MyCustomDataSource()

    # Test basic operations
    ds.set_data([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
    assert ds.total_count() == 2

    # Test CRUD
    new_id = ds.create_record({"name": "Charlie"})
    assert ds.read_record(new_id) is not None

    # Test pagination
    page = ds.get_page(0)
    assert isinstance(page, list)

    # Test filtering
    ds.set_filter("name = 'Alice'")
    filtered = ds.get_page(0)
    assert len(filtered) == 1

    # Test it's an instance of BaseDataSource
    assert isinstance(ds, BaseDataSource)
```

## Migration Guide

If you have an existing datasource implementation, here's how to migrate to use `BaseDataSource`:

### Before (Standalone Class)

```python
class MyDataSource:
    def __init__(self, page_size=10):
        self.page_size = page_size
        self._page = 0

    @staticmethod
    def _infer_type(value):
        # Your implementation
        pass
```

### After (Inheriting BaseDataSource)

```python
from ttkbootstrap.datasource import BaseDataSource

class MyDataSource(BaseDataSource):
    def __init__(self, page_size=10):
        super().__init__(page_size)  # Initialize base class
        # BaseDataSource now provides _page and utility methods

    # Remove _infer_type - inherited from BaseDataSource
```

## Support

For questions, issues, or feature requests, please visit:
- GitHub Issues: https://github.com/israel-dryer/ttkbootstrap/issues
- Documentation: https://ttkbootstrap.readthedocs.io/

## License

This module is part of ttkbootstrap and follows the same license terms.