"""In-memory data source implementation with filtering, sorting, and pagination.

Provides a pure-Python in-memory data manager that supports:
    - Pagination with configurable page size
    - SQL-like filtering with WHERE clause syntax
    - Multi-column sorting with ASC/DESC
    - Full CRUD operations (create, read, update, delete)
    - Record selection tracking
    - CSV export
    - Inferred schema from data

The MemoryDataSource stores all data in memory and provides fast access for
small to medium datasets. For larger datasets or persistence requirements,
consider using SqliteDataSource instead.

Filtering Syntax:
    Supports SQL-like WHERE conditions:
        - Comparisons: =, !=, >, >=, <, <=
        - String operations: CONTAINS, STARTSWITH, ENDSWITH
        - Set operations: IN ('val1', 'val2')
        - Pattern matching: LIKE with % and _ wildcards
        - Logical operators: AND, OR
        - Literals: 'string', "string", 123, 3.14, true, false, null

    Example:
        ```python
        set_filter("status = 'active' AND age >= 18")
        set_filter("name LIKE 'John%'")
        ```

Sorting Syntax:
    Multi-column sorting with ASC/DESC:
        set_sort("last_name ASC, age DESC")
        set_sort("priority DESC, created_at ASC")

Data Format:
    - Records must be dictionaries or will be auto-wrapped as {"text": str(value)}
    - Each record automatically gets an 'id' field (integer, auto-generated if missing)
    - Each record automatically gets a 'selected' field (0 or 1)
"""

from __future__ import annotations

import csv
import re
from collections.abc import Sequence
from typing import Any, Dict, List, Optional, Union, Mapping, Iterable, Tuple

from ttkbootstrap.datasource.base import BaseDataSource
from ttkbootstrap.datasource.types import Primitive


