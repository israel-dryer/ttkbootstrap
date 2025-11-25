"""SQLite-backed data source implementation with persistence, filtering, and pagination.

Provides a database-backed data manager that supports:
    - Persistent storage using SQLite
    - All features of MemoryDataSource (pagination, filtering, sorting, CRUD)
    - Efficient handling of large datasets
    - SQL-native filtering and sorting
    - Automatic schema inference
    - Data persistence across application restarts

The SqliteDataSource is ideal for:
    - Large datasets that don't fit comfortably in memory
    - Applications requiring data persistence
    - Scenarios needing SQL query capabilities
    - Multi-user or multi-session data sharing

For in-memory, lightweight scenarios, consider MemoryDataSource instead.

Examples:
    # Persistent database file
    ds = SqliteDataSource("mydata.db", page_size=50)
    ds.set_data([{"name": "Alice", "age": 30}, ...])

    # In-memory database (no persistence)
    ds = SqliteDataSource(":memory:", page_size=25)

    # SQL filtering and sorting
    ds.set_filter("age >= 25 AND status = 'active'")
    ds.set_sort("name ASC, age DESC")

    # All CRUD operations work identically to MemoryDataSource
    new_id = ds.create_record({"name": "Bob", "age": 28})
    ds.update_record(new_id, {"age": 29})
"""

from __future__ import annotations

import csv
import sqlite3
from typing import Any, Dict, List, Optional, Union, Sequence

from ttkbootstrap.datasource.types import Primitive, Record


