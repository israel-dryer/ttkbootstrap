# FileSourceConfig

Configuration for [FileDataSource](FileDataSource.md) loading and transformations.

See the [DataSource Guide](../../guides/datasource.md) for usage examples.

## Attribute Categories

| Category | Attributes |
|----------|------------|
| **File Format** | `file_format`, `encoding` |
| **CSV/TSV** | `delimiter`, `quotechar`, `skip_rows`, `header_row`, `has_header` |
| **JSON** | `json_lines`, `json_orient` |
| **Column Transforms** | `column_renames`, `column_types`, `column_transforms`, `columns_to_load`, `default_values` |
| **Row Processing** | `row_filter`, `row_transform` |
| **Large Files** | `loading_strategy`, `chunk_size`, `max_memory_rows` |
| **Threading** | `use_threading`, `progress_callback`, `on_complete`, `on_error` |

---

## Class Attributes

### File Format

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_format` | `Literal['auto', 'csv', 'tsv', 'json', 'jsonl']` | `'auto'` | Format type - auto-detected from extension if 'auto'. |
| `encoding` | `str` | `'utf-8'` | Character encoding for reading the file. |

### CSV/TSV

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `delimiter` | `Optional[str]` | `None` | Field separator (None = auto-detect). |
| `quotechar` | `str` | `'"'` | Quote character for fields containing the delimiter. |
| `skip_rows` | `int` | `0` | Number of header rows to skip. |
| `header_row` | `Optional[int]` | `0` | Row index containing column names (None = no header). |
| `has_header` | `bool` | `True` | Whether the first row contains column names. |

### JSON

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `json_lines` | `bool` | `False` | True for line-delimited JSON (JSONL/NDJSON format). |
| `json_orient` | `Literal['records', 'index', 'columns', 'values']` | `'records'` | Pandas-like orientation for JSON arrays. |

### Column Transforms

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `column_renames` | `Optional[Dict[str, str]]` | `None` | Map {old_name: new_name} for renaming columns. |
| `column_types` | `Optional[Dict[str, type]]` | `None` | Map {column: type} for type conversions. |
| `column_transforms` | `Optional[Dict[str, Callable]]` | `None` | Map {column: func} for custom transformations. |
| `columns_to_load` | `Optional[List[str]]` | `None` | List of columns to load (None = all columns). |
| `default_values` | `Optional[Dict[str, Any]]` | `None` | Map {column: value} for missing/null values. |

### Row Processing

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `row_filter` | `Optional[Callable[[Dict], bool]]` | `None` | Function(row_dict) -> bool to filter rows during load. |
| `row_transform` | `Optional[Callable[[Dict], Dict]]` | `None` | Function(row_dict) -> row_dict for row-level transforms. |

### Large Files

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `loading_strategy` | `Literal['eager', 'lazy', 'chunked', 'hybrid', 'auto']` | `'auto'` | How to load file. |
| `chunk_size` | `int` | `10000` | Rows per chunk for chunked/lazy loading. |
| `max_memory_rows` | `int` | `100000` | Threshold for auto-switching loading strategies. |

### Threading

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_threading` | `bool` | `False` | Load file in background thread (non-blocking). |
| `progress_callback` | `Optional[Callable[[int, int], None]]` | `None` | Function(current, total) called during load. |
| `on_complete` | `Optional[Callable[[], None]]` | `None` | Function() called when loading completes. |
| `on_error` | `Optional[Callable[[Exception], None]]` | `None` | Function(exception) called if loading fails. |

---

::: ttkbootstrap.datasource.file_source.FileSourceConfig
    options:
      show_docstring_description: true
      show_docstring_examples: true
      show_docstring_attributes: false
      members: false
