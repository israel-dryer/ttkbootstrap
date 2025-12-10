"""FileDataSource interactive demo with Treeview integration.

Demonstrates FileDataSource capabilities:
- Loading CSV and JSON files
- Transformation pipeline (column renaming, type conversion, filtering)
- Loading strategies (eager, chunked, lazy)
- Progress callbacks
- Filtering and sorting
- Pagination
- CRUD operations
- Integration with ttkbootstrap widgets
"""

import csv
import json
import os
import random
import tempfile
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.datasource import FileDataSource, FileSourceConfig


# Sample data generator
def generate_sample_data(count=100):
    """Generate sample employee data."""
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
    statuses = ['active', 'inactive', 'on_leave']
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']

    data = []
    for i in range(count):
        data.append({
            'employee_id': f'EMP{i:04d}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'age': random.randint(22, 65),
            'department': random.choice(departments),
            'salary': random.randint(40000, 150000),
            'status': random.choice(statuses),
            'years_exp': random.randint(0, 30)
        })
    return data


# Create sample files for the demo
def create_sample_files():
    """Create temporary sample CSV and JSON files."""
    temp_dir = Path(tempfile.gettempdir())

    # Generate sample data
    data = generate_sample_data(100)

    # Create CSV file
    csv_path = temp_dir / 'employees.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    # Create JSON file
    json_path = temp_dir / 'employees.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Create JSONL file
    jsonl_path = temp_dir / 'employees.jsonl'
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write(json.dumps(record) + '\n')

    # Create large CSV for testing chunked loading
    large_data = generate_sample_data(500)
    large_csv_path = temp_dir / 'employees_large.csv'
    with open(large_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=large_data[0].keys())
        writer.writeheader()
        writer.writerows(large_data)

    return csv_path, json_path, jsonl_path, large_csv_path


