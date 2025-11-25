"""
DataSource Demo - Comprehensive example of datasource features

Demonstrates:
- MemoryDataSource and SqliteDataSource
- Data loading and pagination
- Filtering and sorting
- CRUD operations
- Selection management
- CSV export
- Integration with Treeview widget
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.datasource import MemoryDataSource, SqliteDataSource


def create_sample_data():
    """Create sample employee data for demo."""
    return [
        {"name": "Alice Johnson", "age": 30, "department": "Engineering", "salary": 85000},
        {"name": "Bob Smith", "age": 25, "department": "Sales", "salary": 65000},
        {"name": "Charlie Brown", "age": 35, "department": "Engineering", "salary": 95000},
        {"name": "Diana Prince", "age": 28, "department": "Marketing", "salary": 70000},
        {"name": "Eve Adams", "age": 32, "department": "Engineering", "salary": 90000},
        {"name": "Frank Miller", "age": 45, "department": "Sales", "salary": 75000},
        {"name": "Grace Lee", "age": 29, "department": "Marketing", "salary": 68000},
        {"name": "Henry Ford", "age": 38, "department": "Engineering", "salary": 100000},
        {"name": "Iris West", "age": 26, "department": "Sales", "salary": 62000},
        {"name": "Jack Ryan", "age": 41, "department": "Marketing", "salary": 78000},
        {"name": "Karen Hill", "age": 33, "department": "Engineering", "salary": 92000},
        {"name": "Leo King", "age": 27, "department": "Sales", "salary": 64000},
    ]


class DataSourceDemo(ttk.Window):
    def __init__(self):
        super().__init__(title="DataSource Demo", themename="cosmo")
        self.geometry("1000x700")

        # Initialize datasource (using MemoryDataSource for demo)
        self.datasource = MemoryDataSource(page_size=5)
        self.datasource.set_data(create_sample_data())

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        """Setup the user interface."""

        # Main container
        container = ttk.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=YES)

        # Title
        title = ttk.Label(
            container,
            text="DataSource Demo - Employee Management",
            font="heading-lg[bold]",
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))

        # Control panel
        control_frame = ttk.Labelframe(container, text="Controls", padding=10)
        control_frame.pack(fill=X, pady=(0, 10))

        # Filter controls
        filter_frame = ttk.Frame(control_frame)
        filter_frame.pack(fill=X, pady=5)

        ttk.Label(filter_frame, text="Filter:", font="body[bold]").pack(side=LEFT, padx=(0, 10))

        self.filter_var = ttk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=40)
        filter_entry.pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            filter_frame,
            text="Apply Filter",
            command=self.apply_filter,
            bootstyle="info"
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            filter_frame,
            text="Clear",
            command=self.clear_filter,
            bootstyle="secondary-outline"
        ).pack(side=LEFT)

        # Add preset filters
        preset_frame = ttk.Frame(control_frame)
        preset_frame.pack(fill=X, pady=5)

        ttk.Label(preset_frame, text="Presets:", font="caption").pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            preset_frame,
            text="Engineering",
            command=lambda: self.set_preset("department = 'Engineering'"),
            bootstyle="success-outline",
            width=12
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            preset_frame,
            text="Age > 30",
            command=lambda: self.set_preset("age > 30"),
            bootstyle="success-outline",
            width=12
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            preset_frame,
            text="Salary >= 80k",
            command=lambda: self.set_preset("salary >= 80000"),
            bootstyle="success-outline",
            width=12
        ).pack(side=LEFT, padx=2)

        # Sort controls
        sort_frame = ttk.Frame(control_frame)
        sort_frame.pack(fill=X, pady=5)

        ttk.Label(sort_frame, text="Sort:", font="body[bold]").pack(side=LEFT, padx=(0, 10))

        self.sort_var = ttk.StringVar()
        sort_entry = ttk.Entry(sort_frame, textvariable=self.sort_var, width=40)
        sort_entry.pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            sort_frame,
            text="Apply Sort",
            command=self.apply_sort,
            bootstyle="info"
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            sort_frame,
            text="Clear",
            command=self.clear_sort,
            bootstyle="secondary-outline"
        ).pack(side=LEFT)

        # Data display
        data_frame = ttk.Labelframe(container, text="Employee Data", padding=10)
        data_frame.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # Treeview with scrollbar
        tree_frame = ttk.Frame(data_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Create Treeview
        columns = ("id", "name", "age", "department", "salary")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="extended",
            height=10
        )

        # Configure columns
        self.tree.heading("id", text="ID", command=lambda: self.sort_by_column("id"))
        self.tree.heading("name", text="Name", command=lambda: self.sort_by_column("name"))
        self.tree.heading("age", text="Age", command=lambda: self.sort_by_column("age"))
        self.tree.heading("department", text="Department", command=lambda: self.sort_by_column("department"))
        self.tree.heading("salary", text="Salary", command=lambda: self.sort_by_column("salary"))

        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("name", width=150, anchor=W)
        self.tree.column("age", width=60, anchor=CENTER)
        self.tree.column("department", width=120, anchor=W)
        self.tree.column("salary", width=100, anchor=E)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Pagination controls
        pagination_frame = ttk.Frame(data_frame)
        pagination_frame.pack(fill=X, pady=(10, 0))

        self.page_label = ttk.Label(pagination_frame, text="Page 1", font="body")
        self.page_label.pack(side=LEFT, padx=(0, 20))

        ttk.Button(
            pagination_frame,
            text="◄ Previous",
            command=self.prev_page,
            bootstyle="secondary"
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            pagination_frame,
            text="Next ►",
            command=self.next_page,
            bootstyle="secondary"
        ).pack(side=LEFT, padx=2)

        self.count_label = ttk.Label(pagination_frame, text="", font="caption")
        self.count_label.pack(side=RIGHT)

        # Action panel
        action_frame = ttk.Labelframe(container, text="Actions", padding=10)
        action_frame.pack(fill=X)

        # Selection actions
        selection_frame = ttk.Frame(action_frame)
        selection_frame.pack(fill=X, pady=5)

        ttk.Label(selection_frame, text="Selection:", font="body[bold]").pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            selection_frame,
            text="Select All (Page)",
            command=lambda: self.select_all(True),
            bootstyle="success-outline",
            width=15
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            selection_frame,
            text="Select All",
            command=lambda: self.select_all(False),
            bootstyle="success-outline",
            width=15
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            selection_frame,
            text="Unselect All",
            command=lambda: self.unselect_all(False),
            bootstyle="warning-outline",
            width=15
        ).pack(side=LEFT, padx=2)

        self.selection_label = ttk.Label(selection_frame, text="", font="caption")
        self.selection_label.pack(side=RIGHT)

        # CRUD actions
        crud_frame = ttk.Frame(action_frame)
        crud_frame.pack(fill=X, pady=5)

        ttk.Label(crud_frame, text="CRUD:", font="body[bold]").pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            crud_frame,
            text="Add Random Record",
            command=self.add_random_record,
            bootstyle="primary",
            width=18
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            crud_frame,
            text="Delete Selected",
            command=self.delete_selected,
            bootstyle="danger",
            width=15
        ).pack(side=LEFT, padx=2)

        # Export actions
        export_frame = ttk.Frame(action_frame)
        export_frame.pack(fill=X, pady=5)

        ttk.Label(export_frame, text="Export:", font="body[bold]").pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            export_frame,
            text="Export All to CSV",
            command=lambda: self.export_csv(True),
            bootstyle="info",
            width=18
        ).pack(side=LEFT, padx=2)

        ttk.Button(
            export_frame,
            text="Export Selected",
            command=lambda: self.export_csv(False),
            bootstyle="info",
            width=15
        ).pack(side=LEFT, padx=2)

        # Status bar
        self.status_label = ttk.Label(container, text="Ready", font="caption", bootstyle="secondary")
        self.status_label.pack(pady=(10, 0))

        # Bind Enter key to filter/sort entries
        filter_entry.bind('<Return>', lambda e: self.apply_filter())
        sort_entry.bind('<Return>', lambda e: self.apply_sort())

    def refresh_table(self):
        """Refresh the Treeview with current page data."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get current page
        records = self.datasource.get_page()

        # Insert records
        for record in records:
            values = (
                record.get("id", ""),
                record.get("name", ""),
                record.get("age", ""),
                record.get("department", ""),
                f"${record.get('salary', 0):,}"
            )
            item_id = self.tree.insert("", END, values=values)

            # Highlight selected records
            if record.get("selected", 0) == 1:
                self.tree.selection_add(item_id)

        # Update labels
        total = self.datasource.total_count()
        current_page = self.datasource._page + 1
        total_pages = (total + self.datasource.page_size - 1) // self.datasource.page_size

        self.page_label.configure(text=f"Page {current_page} of {total_pages}")
        self.count_label.configure(text=f"Showing {len(records)} of {total} records")

        # Update selection count
        selected_count = self.datasource.selected_count()
        self.selection_label.configure(text=f"{selected_count} selected")

    def apply_filter(self):
        """Apply filter from entry."""
        filter_text = self.filter_var.get().strip()
        try:
            self.datasource.set_filter(filter_text)
            self.datasource._page = 0  # Reset to first page
            self.refresh_table()
            self.status_label.configure(
                text=f"Filter applied: {filter_text}" if filter_text else "Filter cleared",
                bootstyle="success"
            )
        except Exception as e:
            self.status_label.configure(text=f"Filter error: {str(e)}", bootstyle="danger")

    def clear_filter(self):
        """Clear active filter."""
        self.filter_var.set("")
        self.apply_filter()

    def set_preset(self, filter_text: str):
        """Set preset filter."""
        self.filter_var.set(filter_text)
        self.apply_filter()

    def apply_sort(self):
        """Apply sort from entry."""
        sort_text = self.sort_var.get().strip()
        try:
            self.datasource.set_sort(sort_text)
            self.refresh_table()
            self.status_label.configure(
                text=f"Sort applied: {sort_text}" if sort_text else "Sort cleared",
                bootstyle="success"
            )
        except Exception as e:
            self.status_label.configure(text=f"Sort error: {str(e)}", bootstyle="danger")

    def clear_sort(self):
        """Clear active sort."""
        self.sort_var.set("")
        self.apply_sort()

    def sort_by_column(self, column: str):
        """Sort by clicking column header."""
        current_sort = self.sort_var.get()

        # Toggle between ASC and DESC
        if current_sort.startswith(f"{column} ASC"):
            new_sort = f"{column} DESC"
        elif current_sort.startswith(f"{column} DESC"):
            new_sort = ""
        else:
            new_sort = f"{column} ASC"

        self.sort_var.set(new_sort)
        self.apply_sort()

    def next_page(self):
        """Navigate to next page."""
        if self.datasource.has_next_page():
            self.datasource.next_page()
            self.refresh_table()

    def prev_page(self):
        """Navigate to previous page."""
        self.datasource.prev_page()
        self.refresh_table()

    def select_all(self, current_page_only: bool):
        """Select all records."""
        count = self.datasource.select_all(current_page_only=current_page_only)
        self.refresh_table()
        scope = "on current page" if current_page_only else "in dataset"
        self.status_label.configure(
            text=f"Selected {count} records {scope}",
            bootstyle="success"
        )

    def unselect_all(self, current_page_only: bool):
        """Unselect all records."""
        count = self.datasource.unselect_all(current_page_only=current_page_only)
        self.refresh_table()
        self.status_label.configure(text=f"Unselected {count} records", bootstyle="info")

    def add_random_record(self):
        """Add a new random employee record."""
        import random

        names = ["John Doe", "Jane Smith", "Mike Wilson", "Sarah Connor"]
        departments = ["Engineering", "Sales", "Marketing", "HR"]

        new_record = {
            "name": random.choice(names),
            "age": random.randint(25, 50),
            "department": random.choice(departments),
            "salary": random.randint(50000, 120000)
        }

        new_id = self.datasource.create_record(new_record)
        self.refresh_table()
        self.status_label.configure(
            text=f"Created record ID {new_id}: {new_record['name']}",
            bootstyle="success"
        )

    def delete_selected(self):
        """Delete all selected records."""
        selected = self.datasource.get_selected()
        if not selected:
            self.status_label.configure(text="No records selected", bootstyle="warning")
            return

        count = 0
        for record in selected:
            if self.datasource.delete_record(record["id"]):
                count += 1

        self.refresh_table()
        self.status_label.configure(
            text=f"Deleted {count} records",
            bootstyle="danger"
        )

    def export_csv(self, include_all: bool):
        """Export data to CSV."""
        from tkinter import filedialog

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filepath:
            self.datasource.export_to_csv(filepath, include_all=include_all)
            scope = "all records" if include_all else "selected records"
            self.status_label.configure(
                text=f"Exported {scope} to {filepath}",
                bootstyle="success"
            )


def main():
    """Run the datasource demo."""
    app = DataSourceDemo()

    # Print usage instructions
    print("=" * 60)
    print("DataSource Demo - Usage Instructions")
    print("=" * 60)
    print("\nFiltering Examples:")
    print("  department = 'Engineering'")
    print("  age > 30")
    print("  salary >= 80000")
    print("  name CONTAINS 'son'")
    print("  department = 'Engineering' AND age > 30")
    print("\nSorting Examples:")
    print("  name ASC")
    print("  age DESC")
    print("  department ASC, salary DESC")
    print("\nFeatures:")
    print("  - Click column headers to sort")
    print("  - Use preset filters for quick access")
    print("  - Select/unselect records (per page or all)")
    print("  - Add random records to test pagination")
    print("  - Export to CSV (all or selected only)")
    print("=" * 60)

    app.mainloop()


if __name__ == "__main__":
    main()