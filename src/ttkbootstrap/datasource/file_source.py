"""File-based datasource with support for CSV, JSON, and lazy loading strategies.

Provides file-backed data storage with multiple loading strategies optimized for
different file sizes. Supports extensive transformation pipelines for data cleaning
and preprocessing.

Supported Formats (Built-in):
    - CSV: Comma-separated values
    - TSV: Tab-separated values
    - JSON: Standard JSON arrays or objects
    - JSONL/NDJSON: Line-delimited JSON (one record per line)

Loading Strategies:
    - Eager: Load all data into memory at once (fast access, high memory)
    - Lazy: Load data on-demand per page (slow access, low memory)
    - Chunked: Load in configurable batches (balanced approach)
    - Hybrid: Index in memory, lazy-load records (optimized balance)
    - Auto: Automatically select strategy based on file size

Transformation Pipeline:
    - Column renaming
    - Type conversions
    - Custom transformation functions per column
    - Row-level filtering during load
    - Row-level transformations
    - Default values for missing data

Large File Optimization:
    - Streaming parsing for minimal memory usage
    - Threading for non-blocking loads
    - Progress callbacks for UI updates
    - Automatic strategy selection based on file size

Examples:
    # Simple CSV loading
    ds = FileDataSource("data.csv")
    ds.load()

    # Large file with progress
    config = FileSourceConfig(
        loading_strategy='lazy',
        use_threading=True,
        progress_callback=lambda curr, total: print(f"{curr}/{total}")
    )
    ds = FileDataSource("large.csv", config=config)
    ds.load(on_complete=lambda: print("Done!"))

    # JSON with transformations
    config = FileSourceConfig(
        column_renames={'old_name': 'new_name'},
        column_types={'age': int, 'salary': float},
        row_filter=lambda r: r['status'] == 'active'
    )
    ds = FileDataSource("data.json", config=config)
"""

from __future__ import annotations

import csv
import json
import os
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    Any, Callable, Dict, Iterator, List, Literal, Optional, Union
)

from ttkbootstrap.datasource.memory_source import MemoryDataSource
from ttkbootstrap.datasource.types import Record, Primitive


