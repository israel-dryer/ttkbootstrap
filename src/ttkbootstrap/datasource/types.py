"""Type definitions and protocols for ttkbootstrap datasource module.

This module defines the core protocol that all datasource implementations must follow,
enabling consistent data management across different backends (memory, SQLite, web, etc.).

The DataSourceProtocol provides a unified interface for:
    - Data loading and configuration (set_data, set_filter, set_sort)
    - Pagination (get_page, next_page, prev_page, has_next_page)
    - CRUD operations (create, read, update, delete)
    - Selection management (select/unselect records)
    - Data export (CSV export)
    - Index-based access (get_page_from_index)

All datasource implementations should conform to this protocol to ensure
compatibility with datasource-aware widgets and utilities.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, Sequence, Mapping, runtime_checkable

# Type aliases for clarity
Primitive = Any  # Can be str, int, float, bool, None, etc.
Record = Dict[str, Any]


@runtime_checkable
class DataSourceProtocol(Protocol):
    """Protocol defining the interface for data source implementations.

    This protocol establishes a contract that all datasource backends must implement,
    ensuring consistent behavior across different storage mechanisms (memory, database,
    web API, etc.).

    All datasource implementations must support:
        - Pagination with configurable page size
        - Filtering using SQL-like WHERE syntax
        - Sorting using SQL-like ORDER BY syntax
        - Full CRUD operations on records
        - Selection tracking for multi-select scenarios
        - CSV export capabilities
        - Direct index-based data access

    Attributes:
        page_size: Number of records per page

    Notes:
        - Records are represented as Dict[str, Any] with at least 'id' and 'selected' fields
        - Filtering and sorting syntax follows SQL conventions for familiarity
        - All methods preserve immutability - operations return new data or modify in-place
    """

    # public attrs
    page_size: int

    # ---------- data & view config ----------
    def set_data(self, records: Sequence[Primitive] | Sequence[Mapping[str, Any]]) -> DataSourceProtocol:
        """Load data records into the datasource.

        Args:
            records: Sequence of records (dicts) or primitives (auto-wrapped)

        Returns:
            Self for method chaining
        """
        ...

    def set_filter(self, where_sql: str = "") -> None:
        """Apply SQL-like WHERE clause filter to data.

        Args:
            where_sql: SQL WHERE condition (e.g., "age > 25 AND status = 'active'")
        """
        ...

    def set_sort(self, order_by_sql: str = "") -> None:
        """Apply SQL-like ORDER BY clause to data.

        Args:
            order_by_sql: SQL ORDER BY clause (e.g., "name ASC, age DESC")
        """
        ...

    # ---------- pagination ----------
    def get_page(self, page: Optional[int] = None) -> List[Record]:
        """Get records for specified page (or current page if None).

        Args:
            page: Page number (0-indexed); updates current page if provided

        Returns:
            List of record dictionaries for the page
        """
        ...

    def next_page(self) -> List[Record]:
        """Advance to next page and return its records.

        Returns:
            List of record dictionaries for the new page
        """
        ...

    def prev_page(self) -> List[Record]:
        """Move to previous page and return its records.

        Returns:
            List of record dictionaries for the new page
        """
        ...

    def has_next_page(self) -> bool:
        """Check if more pages exist after current page.

        Returns:
            True if next page exists, False otherwise
        """
        ...

    def total_count(self) -> int:
        """Get total number of records matching current filter.

        Returns:
            Total record count (respects active filter)
        """
        ...

    # ---------- CRUD ----------
    def create_record(self, record: Dict[str, Any]) -> int:
        """Create new record and return its ID.

        Args:
            record: Dictionary with record data

        Returns:
            The ID assigned to the new record
        """
        ...

    def read_record(self, record_id: Any) -> Optional[Record]:
        """Retrieve single record by ID.

        Args:
            record_id: Unique identifier of the record

        Returns:
            Record dictionary or None if not found
        """
        ...

    def update_record(self, record_id: Any, updates: Dict[str, Any]) -> bool:
        """Update record fields by ID.

        Args:
            record_id: Unique identifier of the record
            updates: Dictionary with fields to update

        Returns:
            True if record was updated, False if not found
        """
        ...

    def delete_record(self, record_id: Any) -> bool:
        """Delete record by ID.

        Args:
            record_id: Unique identifier of the record

        Returns:
            True if record was deleted, False if not found
        """
        ...

    # ---------- selection ----------
    def select_record(self, record_id: Any) -> bool:
        """Mark record as selected.

        Args:
            record_id: Unique identifier of the record

        Returns:
            True if record was selected, False if not found
        """
        ...

    def unselect_record(self, record_id: Any) -> bool:
        """Mark record as unselected.

        Args:
            record_id: Unique identifier of the record

        Returns:
            True if record was unselected, False if not found
        """
        ...

    def select_all(self, current_page_only: bool = False) -> int:
        """Select all records (optionally only current page).

        Args:
            current_page_only: If True, select only records on current page

        Returns:
            Number of records selected
        """
        ...

    def unselect_all(self, current_page_only: bool = False) -> int:
        """Unselect all records (optionally only current page).

        Args:
            current_page_only: If True, unselect only records on current page

        Returns:
            Number of records unselected
        """
        ...

    def get_selected(self, page: Optional[int] = None) -> List[Record]:
        """Get selected records, optionally paginated.

        Args:
            page: Optional page number for paginating selected records

        Returns:
            List of selected record dictionaries
        """
        ...

    def selected_count(self) -> int:
        """Get total number of selected records.

        Returns:
            Count of selected records
        """
        ...

    # ---------- export ----------
    def export_to_csv(self, filepath: str, include_all: bool = True) -> None:
        """Export records to CSV file.

        Args:
            filepath: Path to output CSV file
            include_all: If True, export all records; if False, export only selected
        """
        ...

    # ---------- index-based paging ----------
    def get_page_from_index(self, start_index: int, count: int) -> List[Record]:
        """Get records by start index and count (respects filter/sort).

        Args:
            start_index: Starting record index
            count: Number of records to retrieve

        Returns:
            List of record dictionaries
        """
        ...