class FileDataSourceDemo:
    """Demo application for FileDataSource."""

    def __init__(self, root):
        self.root = root
        self.root.title("FileDataSource Demo")
        self.root.geometry("1200x800")

        # Create sample files
        self.csv_file, self.json_file, self.jsonl_file, self.large_csv = create_sample_files()

        # Data source
        self.datasource = None

        # UI Setup
        self._create_layout()

        # Load default file
        self.load_csv_basic()

    def _create_layout(self):
        """Create the UI layout."""
        # Main container
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=BOTH, expand=YES)

        # Control panel
        control_frame = ttk.LabelFrame(main, text="File Loading Options", padding=10)
        control_frame.pack(fill=X, padx=5, pady=5)

        self._create_controls(control_frame)

        # Data display
        data_frame = ttk.LabelFrame(main, text="Data View", padding=10)
        data_frame.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        self._create_treeview(data_frame)

        # Status and pagination
        bottom_frame = ttk.Frame(main)
        bottom_frame.pack(fill=X, padx=5, pady=5)

        self._create_pagination(bottom_frame)
        self._create_status(bottom_frame)

    def _create_controls(self, parent):
        """Create control buttons."""
        # File type buttons
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=X, pady=5)

        ttk.Label(file_frame, text="Load File:").pack(side=LEFT, padx=5)
        ttk.Button(file_frame, text="CSV (Basic)", command=self.load_csv_basic, bootstyle=PRIMARY).pack(side=LEFT, padx=2)
        ttk.Button(file_frame, text="CSV (Transformed)", command=self.load_csv_transformed, bootstyle=INFO).pack(side=LEFT, padx=2)
        ttk.Button(file_frame, text="JSON", command=self.load_json, bootstyle=SUCCESS).pack(side=LEFT, padx=2)
        ttk.Button(file_frame, text="JSONL", command=self.load_jsonl, bootstyle=WARNING).pack(side=LEFT, padx=2)
        ttk.Button(file_frame, text="Large CSV (Chunked)", command=self.load_large_csv, bootstyle=DANGER).pack(side=LEFT, padx=2)

        # Filter presets
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=X, pady=5)

        ttk.Label(filter_frame, text="Filter:").pack(side=LEFT, padx=5)
        ttk.Button(filter_frame, text="All", command=lambda: self.apply_filter(""), bootstyle=SECONDARY).pack(side=LEFT, padx=2)
        ttk.Button(filter_frame, text="Engineering", command=lambda: self.apply_filter("department = 'Engineering'")).pack(side=LEFT, padx=2)
        ttk.Button(filter_frame, text="Age > 40", command=lambda: self.apply_filter("age > 40")).pack(side=LEFT, padx=2)
        ttk.Button(filter_frame, text="Salary > 80k", command=lambda: self.apply_filter("salary > 80000")).pack(side=LEFT, padx=2)
        ttk.Button(filter_frame, text="Active Only", command=lambda: self.apply_filter("status = 'active'")).pack(side=LEFT, padx=2)

        # Sort options
        sort_frame = ttk.Frame(parent)
        sort_frame.pack(fill=X, pady=5)

        ttk.Label(sort_frame, text="Sort:").pack(side=LEFT, padx=5)
        ttk.Button(sort_frame, text="Name ↑", command=lambda: self.apply_sort("last_name ASC")).pack(side=LEFT, padx=2)
        ttk.Button(sort_frame, text="Age ↑", command=lambda: self.apply_sort("age ASC")).pack(side=LEFT, padx=2)
        ttk.Button(sort_frame, text="Salary ↓", command=lambda: self.apply_sort("salary DESC")).pack(side=LEFT, padx=2)
        ttk.Button(sort_frame, text="Department ↑", command=lambda: self.apply_sort("department ASC")).pack(side=LEFT, padx=2)

        # Custom filter/sort
        custom_frame = ttk.Frame(parent)
        custom_frame.pack(fill=X, pady=5)

        ttk.Label(custom_frame, text="Custom Filter:").pack(side=LEFT, padx=5)
        self.filter_entry = ttk.Entry(custom_frame, width=30)
        self.filter_entry.pack(side=LEFT, padx=2)
        self.filter_entry.bind('<Return>', lambda e: self.apply_filter(self.filter_entry.get()))

        ttk.Label(custom_frame, text="Custom Sort:").pack(side=LEFT, padx=10)
        self.sort_entry = ttk.Entry(custom_frame, width=20)
        self.sort_entry.pack(side=LEFT, padx=2)
        self.sort_entry.bind('<Return>', lambda e: self.apply_sort(self.sort_entry.get()))

        # Progress bar
        self.progress_var = ttk.IntVar()
        self.progress = ttk.Progressbar(parent, variable=self.progress_var, maximum=100, bootstyle="success-striped")
        self.progress.pack(fill=X, pady=5)

    def _create_treeview(self, parent):
        """Create the treeview widget."""
        # Treeview with scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        vsb.pack(side=RIGHT, fill=Y)

        hsb = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        hsb.pack(side=BOTTOM, fill=X)

        # Treeview
        self.tree = ttk.TreeView(
            tree_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            bootstyle=INFO,
            show='tree headings'
        )
        self.tree.pack(fill=BOTH, expand=YES)

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Enable column sorting by clicking headers
        self.tree.bind('<Button-1>', self._on_tree_click)

    def _create_pagination(self, parent):
        """Create pagination controls."""
        pag_frame = ttk.Frame(parent)
        pag_frame.pack(side=LEFT, padx=5)

        ttk.Button(pag_frame, text="⏮ First", command=self.first_page, width=8).pack(side=LEFT, padx=2)
        ttk.Button(pag_frame, text="◀ Prev", command=self.prev_page, width=8).pack(side=LEFT, padx=2)

        self.page_label = ttk.Label(pag_frame, text="Page: 0 / 0")
        self.page_label.pack(side=LEFT, padx=10)

        ttk.Button(pag_frame, text="Next ▶", command=self.next_page, width=8).pack(side=LEFT, padx=2)
        ttk.Button(pag_frame, text="Last ⏭", command=self.last_page, width=8).pack(side=LEFT, padx=2)

        # Page size
        ttk.Label(pag_frame, text="Page size:").pack(side=LEFT, padx=10)
        self.page_size_var = ttk.IntVar(value=25)
        page_size_spin = ttk.Spinbox(
            pag_frame,
            from_=10,
            to=100,
            increment=5,
            textvariable=self.page_size_var,
            width=10,
            command=self.change_page_size
        )
        page_size_spin.pack(side=LEFT, padx=2)

    def _create_status(self, parent):
        """Create status display."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(side=RIGHT, padx=5)

        self.status_label = ttk.Label(status_frame, text="Ready", bootstyle=INFO)
        self.status_label.pack()

    def _setup_treeview_columns(self, columns):
        """Setup treeview columns based on datasource columns."""
        # Clear existing
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = columns

        # Configure columns
        self.tree.column('#0', width=50, stretch=NO)
        self.tree.heading('#0', text='#')

        for col in columns:
            self.tree.column(col, width=100, anchor=W)
            self.tree.heading(col, text=col.replace('_', ' ').title())

    def _update_treeview(self):
        """Update treeview with current page data."""
        if not self.datasource or not self.datasource.is_loaded:
            return

        # Clear tree
        self.tree.delete(*self.tree.get_children())

        # Get current page
        records = self.datasource.get_page()

        if not records:
            self._update_status("No records to display")
            return

        # Setup columns if needed
        columns = list(records[0].keys())
        if 'selected' in columns:
            columns.remove('selected')
        if 'id' in columns:
            columns.remove('id')

        self.tree['columns'] = columns

        # Configure columns
        self.tree.column('#0', width=50, stretch=NO)
        self.tree.heading('#0', text='ID')

        for col in columns:
            self.tree.column(col, width=120, anchor=W)
            self.tree.heading(col, text=col.replace('_', ' ').title())

        # Insert records
        for record in records:
            record_id = record.get('id', '')
            values = [record.get(col, '') for col in columns]
            self.tree.insert('', END, text=record_id, values=values)

        # Update pagination display
        self._update_pagination_display()

        # Update status
        total = self.datasource.total_count()
        filtered = len(records)
        page = self.datasource._page + 1
        self._update_status(f"Showing {filtered} records (Total: {total}, Page: {page})")

    def _update_pagination_display(self):
        """Update pagination label."""
        if not self.datasource:
            return

        current_page = self.datasource._page + 1
        total_pages = (self.datasource.total_count() + self.datasource.page_size - 1) // self.datasource.page_size
        total_pages = max(1, total_pages)

        self.page_label.config(text=f"Page: {current_page} / {total_pages}")

    def _update_status(self, message):
        """Update status label."""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def _progress_callback(self, current, total):
        """Progress callback for threaded loading."""
        if total > 0:
            percent = int((current / total) * 100)
            self.progress_var.set(percent)
            self._update_status(f"Loading: {current}/{total} ({percent}%)")

    def _on_complete(self):
        """Called when file loading completes."""
        self.progress_var.set(100)
        self._update_treeview()
        self._update_status(f"Loaded {self.datasource.total_count()} records successfully")

    def _on_tree_click(self, event):
        """Handle tree header clicks for sorting."""
        region = self.tree.identify_region(event.x, event.y)
        if region == 'heading':
            col_id = self.tree.identify_column(event.x)
            if col_id != '#0':  # Not the ID column
                col_index = int(col_id.replace('#', '')) - 1
                columns = self.tree['columns']
                if col_index < len(columns):
                    col_name = columns[col_index]
                    # Toggle sort direction
                    current_sort = self.sort_entry.get()
                    if col_name in current_sort and 'DESC' not in current_sort:
                        sort_expr = f"{col_name} DESC"
                    else:
                        sort_expr = f"{col_name} ASC"
                    self.apply_sort(sort_expr)

    # File loading methods
    def load_csv_basic(self):
        """Load CSV with basic configuration."""
        self._update_status("Loading CSV (basic)...")

        self.datasource = FileDataSource(
            self.csv_file,
            page_size=self.page_size_var.get()
        )
        self.datasource.load()
        self._on_complete()

    def load_csv_transformed(self):
        """Load CSV with transformations."""
        self._update_status("Loading CSV with transformations...")

        config = FileSourceConfig(
            column_renames={
                'employee_id': 'id',
                'first_name': 'first',
                'last_name': 'last',
                'years_exp': 'experience'
            },
            column_types={
                'age': int,
                'salary': float,
                'experience': int
            },
            column_transforms={
                'first': str.title,
                'last': str.title,
                'department': str.upper
            },
            row_filter=lambda r: r.get('status') == 'active',
            default_values={'experience': 0}
        )

        self.datasource = FileDataSource(
            self.csv_file,
            config=config,
            page_size=self.page_size_var.get()
        )
        self.datasource.load()
        self._on_complete()

    def load_json(self):
        """Load JSON file."""
        self._update_status("Loading JSON...")

        self.datasource = FileDataSource(
            self.json_file,
            page_size=self.page_size_var.get()
        )
        self.datasource.load()
        self._on_complete()

    def load_jsonl(self):
        """Load JSONL file."""
        self._update_status("Loading JSONL...")

        config = FileSourceConfig(json_lines=True)

        self.datasource = FileDataSource(
            self.jsonl_file,
            config=config,
            page_size=self.page_size_var.get()
        )
        self.datasource.load()
        self._on_complete()

    def load_large_csv(self):
        """Load large CSV with chunked strategy and progress."""
        self._update_status("Loading large CSV with progress...")
        self.progress_var.set(0)

        config = FileSourceConfig(
            loading_strategy='chunked',
            chunk_size=100,
            use_threading=False,  # Use sync for demo simplicity
            progress_callback=self._progress_callback
        )

        self.datasource = FileDataSource(
            self.large_csv,
            config=config,
            page_size=self.page_size_var.get()
        )
        self.datasource.load()
        self._on_complete()

    # Filter and sort
    def apply_filter(self, filter_expr):
        """Apply filter to datasource."""
        if not self.datasource or not self.datasource.is_loaded:
            return

        self.filter_entry.delete(0, END)
        self.filter_entry.insert(0, filter_expr)

        self.datasource.set_filter(filter_expr)
        self.datasource._page = 0  # Reset to first page
        self._update_treeview()

        if filter_expr:
            self._update_status(f"Filter applied: {filter_expr}")
        else:
            self._update_status("Filter cleared")

    def apply_sort(self, sort_expr):
        """Apply sort to datasource."""
        if not self.datasource or not self.datasource.is_loaded:
            return

        self.sort_entry.delete(0, END)
        self.sort_entry.insert(0, sort_expr)

        self.datasource.set_sort(sort_expr)
        self._update_treeview()
        self._update_status(f"Sort applied: {sort_expr}")

    # Pagination
    def first_page(self):
        """Go to first page."""
        if self.datasource and self.datasource.is_loaded:
            self.datasource.get_page(0)
            self._update_treeview()

    def prev_page(self):
        """Go to previous page."""
        if self.datasource and self.datasource.is_loaded:
            self.datasource.prev_page()
            self._update_treeview()

    def next_page(self):
        """Go to next page."""
        if self.datasource and self.datasource.is_loaded:
            if self.datasource.has_next_page():
                self.datasource.next_page()
                self._update_treeview()

    def last_page(self):
        """Go to last page."""
        if self.datasource and self.datasource.is_loaded:
            total = self.datasource.total_count()
            last_page = (total - 1) // self.datasource.page_size
            self.datasource.get_page(last_page)
            self._update_treeview()

    def change_page_size(self):
        """Change page size."""
        if self.datasource and self.datasource.is_loaded:
            self.datasource.page_size = self.page_size_var.get()
            self.datasource._page = 0  # Reset to first page
            self._update_treeview()


if __name__ == '__main__':
    app = ttk.Window(theme="superhero")
    demo = FileDataSourceDemo(app)

    # Cleanup temp files on close
    def on_closing():
        try:
            os.unlink(demo.csv_file)
            os.unlink(demo.json_file)
            os.unlink(demo.jsonl_file)
            os.unlink(demo.large_csv)
        except:
            pass
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)

    app.update_idletasks()
    app.mainloop()