class SqliteDataSource:
    """SQLite-backed data manager with pagination, filtering, sorting, and CRUD operations.

    Provides persistent storage using SQLite database with automatic schema inference
    and SQL-native filtering/sorting. Supports all operations defined in DataSourceProtocol.

    Args:
        name: Database file path or ":memory:" for in-memory database (default: ":memory:")
        page_size: Number of records per page (default: 10)

    Attributes:
        conn: SQLite database connection
        page_size: Current page size setting

    Examples:
        # Create persistent database
        ds = SqliteDataSource("data.db", page_size=20)
        ds.set_data([
            {"name": "Alice", "age": 30, "dept": "Engineering"},
            {"name": "Bob", "age": 25, "dept": "Sales"},
        ])

        # Use SQL for filtering and sorting
        ds.set_filter("age > 25")
        ds.set_sort("name ASC")

        # Pagination
        page1 = ds.get_page(0)
        has_more = ds.has_next_page()

        # CRUD operations
        new_id = ds.create_record({"name": "Charlie", "age": 28, "dept": "Marketing"})
        ds.update_record(new_id, {"dept": "Engineering"})
        record = ds.read_record(new_id)
        ds.delete_record(new_id)

        # Selection and export
        ds.select_all()
        ds.export_to_csv("selected.csv", include_all=False)

    Notes:
        - The database connection persists for the lifetime of the object
        - Close the connection explicitly with conn.close() if needed
        - Schema is inferred from first record's data types
        - 'id' field is automatically set as PRIMARY KEY
        - 'selected' field is added automatically for selection tracking
    """

    def __init__(self, name: str = ":memory:", page_size: int = 10):
        """Create SQLite datasource and set initial pagination state.

        Args:
            name: Database file path or ':memory:' for an in-memory database.
            page_size: Number of records returned per page during pagination.
        """
        self.conn = sqlite3.connect(name)
        self.conn.row_factory = sqlite3.Row
        self.page_size = page_size
        self._table = "records"
        self._where = ""
        self._order_by = ""
        self._page = 0
        self._columns = []

    @classmethod
    def _infer_type(cls, value: Any) -> str:
        """Infer SQL type from Python value."""
        if isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "REAL"
        elif isinstance(value, bytes):
            return "BLOB"
        return "TEXT"

    def set_data(self, records: Union[Sequence[Primitive], Sequence[dict[str, Any]]]):
        """Load records into database, creating table with inferred schema.

        Args:
            records: Sequence of dicts or primitives (auto-wrapped as {"text": str(x)})

        Returns:
            Self for method chaining
        """
        if not records:
            return self

        # Coerce into a dictionary if not already
        if not isinstance(records[0], dict):
            records = [dict(text=str(x)) for x in records]

        # Ensure each record has an 'id'
        for i, record in enumerate(records):
            if "id" not in record:
                record["id"] = i

            if "selected" not in record:
                record["selected"] = 0

        self._columns = list(records[0].keys())
        col_types = {col: self._infer_type(records[0][col]) for col in self._columns}
        col_definitions = ", ".join(
            f"{col} {col_types[col]}" + (" PRIMARY KEY" if col == "id" else "")
            for col in self._columns
        )

        self.conn.execute(f"DROP TABLE IF EXISTS {self._table}")
        self.conn.execute(f"CREATE TABLE {self._table} ({col_definitions})")

        with self.conn:
            for row in records:
                placeholders = ", ".join("?" for _ in self._columns)
                values = tuple(row.get(col) for col in self._columns)
                self.conn.execute(f"INSERT INTO {self._table} VALUES ({placeholders})", values)
        return self

    def set_filter(self, where_sql: str = ""):
        """Apply SQL WHERE clause filter."""
        self._where = where_sql

    def set_sort(self, order_by_sql: str = ""):
        """Apply SQL ORDER BY clause for sorting."""
        self._order_by = order_by_sql

    def get_page(self, page: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get records for specified page."""
        if page is not None:
            self._page = page
        offset = self._page * self.page_size

        query = f"SELECT * FROM {self._table}"
        if self._where:
            query += f" WHERE {self._where}"
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        query += f" LIMIT {self.page_size} OFFSET {offset}"

        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def next_page(self) -> List[Dict[str, Any]]:
        """Advance to next page and return its records."""
        self._page += 1
        return self.get_page()

    def prev_page(self) -> List[Dict[str, Any]]:
        """Move to previous page and return its records."""
        self._page = max(0, self._page - 1)
        return self.get_page()

    def has_next_page(self) -> bool:
        """Check if more pages exist after current page."""
        return (self._page + 1) * self.page_size < self.total_count()

    def total_count(self) -> int:
        """Get total number of records matching current filter."""
        query = f"SELECT COUNT(*) FROM {self._table}"
        if self._where:
            query += f" WHERE {self._where}"
        return self.conn.execute(query).fetchone()[0]

    # === CRUD OPERATIONS ===

    def create_record(self, record: Dict[str, Any]) -> int:
        """Create new record and return its ID."""
        if "id" not in record:
            record["id"] = self._generate_new_id()

        if "selected" not in record:
            record["selected"] = 0

        keys = record.keys()
        cols = ", ".join(keys)
        placeholders = ", ".join("?" for _ in keys)
        values = tuple(record[col] for col in keys)

        with self.conn:
            self.conn.execute(f"INSERT INTO {self._table} ({cols}) VALUES ({placeholders})", values)
        return record["id"]

    def read_record(self, record_id: Any) -> Optional[Dict[str, Any]]:
        """Retrieve single record by ID."""
        cursor = self.conn.execute(f"SELECT * FROM {self._table} WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_record(self, record_id: Any, updates: Dict[str, Any]) -> bool:
        """Update record fields by ID."""
        if not updates:
            return False
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = tuple(updates.values()) + (record_id,)
        with self.conn:
            cur = self.conn.execute(f"UPDATE {self._table} SET {set_clause} WHERE id = ?", values)
            return cur.rowcount > 0

    def delete_record(self, record_id: Any) -> bool:
        """Delete record by ID."""
        with self.conn:
            cur = self.conn.execute(f"DELETE FROM {self._table} WHERE id = ?", (record_id,))
            return cur.rowcount > 0

    def _generate_new_id(self) -> int:
        """Generate next available integer ID."""
        cursor = self.conn.execute(f"SELECT MAX(id) FROM {self._table}")
        max_id = cursor.fetchone()[0]
        return (max_id or 0) + 1

    # === SELECTION ====

    def select_record(self, record_id: Any) -> bool:
        """Mark record as selected."""
        return self._set_selected_flag(record_id, 1)

    def unselect_record(self, record_id: Any) -> bool:
        """Mark record as unselected."""
        return self._set_selected_flag(record_id, 0)

    def select_all(self, current_page_only: bool = False) -> int:
        """Select all records (optionally only current page)."""
        self._ensure_selected_column()
        if current_page_only:
            ids = [row["id"] for row in self.get_page()]
            if not ids:
                return 0
            placeholders = ", ".join("?" for _ in ids)
            query = f"UPDATE {self._table} SET selected = 1 WHERE id IN ({placeholders})"
            with self.conn:
                cur = self.conn.execute(query, ids)
                return cur.rowcount
        else:
            with self.conn:
                cur = self.conn.execute(f"UPDATE {self._table} SET selected = 1")
                return cur.rowcount

    def unselect_all(self, current_page_only: bool = False) -> int:
        """Unselect all records (optionally only current page)."""
        self._ensure_selected_column()
        if current_page_only:
            ids = [row["id"] for row in self.get_page()]
            if not ids:
                return 0
            placeholders = ", ".join("?" for _ in ids)
            query = f"UPDATE {self._table} SET selected = 0 WHERE id IN ({placeholders})"
            with self.conn:
                cur = self.conn.execute(query, ids)
                return cur.rowcount
        else:
            with self.conn:
                cur = self.conn.execute(f"UPDATE {self._table} SET selected = 0")
                return cur.rowcount

    def get_selected(self, page: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get selected records, optionally paginated."""
        self._ensure_selected_column()
        query = f"SELECT * FROM {self._table} WHERE selected = 1"

        if page is not None:
            offset = page * self.page_size
            query += f" LIMIT {self.page_size} OFFSET {offset}"

        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def _ensure_selected_column(self):
        """Add 'selected' column to table if it doesn't exist."""
        if "selected" not in self._columns:
            with self.conn:
                self.conn.execute(f"ALTER TABLE {self._table} ADD COLUMN selected INTEGER DEFAULT 0")
            self._columns.append("selected")

    def selected_count(self) -> int:
        """Get total number of selected records."""
        self._ensure_selected_column()
        query = f"SELECT COUNT(*) FROM {self._table} WHERE selected = 1"
        return self.conn.execute(query).fetchone()[0]

    def _set_selected_flag(self, record_id: Any, flag: int) -> bool:
        """Set selection flag for record by ID."""
        if "selected" not in self._columns:
            # Add selected column if it doesn't exist
            with self.conn:
                self.conn.execute(f"ALTER TABLE {self._table} ADD COLUMN selected INTEGER DEFAULT 0")
            self._columns.append("selected")

        with self.conn:
            cur = self.conn.execute(f"UPDATE {self._table} SET selected = ? WHERE id = ?", (flag, record_id))
            return cur.rowcount > 0

    # === DATA EXPORT ===

    def export_to_csv(self, filepath: str, include_all: bool = True):
        """Export records to CSV file."""
        self._ensure_selected_column()
        query = f"SELECT * FROM {self._table}"
        if not include_all:
            query += " WHERE selected = 1"

        cursor = self.conn.execute(query)
        rows = cursor.fetchall()

        if not rows:
            return

        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))

    def get_page_from_index(self, start_index: int, count: int) -> List[Dict[str, Any]]:
        """Get records by start index and count (respects filter/sort)."""
        query = f"SELECT * FROM {self._table}"
        if self._where:
            query += f" WHERE {self._where}"
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        query += f" LIMIT {count} OFFSET {start_index}"
        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]