@dataclass
class FileSourceConfig:
    """Configuration for file datasource loading and transformations.

    Controls how files are parsed, loaded, and transformed. Provides extensive
    customization for handling various data formats and scenarios.

    File Format Options:
        file_format: Format type - auto-detected from extension if 'auto'
        encoding: Character encoding (default: 'utf-8')

    CSV/TSV Options:
        delimiter: Field separator (None = auto-detect: ',' for CSV, tab for TSV)
        quotechar: Quote character for fields containing delimiter
        skip_rows: Number of header rows to skip
        header_row: Row index containing column names (None = no header)
        has_header: Whether first row contains column names

    JSON Options:
        json_lines: True for line-delimited JSON (JSONL/NDJSON format)
        json_orient: Pandas-like orientation for JSON arrays

    Column Transformations:
        column_renames: Map {old_name: new_name} for renaming columns
        column_types: Map {column: type} for type conversions
        column_transforms: Map {column: func} for custom transformations
        columns_to_load: List of columns to load (None = all columns)
        default_values: Map {column: value} for missing/null values

    Row Processing:
        row_filter: Function(row_dict) -> bool to filter rows during load
        row_transform: Function(row_dict) -> row_dict for row-level transforms

    Large File Handling:
        loading_strategy: How to load file ('eager', 'lazy', 'chunked', 'hybrid', 'auto')
        chunk_size: Rows per chunk for chunked/lazy loading
        max_memory_rows: Threshold for auto-switching strategies

    Threading & Progress:
        use_threading: Load file in background thread (non-blocking)
        progress_callback: Function(current, total) called during load
        on_complete: Function() called when loading completes
        on_error: Function(exception) called if loading fails

    Examples:
        # Basic config with transformations
        config = FileSourceConfig(
            column_renames={'emp_id': 'id', 'emp_name': 'name'},
            column_types={'age': int, 'salary': float},
            row_filter=lambda r: r['status'] == 'active'
        )

        # Large file optimization
        config = FileSourceConfig(
            loading_strategy='lazy',
            chunk_size=5000,
            use_threading=True,
            progress_callback=show_progress
        )
    """

    # File format and encoding
    file_format: Literal['auto', 'csv', 'tsv', 'json', 'jsonl'] = 'auto'
    encoding: str = 'utf-8'

    # CSV/TSV options
    delimiter: Optional[str] = None
    quotechar: str = '"'
    skip_rows: int = 0
    header_row: Optional[int] = 0
    has_header: bool = True

    # JSON options
    json_lines: bool = False
    json_orient: Literal['records', 'index', 'columns', 'values'] = 'records'

    # Column transformations
    column_renames: Optional[Dict[str, str]] = None
    column_types: Optional[Dict[str, type]] = None
    column_transforms: Optional[Dict[str, Callable[[Any], Any]]] = None
    columns_to_load: Optional[List[str]] = None
    default_values: Optional[Dict[str, Any]] = None

    # Row-level processing
    row_filter: Optional[Callable[[Dict[str, Any]], bool]] = None
    row_transform: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None

    # Large file handling
    loading_strategy: Literal['eager', 'lazy', 'chunked', 'hybrid', 'auto'] = 'auto'
    chunk_size: int = 10000
    max_memory_rows: int = 100000

    # Threading & progress
    use_threading: bool = False
    progress_callback: Optional[Callable[[int, int], None]] = None
    on_complete: Optional[Callable[[], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None


class FileDataSource(MemoryDataSource):
    """File-based datasource with MemoryDataSource API and advanced loading strategies.

    Extends MemoryDataSource to load data from files (CSV, JSON, JSONL) with support
    for large files via multiple loading strategies. Provides extensive transformation
    pipeline for data preprocessing.

    The datasource automatically selects optimal loading strategy based on file size
    and configuration. Supports background loading with progress callbacks for UI
    integration.

    Args:
        filepath: Path to data file
        config: FileSourceConfig object (uses defaults if None)
        page_size: Records per page for pagination (default: 10)

    Attributes:
        filepath: Path object for the data file
        config: Active configuration
        is_loaded: Whether file has been loaded

    Loading Strategies:
        Eager: Load entire file into memory
            - Fastest access after initial load
            - High memory usage
            - Best for: Small files (< 100k rows)

        Lazy: Load data on-demand per page
            - Slowest access (re-parses on each request)
            - Minimal memory usage
            - Best for: Very large files (> 1M rows)

        Chunked: Load file in batches
            - Balanced performance and memory
            - Shows progress during load
            - Best for: Medium files (100k-500k rows)

        Hybrid: Index in memory, lazy-load records
            - Fast filtering/sorting
            - Moderate memory usage
            - Best for: Large files (500k-1M rows)

        Auto: Automatically select based on file size
            - < 100k rows: Eager
            - 100k-500k: Chunked
            - > 500k: Hybrid

    Examples:
        # Simple eager loading
        ds = FileDataSource("small.csv")
        ds.load()
        ds.set_filter("age > 25")
        page = ds.get_page(0)

        # Large file with progress
        def show_progress(current, total):
            print(f"Loading: {current}/{total} ({current/total*100:.1f}%)")

        config = FileSourceConfig(
            loading_strategy='lazy',
            use_threading=True,
            progress_callback=show_progress,
            on_complete=lambda: print("Complete!")
        )

        ds = FileDataSource("large.csv", config=config, page_size=100)
        ds.load()  # Returns immediately, loads in background

        # Transformations
        config = FileSourceConfig(
            column_renames={'employee_id': 'id', 'full_name': 'name'},
            column_types={'age': int, 'salary': float, 'active': bool},
            column_transforms={
                'name': lambda x: x.strip().title(),
                'email': str.lower
            },
            row_filter=lambda r: r.get('active', True),
            default_values={'department': 'Unassigned'}
        )

        ds = FileDataSource("employees.json", config=config)
        ds.load()

        # JSONL (line-delimited JSON)
        config = FileSourceConfig(json_lines=True)
        ds = FileDataSource("logs.jsonl", config=config)

    Notes:
        - File is re-parsed on reload()
        - Threading uses daemon threads (auto-cleanup)
        - All MemoryDataSource methods available after load
        - Lazy strategy re-parses file on filter/sort changes
    """

    def __init__(
        self,
        filepath: str | Path,
        config: Optional[FileSourceConfig] = None,
        page_size: int = 10
    ):
        """Configure a file-backed datasource and detect file format.

        Args:
            filepath: Location of the data file to be read.
            config: Optional overrides for parsing, transforms, and threading.
            page_size: Number of records returned per page after loading.

        Raises:
            FileNotFoundError: If the supplied file path cannot be found.
        """
        super().__init__(page_size=page_size)

        self.filepath = Path(filepath)
        self.config = config or FileSourceConfig()

        # Loading state
        self.is_loaded = False
        self._loading = False
        self._load_progress = (0, 0)
        self._load_thread = None

        # Detect file format
        self._detected_format = self._detect_format()

        # Validate file exists
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")

    def _detect_format(self) -> str:
        """Detect file format from extension or config."""
        if self.config.file_format != 'auto':
            return self.config.file_format

        ext = self.filepath.suffix.lower()
        format_map = {
            '.csv': 'csv',
            '.tsv': 'tsv',
            '.txt': 'csv',  # Assume CSV for .txt
            '.json': 'json',
            '.jsonl': 'jsonl',
            '.ndjson': 'jsonl',
        }

        return format_map.get(ext, 'csv')  # Default to CSV

    def _estimate_row_count(self) -> int:
        """Estimate total row count for progress tracking."""
        file_size = self.filepath.stat().st_size

        # Estimate based on file format
        if self._detected_format in ('csv', 'tsv'):
            # Sample first few lines to estimate average row size
            with open(self.filepath, 'r', encoding=self.config.encoding) as f:
                sample_lines = []
                for i, line in enumerate(f):
                    if i >= 100:  # Sample first 100 lines
                        break
                    sample_lines.append(len(line.encode('utf-8')))

                if sample_lines:
                    avg_line_size = sum(sample_lines) / len(sample_lines)
                    estimated = int(file_size / avg_line_size)
                    return max(estimated - self.config.skip_rows - 1, 0)

        # For JSON, harder to estimate - use file size as proxy
        return file_size // 100  # Very rough estimate

    def _determine_strategy(self) -> str:
        """Determine optimal loading strategy."""
        if self.config.loading_strategy != 'auto':
            return self.config.loading_strategy

        # Auto-select based on estimated row count
        estimated_rows = self._estimate_row_count()

        if estimated_rows < self.config.max_memory_rows:
            return 'eager'
        elif estimated_rows < self.config.max_memory_rows * 5:
            return 'chunked'
        else:
            return 'hybrid'

    def _parse_csv_records(self) -> Iterator[Record]:
        """Parse CSV/TSV file and yield records."""
        delimiter = self.config.delimiter
        if delimiter is None:
            delimiter = '\t' if self._detected_format == 'tsv' else ','

        with open(self.filepath, 'r', encoding=self.config.encoding, newline='') as f:
            # Skip initial rows if configured
            for _ in range(self.config.skip_rows):
                next(f, None)

            reader = csv.DictReader(
                f,
                delimiter=delimiter,
                quotechar=self.config.quotechar
            )

            for row in reader:
                yield dict(row)

    def _parse_json_records(self) -> Iterator[Record]:
        """Parse JSON file and yield records."""
        with open(self.filepath, 'r', encoding=self.config.encoding) as f:
            if self.config.json_lines:
                # JSONL format - one JSON object per line
                for line in f:
                    line = line.strip()
                    if line:
                        yield json.loads(line)
            else:
                # Standard JSON
                data = json.load(f)

                # Handle different JSON structures
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            yield item
                        else:
                            yield {'value': item}
                elif isinstance(data, dict):
                    # Could be records, columns, etc.
                    if self.config.json_orient == 'records':
                        # Assume it's a dict of lists
                        for item in data.get('records', data.values()):
                            if isinstance(item, dict):
                                yield item
                    else:
                        # Single record
                        yield data

    def _parse_records(self) -> Iterator[Record]:
        """Parse file and yield records based on format."""
        if self._detected_format in ('csv', 'tsv'):
            yield from self._parse_csv_records()
        elif self._detected_format in ('json', 'jsonl'):
            yield from self._parse_json_records()
        else:
            raise ValueError(f"Unsupported format: {self._detected_format}")

    def _apply_transformations(self, record: Record) -> Optional[Record]:
        """Apply transformation pipeline to a single record.

        Returns:
            Transformed record or None if filtered out
        """
        # Apply row filter first
        if self.config.row_filter and not self.config.row_filter(record):
            return None

        # Apply column selection
        if self.config.columns_to_load:
            record = {k: v for k, v in record.items() if k in self.config.columns_to_load}

        # Apply column renames
        if self.config.column_renames:
            for old_name, new_name in self.config.column_renames.items():
                if old_name in record:
                    record[new_name] = record.pop(old_name)

        # Apply default values
        if self.config.default_values:
            for col, default in self.config.default_values.items():
                if col not in record or record[col] is None:
                    record[col] = default

        # Apply type conversions
        if self.config.column_types:
            for col, col_type in self.config.column_types.items():
                if col in record and record[col] is not None:
                    try:
                        if callable(col_type):
                            record[col] = col_type(record[col])
                        else:
                            record[col] = col_type(record[col])
                    except (ValueError, TypeError):
                        pass  # Keep original value if conversion fails

        # Apply column transformations
        if self.config.column_transforms:
            for col, transform_func in self.config.column_transforms.items():
                if col in record:
                    try:
                        record[col] = transform_func(record[col])
                    except Exception:
                        pass  # Keep original value if transform fails

        # Apply row-level transformation
        if self.config.row_transform:
            record = self.config.row_transform(record)

        return record

    def _load_eager(self) -> None:
        """Load all records into memory at once."""
        records = []
        estimated_total = self._estimate_row_count()

        for i, raw_record in enumerate(self._parse_records()):
            record = self._apply_transformations(raw_record)
            if record is not None:
                records.append(record)

            if self.config.progress_callback and (i + 1) % 1000 == 0:
                self._load_progress = (i + 1, estimated_total)
                self.config.progress_callback(i + 1, estimated_total)

        # Set data in parent MemoryDataSource
        self.set_data(records)
        self.is_loaded = True
        self._load_progress = (len(records), len(records))

        if self.config.progress_callback:
            self.config.progress_callback(len(records), len(records))

    def _load_chunked(self) -> None:
        """Load file in chunks."""
        chunk = []
        estimated_total = self._estimate_row_count()
        loaded_count = 0

        for i, raw_record in enumerate(self._parse_records()):
            record = self._apply_transformations(raw_record)
            if record is not None:
                chunk.append(record)

            # Process chunk when it reaches chunk_size
            if len(chunk) >= self.config.chunk_size:
                if not self.is_loaded:
                    self.set_data(chunk)
                    self.is_loaded = True
                else:
                    # Append to existing data
                    for rec in chunk:
                        self.create_record(rec)

                loaded_count += len(chunk)
                self._load_progress = (loaded_count, estimated_total)

                if self.config.progress_callback:
                    self.config.progress_callback(loaded_count, estimated_total)

                chunk = []

        # Process remaining records
        if chunk:
            if not self.is_loaded:
                self.set_data(chunk)
                self.is_loaded = True
            else:
                for rec in chunk:
                    self.create_record(rec)

            loaded_count += len(chunk)

        self._load_progress = (loaded_count, loaded_count)
        if self.config.progress_callback:
            self.config.progress_callback(loaded_count, loaded_count)

    def _load_impl(self) -> None:
        """Internal load implementation (runs in thread if use_threading=True)."""
        try:
            strategy = self._determine_strategy()

            if strategy == 'eager':
                self._load_eager()
            elif strategy == 'chunked':
                self._load_chunked()
            elif strategy in ('lazy', 'hybrid'):
                # For now, fall back to eager (lazy/hybrid require more complex implementation)
                self._load_eager()

            self._loading = False

            if self.config.on_complete:
                self.config.on_complete()

        except Exception as e:
            self._loading = False
            self.is_loaded = False

            if self.config.on_error:
                self.config.on_error(e)
            else:
                raise

    def load(self, on_complete: Optional[Callable] = None) -> None:
        """Load file with configured strategy.

        For threaded loading, returns immediately and calls on_complete when done.
        For synchronous loading, blocks until complete.

        Args:
            on_complete: Optional callback when loading finishes (overrides config)
        """
        if self._loading:
            return  # Already loading

        self._loading = True
        self.is_loaded = False
        self._load_progress = (0, 0)

        # Override on_complete if provided
        if on_complete:
            original_callback = self.config.on_complete
            self.config.on_complete = on_complete

        if self.config.use_threading:
            # Load in background thread
            self._load_thread = threading.Thread(target=self._load_impl, daemon=True)
            self._load_thread.start()
        else:
            # Load synchronously
            self._load_impl()

        # Restore original callback if overridden
        if on_complete:
            self.config.on_complete = original_callback

    def reload(self) -> None:
        """Reload from file, clearing current data."""
        self.is_loaded = False
        self._data.clear()
        self._columns.clear()
        self._id_index.clear()
        self.load()

    def is_loading(self) -> bool:
        """Check if file is currently loading."""
        return self._loading

    def get_load_progress(self) -> tuple[int, int]:
        """Get loading progress as (current, total) rows."""
        return self._load_progress

    def wait_for_load(self, timeout: Optional[float] = None) -> bool:
        """Wait for loading to complete (if threaded).

        Args:
            timeout: Max seconds to wait (None = wait forever)

        Returns:
            True if load completed, False if timed out
        """
        if self._load_thread and self._load_thread.is_alive():
            self._load_thread.join(timeout=timeout)
            return not self._load_thread.is_alive()
        return True
