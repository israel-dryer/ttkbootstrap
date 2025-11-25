"""Data source abstraction for ttkbootstrap widgets.

Provides unified interface for data management with multiple backend implementations:
    - MemoryDataSource: Fast in-memory storage for small to medium datasets
    - SqliteDataSource: Persistent SQLite storage for large datasets
    - FileDataSource: File-based storage with support for CSV, JSON, and various formats

All datasources support:
    - Pagination with configurable page size
    - SQL-like filtering and sorting
    - Full CRUD operations (create, read, update, delete)
    - Record selection tracking
    - CSV export

Usage:
    from ttkbootstrap.datasource import MemoryDataSource, SqliteDataSource, FileDataSource

    # In-memory datasource
    ds = MemoryDataSource(page_size=20)
    ds.set_data([{"name": "Alice", "age": 30}, ...])

    # SQLite datasource (persistent)
    db = SqliteDataSource("mydata.db", page_size=50)
    db.set_data([{"name": "Bob", "age": 25}, ...])

    # File datasource (CSV, JSON, etc.)
    file_ds = FileDataSource("data.csv", page_size=25)
    file_ds.load()

    # Common operations (work with all)
    ds.set_filter("age >= 25")
    ds.set_sort("name ASC")
    page1 = ds.get_page(0)
"""

from ttkbootstrap.datasource.base import BaseDataSource
from ttkbootstrap.datasource.memory_source import MemoryDataSource
from ttkbootstrap.datasource.sqlite_source import SqliteDataSource
from ttkbootstrap.datasource.file_source import FileDataSource, FileSourceConfig
from ttkbootstrap.datasource.types import DataSourceProtocol, Record, Primitive

__all__ = [
    'BaseDataSource',
    'MemoryDataSource',
    'SqliteDataSource',
    'FileDataSource',
    'FileSourceConfig',
    'DataSourceProtocol',
    'Record',
    'Primitive',
]