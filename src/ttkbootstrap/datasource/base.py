"""Abstract base class for datasource implementations.

Provides a common foundation for all datasource implementations with:
    - Abstract method definitions enforcing the DataSourceProtocol interface
    - Shared utility methods for type inference, literal parsing, and validation
    - Template methods for common operations
    - Hook methods for extensibility

Subclasses must implement storage-specific operations (set_data, get_page, CRUD, etc.)
while inheriting common utilities and patterns.

This base class makes it easier to:
    - Create custom datasource implementations
    - Reduce code duplication across implementations
    - Ensure consistent behavior across all datasources
    - Extend datasource functionality through hooks
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence, Mapping

from ttkbootstrap.datasource.types import Primitive, Record


class BaseDataSource(ABC):
    """Abstract base class for datasource implementations.

    Provides shared utilities and enforces the DataSourceProtocol interface through
    abstract methods. Subclasses implement storage-specific logic while inheriting
    common functionality.

    Args:
        page_size: Number of records per page (default: 10)

    Attributes:
        page_size: Current page size setting

    Examples:
        # Create custom datasource
        class RedisDataSource(BaseDataSource):
            def __init__(self, redis_client, page_size=10):
                super().__init__(page_size)
                self.redis = redis_client

            def set_data(self, records):
                # Redis-specific implementation
                pass

            def get_page(self, page=None):
                # Redis-specific implementation
                pass

            # ... implement other abstract methods
    """

    def __init__(self, page_size: int = 10):
        """Initialize base datasource with pagination settings.

        Args:
            page_size: Number of records returned per page when paginating.
        """
        self.page_size = page_size
        self._page = 0

    # ========== ABSTRACT METHODS - MUST BE IMPLEMENTED ==========

    # Data & View Configuration
    @abstractmethod
    def set_data(self, records: Sequence[Primitive] | Sequence[Mapping[str, Any]]) -> 'BaseDataSource':
        """Load data records into the datasource.

        Args:
            records: Sequence of records (dicts) or primitives (auto-wrapped)

        Returns:
            Self for method chaining
        """
        ...

    @abstractmethod
    def set_filter(self, where_sql: str = "") -> None:
        """Apply SQL-like WHERE clause filter to data.

        Args:
            where_sql: SQL WHERE condition (e.g., "age > 25 AND status = 'active'")
        """
        ...

    @abstractmethod
    def set_sort(self, order_by_sql: str = "") -> None:
        """Apply SQL-like ORDER BY clause to data.

        Args:
            order_by_sql: SQL ORDER BY clause (e.g., "name ASC, age DESC")
        """
        ...

    # Pagination
    @abstractmethod
    def get_page(self, page: Optional[int] = None) -> List[Record]:
        """Get records for specified page (or current page if None).

        Args:
            page: Page number (0-indexed); updates current page if provided

        Returns:
            List of record dictionaries for the page
        """
        ...

    @abstractmethod
    def next_page(self) -> List[Record]:
        """Advance to next page and return its records.

        Returns:
            List of record dictionaries for the new page
        """
        ...

    @abstractmethod
    def prev_page(self) -> List[Record]:
        """Move to previous page and return its records.

        Returns:
            List of record dictionaries for the new page
        """
        ...

    @abstractmethod
    def has_next_page(self) -> bool:
        """Check if more pages exist after current page.

        Returns:
            True if next page exists, False otherwise
        """
        ...

    @abstractmethod
    def total_count(self) -> int:
        """Get total number of records matching current filter.

        Returns:
            Total record count (respects active filter)
        """
        ...

    # CRUD Operations
    @abstractmethod
    def create_record(self, record: Dict[str, Any]) -> int:
        """Create new record and return its ID.

        Args:
            record: Dictionary with record data

        Returns:
            The ID assigned to the new record
        """
        ...

    @abstractmethod
    def read_record(self, record_id: Any) -> Optional[Record]:
        """Retrieve single record by ID.

        Args:
            record_id: Unique identifier of the record

        Returns:
            Record dictionary or None if not found
        """
        ...

    @abstractmethod
    def update_record(self, record_id: Any, updates: Dict[str, Any]) -> bool:
        """Update record fields by ID.

        Args:
            record_id: Unique identifier of the record
            updates: Dictionary with fields to update

        Returns:
            True if record was updated, False if not found
        """
        ...

    @abstractmethod
    def delete_record(self, record_id: Any) -> bool:
        """Delete record by ID.

        Args:
            record_id: Unique identifier of the record

        Returns:
            True if record was deleted, False if not found
        """
        ...

    # Selection Management
    @abstractmethod
    def select_record(self, record_id: Any) -> bool:
        """Mark record as selected.

        Args:
            record_id: Unique identifier of the record

        Returns:
            True if record was selected, False if not found
        """
        ...

    @abstractmethod
    def unselect_record(self, record_id: Any) -> bool:
        """Mark record as unselected.

        Args:
            record_id: Unique identifier of the record

        Returns:
            True if record was unselected, False if not found
        """
        ...

    @abstractmethod
    def select_all(self, current_page_only: bool = False) -> int:
        """Select all records (optionally only current page).

        Args:
            current_page_only: If True, select only records on current page

        Returns:
            Number of records selected
        """
        ...

    @abstractmethod
    def unselect_all(self, current_page_only: bool = False) -> int:
        """Unselect all records (optionally only current page).

        Args:
            current_page_only: If True, unselect only records on current page

        Returns:
            Number of records unselected
        """
        ...

    @abstractmethod
    def get_selected(self, page: Optional[int] = None) -> List[Record]:
        """Get selected records, optionally paginated.

        Args:
            page: Optional page number for paginating selected records

        Returns:
            List of selected record dictionaries
        """
        ...

    @abstractmethod
    def selected_count(self) -> int:
        """Get total number of selected records.

        Returns:
            Count of selected records
        """
        ...

    # Export
    @abstractmethod
    def export_to_csv(self, filepath: str, include_all: bool = True) -> None:
        """Export records to CSV file.

        Args:
            filepath: Path to output CSV file
            include_all: If True, export all records; if False, export only selected
        """
        ...

    # Index-based Access
    @abstractmethod
    def get_page_from_index(self, start_index: int, count: int) -> List[Record]:
        """Get records by start index and count (respects filter/sort).

        Args:
            start_index: Starting record index
            count: Number of records to retrieve

        Returns:
            List of record dictionaries
        """
        ...

    # ========== SHARED UTILITY METHODS ==========

    @staticmethod
    def _infer_type(value: Any) -> str:
        """Infer SQL-compatible type from Python value.

        Args:
            value: Python value to infer type from

        Returns:
            SQL type string ('INTEGER', 'REAL', 'BLOB', or 'TEXT')

        Examples:
            >>> BaseDataSource._infer_type(42)
            'INTEGER'
            >>> BaseDataSource._infer_type(3.14)
            'REAL'
            >>> BaseDataSource._infer_type("hello")
            'TEXT'
        """
        if isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "REAL"
        elif isinstance(value, (bytes, bytearray)):
            return "BLOB"
        return "TEXT"

    @staticmethod
    def _is_mapping(x: Any) -> bool:
        """Check if value is a mapping (dict-like).

        Args:
            x: Value to check

        Returns:
            True if value is a mapping, False otherwise

        Examples:
            >>> BaseDataSource._is_mapping({'a': 1})
            True
            >>> BaseDataSource._is_mapping([1, 2, 3])
            False
        """
        return isinstance(x, Mapping)

    @staticmethod
    def _coerce_literal(s: str) -> Any:
        """Parse string literal into Python value (int, float, bool, None, or str).

        Converts SQL/JSON-like literal strings into appropriate Python types:
            - Quoted strings ('foo', "bar") -> str
            - true/false -> bool
            - null/none -> None
            - Numeric strings -> int or float
            - Everything else -> str

        Args:
            s: String literal to parse

        Returns:
            Parsed Python value

        Examples:
            >>> BaseDataSource._coerce_literal("'hello'")
            'hello'
            >>> BaseDataSource._coerce_literal("42")
            42
            >>> BaseDataSource._coerce_literal("3.14")
            3.14
            >>> BaseDataSource._coerce_literal("true")
            True
            >>> BaseDataSource._coerce_literal("null")
            None
        """
        t = s.strip()

        # Handle quoted strings
        if len(t) >= 2 and ((t[0] == t[-1] == "'") or (t[0] == t[-1] == '"')):
            return t[1:-1]

        # Handle booleans
        if t.lower() == "true":
            return True
        if t.lower() == "false":
            return False

        # Handle null/none
        if t.lower() in ("null", "none"):
            return None

        # Try numeric conversion
        try:
            return int(t)
        except Exception:
            pass

        try:
            return float(t)
        except Exception:
            pass

        # Default to string
        return t

    @staticmethod
    def _validate_record(record: Any) -> None:
        """Validate that a record is a dictionary.

        Args:
            record: Value to validate

        Raises:
            ValueError: If record is not a dictionary

        Examples:
            >>> BaseDataSource._validate_record({'id': 1})  # OK
            >>> BaseDataSource._validate_record([1, 2, 3])  # Raises ValueError
        """
        if not isinstance(record, dict):
            raise ValueError(f"Record must be a dictionary, got {type(record).__name__}")

    # ========== HOOK METHODS (Can be overridden by subclasses) ==========

    def _before_create(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before creating a record.

        Subclasses can override this to perform validation, transformation,
        or side effects before record creation.

        Args:
            record: Record about to be created

        Returns:
            Modified record (or original if no changes)

        Examples:
            class TimestampedDataSource(BaseDataSource):
                def _before_create(self, record):
                    record = super()._before_create(record)
                    record['created_at'] = datetime.now()
                    return record
        """
        return record

    def _after_create(self, record_id: int, record: Dict[str, Any]) -> None:
        """Hook called after creating a record.

        Subclasses can override this to perform logging, caching updates,
        or other side effects after record creation.

        Args:
            record_id: ID of the created record
            record: The created record

        Examples:
            class LoggingDataSource(BaseDataSource):
                def _after_create(self, record_id, record):
                    super()._after_create(record_id, record)
                    logger.info(f"Created record {record_id}")
        """
        pass

    def _before_update(self, record_id: Any, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before updating a record.

        Args:
            record_id: ID of record being updated
            updates: Updates to apply

        Returns:
            Modified updates (or original if no changes)
        """
        return updates

    def _after_update(self, record_id: Any, updates: Dict[str, Any], success: bool) -> None:
        """Hook called after updating a record.

        Args:
            record_id: ID of updated record
            updates: Updates that were applied
            success: Whether the update succeeded
        """
        pass

    def _before_delete(self, record_id: Any) -> None:
        """Hook called before deleting a record.

        Args:
            record_id: ID of record about to be deleted
        """
        pass

    def _after_delete(self, record_id: Any, success: bool) -> None:
        """Hook called after deleting a record.

        Args:
            record_id: ID of deleted record
            success: Whether the deletion succeeded
        """
        pass