class MemoryDataSource(BaseDataSource):
    """In-memory data manager with pagination, filtering, sorting, and CRUD operations.

    Stores all records in memory as dictionaries with automatic ID generation and
    selection tracking. Provides SQL-like filtering and sorting syntax for intuitive
    data manipulation.

    The datasource maintains an internal index for O(1) ID lookups and supports
    dynamic schema inference from provided data.

    Args:
        page_size: Number of records per page (default: 10)

    Attributes:
        page_size: Current page size setting

    Example:
        ```python
        ds = MemoryDataSource(page_size=20)
        ds.set_data([
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ])
        ds.set_filter("age >= 30")
        page = ds.get_page(0)
        ```
    """

    def __init__(self, page_size: int = 10):
        """Initialize the in-memory datasource with defaults.

        Args:
            page_size: Number of records returned per page when paginating.
        """
        super().__init__(page_size)
        self._table = "records"
        self._columns: List[str] = []
        self._data: List[Dict[str, Any]] = []
        self._id_index: Dict[Any, int] = {}
        self._where_sql: str = ""
        self._order_by_sql: str = ""
        self._filter_predicate = None
        self._sort_keys: List[Tuple[str, bool]] = []

    def _rebuild_id_index(self) -> None:
        """Rebuild the ID-to-position index for fast lookups."""
        self._id_index.clear()
        for i, rec in enumerate(self._data):
            self._id_index[rec.get("id")] = i

    def _ensure_selected_column(self) -> None:
        """Ensure all records have a 'selected' field."""
        if "selected" not in self._columns:
            self._columns.append("selected")
            for r in self._data:
                r.setdefault("selected", 0)

    def _ensure_id(self) -> None:
        """Ensure all records have unique integer IDs."""
        used = set()
        max_id = 0
        for r in self._data:
            if "id" in r and isinstance(r["id"], int):
                used.add(r["id"])
                max_id = max(max_id, r["id"])
        for r in self._data:
            if "id" not in r or not isinstance(r["id"], int) or r["id"] in used:
                max_id += 1
                r["id"] = max_id
                used.add(max_id)
        self._rebuild_id_index()

    @staticmethod
    def _like_to_regex(pattern: str) -> re.Pattern:
        """Convert SQL LIKE pattern to regex (% -> .*, _ -> .)."""
        esc = ""
        for ch in pattern:
            if ch in ".^$*+?{}[]\\|()":
                esc += "\\" + ch
            else:
                esc += ch
        esc = esc.replace("%", ".*").replace("_", ".")
        return re.compile("^" + esc + "$", re.IGNORECASE)

    def _parse_filter(self, where_sql: str):
        """Parse WHERE clause into a predicate function.

        Args:
            where_sql: SQL WHERE clause

        Returns:
            Predicate function that evaluates rows, or None if no filter
        """
        if not where_sql:
            return None

        tokens = re.split(r"\s+(AND|OR)\s+", where_sql, flags=re.IGNORECASE)
        terms: List[Tuple[str, str, Any]] = []
        ops_between: List[str] = []

        def parse_term(t: str) -> Tuple[str, str, Any]:
            m_in = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+IN\s*\((.*)\)\s*$", t, flags=re.IGNORECASE)
            if m_in:
                col, inner = m_in.group(1), m_in.group(2)
                parts = [p.strip() for p in inner.split(",") if p.strip()]
                values = [self._coerce_literal(p) for p in parts]
                return col, "IN", values

            m_like = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+LIKE\s+(.+)\s*$", t, flags=re.IGNORECASE)
            if m_like:
                col, val = m_like.group(1), self._coerce_literal(m_like.group(2))
                return col, "LIKE", val

            for op in ("CONTAINS", "STARTSWITH", "ENDSWITH"):
                m = re.match(rf"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+{op}\s+(.+)\s*$", t, flags=re.IGNORECASE)
                if m:
                    col, val = m.group(1), self._coerce_literal(m.group(2))
                    return col, op.upper(), val

            m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(=|!=|>=|>|<=|<)\s*(.+)\s*$", t)
            if m:
                col, op, val = m.group(1), m.group(2), self._coerce_literal(m.group(3))
                return col, op, val

            m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*$", t)
            if m:
                col = m.group(1)
                return col, "truthy", True

            raise ValueError(f"Unrecognized filter term: {t!r}")

        for i, tok in enumerate(tokens):
            if i % 2 == 0:
                if not tok.strip():
                    continue
                terms.append(parse_term(tok))
            else:
                ops_between.append(tok.strip().upper())

        if not terms:
            return None

        prepared: List[Tuple[str, str, Any]] = []
        for col, op, val in terms:
            if op == "LIKE" and isinstance(val, str):
                prepared.append((col, op, self._like_to_regex(val)))
            else:
                prepared.append((col, op, val))

        def predicate(row: Mapping[str, Any]) -> bool:
            def eval_term(col: str, op: str, val: Any) -> bool:
                rv = row.get(col, None)
                try:
                    if op == "=":   return rv == val
                    if op == "!=":  return rv != val
                    if op == ">":   return (rv is not None) and (val is not None) and rv > val
                    if op == ">=":  return (rv is not None) and (val is not None) and rv >= val
                    if op == "<":   return (rv is not None) and (val is not None) and rv < val
                    if op == "<=":  return (rv is not None) and (val is not None) and rv <= val
                    if op == "CONTAINS":
                        return (rv is not None) and (val is not None) and (str(val).lower() in str(rv).lower())
                    if op == "STARTSWITH":
                        return (rv is not None) and (val is not None) and str(rv).lower().startswith(str(val).lower())
                    if op == "ENDSWITH":
                        return (rv is not None) and (val is not None) and str(rv).lower().endswith(str(val).lower())
                    if op == "IN":
                        return rv in val
                    if op == "LIKE" and isinstance(val, re.Pattern):
                        return (rv is not None) and bool(val.match(str(rv)))
                    if op == "truthy":
                        return bool(rv)
                except Exception:
                    return False
                return False

            result = eval_term(*prepared[0])
            for j, t in enumerate(prepared[1:], start=0):
                op_between = ops_between[j] if j < len(ops_between) else "AND"
                if op_between == "AND":
                    result = result and eval_term(*t)
                else:
                    result = result or eval_term(*t)
            return result

        return predicate

    def _parse_sort(self, order_by_sql: str) -> List[Tuple[str, bool]]:
        """Parse ORDER BY clause into list of (column, reverse_bool) tuples."""
        if not order_by_sql:
            return []
        parts = [p.strip() for p in order_by_sql.split(",") if p.strip()]
        out: List[Tuple[str, bool]] = []
        for p in parts:
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)(?:\s+(ASC|DESC))?$", p, flags=re.IGNORECASE)
            if not m:
                continue
            col = m.group(1)
            dir_tok = (m.group(2) or "ASC").upper()
            out.append((col, dir_tok == "DESC"))
        return out

    def _apply_filter_and_sort(self, rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply current filter and sort to row collection."""
        if self._filter_predicate:
            rows = [r for r in rows if self._filter_predicate(r)]
        else:
            rows = list(rows)

        if self._sort_keys:
            def key_func(r: Dict[str, Any]):
                key_parts = []
                for col, reverse in self._sort_keys:
                    v = r.get(col)
                    key_parts.append((v is None, v))
                return tuple(key_parts)

            for col, rev in reversed(self._sort_keys):
                rows.sort(key=lambda r, c=col: (r.get(c) is None, r.get(c)), reverse=rev)

        return rows

    def set_data(self, records: Union[Sequence[Primitive], Sequence[Dict[str, Any]]]) -> "MemoryDataSource":
        """Load records into datasource.

        Args:
            records: Sequence of dicts or primitives (auto-wrapped as {"text": str(x)})

        Returns:
            Self for method chaining
        """
        if not records:
            self._data = []
            self._columns = []
            self._rebuild_id_index()
            return self

        if records and not self._is_mapping(records[0]):
            records = [dict(text=str(x)) for x in records]

        data: List[Dict[str, Any]] = []
        for i, rec in enumerate(records):
            r = dict(rec)
            r.setdefault("id", i)
            r.setdefault("selected", 0)
            data.append(r)

        self._data = data
        self._columns = list(self._data[0].keys())
        self._ensure_id()
        self._ensure_selected_column()
        return self

    def set_filter(self, where_sql: str = ""):
        """Apply SQL-like WHERE filter to data."""
        self._where_sql = where_sql or ""
        self._filter_predicate = self._parse_filter(self._where_sql)

    def set_sort(self, order_by_sql: str = ""):
        """Apply SQL-like ORDER BY sorting to data."""
        self._order_by_sql = order_by_sql or ""
        self._sort_keys = self._parse_sort(self._order_by_sql)

    def _filtered_sorted_rows(self) -> List[Dict[str, Any]]:
        """Get all rows with current filter and sort applied."""
        return self._apply_filter_and_sort(self._data)

    def get_page(self, page: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get records for specified page."""
        if page is not None:
            self._page = max(0, int(page))
        rows = self._filtered_sorted_rows()
        start = self._page * self.page_size
        end = start + self.page_size
        return [dict(r) for r in rows[start:end]]

    def next_page(self) -> List[Dict[str, Any]]:
        """Advance to next page and return its records."""
        if self.has_next_page():
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
        return len(self._filtered_sorted_rows())

    def _generate_new_id(self) -> int:
        """Generate next available integer ID."""
        if not self._data:
            return 1
        return max(int(r.get("id", 0)) for r in self._data) + 1

    def create_record(self, record: Dict[str, Any]) -> int:
        """Create new record and return its ID."""
        r = dict(record)
        if "id" not in r:
            r["id"] = self._generate_new_id()
        if "selected" not in r:
            r["selected"] = 0
        self._data.append(r)
        self._columns = list(set(self._columns) | set(r.keys()))
        self._id_index[r["id"]] = len(self._data) - 1
        return r["id"]

    def read_record(self, record_id: Any) -> Optional[Dict[str, Any]]:
        """Retrieve single record by ID."""
        idx = self._id_index.get(record_id)
        if idx is None:
            return None
        return dict(self._data[idx])

    def update_record(self, record_id: Any, updates: Dict[str, Any]) -> bool:
        """Update record fields by ID."""
        if not updates:
            return False
        idx = self._id_index.get(record_id)
        if idx is None:
            return False
        self._data[idx].update(updates)
        self._columns = list(set(self._columns) | set(updates.keys()))
        return True

    def delete_record(self, record_id: Any) -> bool:
        """Delete record by ID."""
        idx = self._id_index.get(record_id)
        if idx is None:
            return False
        self._data.pop(idx)
        self._rebuild_id_index()
        return True

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
            ids = [r["id"] for r in self.get_page()]
            count = 0
            idset = set(ids)
            for r in self._data:
                if r["id"] in idset and r.get("selected") != 1:
                    r["selected"] = 1
                    count += 1
            return count
        else:
            count = 0
            for r in self._data:
                if r.get("selected") != 1:
                    r["selected"] = 1
                    count += 1
            return count

    def unselect_all(self, current_page_only: bool = False) -> int:
        """Unselect all records (optionally only current page)."""
        self._ensure_selected_column()
        if current_page_only:
            ids = [r["id"] for r in self.get_page()]
            count = 0
            idset = set(ids)
            for r in self._data:
                if r["id"] in idset and r.get("selected") != 0:
                    r["selected"] = 0
                    count += 1
            return count
        else:
            count = 0
            for r in self._data:
                if r.get("selected") != 0:
                    r["selected"] = 0
                    count += 1
            return count

    def _set_selected_flag(self, record_id: Any, flag: int) -> bool:
        """Set selection flag for record by ID."""
        self._ensure_selected_column()
        idx = self._id_index.get(record_id)
        if idx is None:
            return False
        self._data[idx]["selected"] = 1 if flag else 0
        return True

    def get_selected(self, page: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get selected records, optionally paginated."""
        self._ensure_selected_column()
        rows = [r for r in self._data if r.get("selected") == 1]
        rows = self._apply_filter_and_sort(rows)
        if page is None:
            return [dict(r) for r in rows]
        start = max(0, int(page)) * self.page_size
        end = start + self.page_size
        return [dict(r) for r in rows[start:end]]

    def selected_count(self) -> int:
        """Get total number of selected records."""
        self._ensure_selected_column()
        return sum(1 for r in self._data if r.get("selected") == 1)

    def export_to_csv(self, filepath: str, include_all: bool = True) -> None:
        """Export records to CSV file."""
        rows = self._data if include_all else [r for r in self._data if r.get("selected") == 1]
        if not rows:
            return
        fieldnames = list(self._columns) if self._columns else list(rows[0].keys())
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r.get(k) for k in fieldnames})

    def get_page_from_index(self, start_index: int, count: int) -> List[Dict[str, Any]]:
        """Get records by start index and count (respects filter/sort)."""
        rows = self._filtered_sorted_rows()
        start = max(0, int(start_index))
        end = start + max(0, int(count))
        return [dict(r) for r in rows[start:end]]
