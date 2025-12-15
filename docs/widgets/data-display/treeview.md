---
title: TreeView
icon: fontawesome/solid/folder-tree
---

# TreeView

`TreeView` displays hierarchical or tabular data.

In ttkbootstrap v2, `TreeView` is a wrapper around Tkinter's `ttk.Treeview` that keeps the familiar API but adds a few "app-ready" conveniences:

- **Bootstyle tokens** (`bootstyle="primary"`, `bootstyle="success"`, etc.)
- **Surface-aware** styling via `surface_color=...` (or inherit from the parent surface)
- **Style options** for customization (borders, icons, selection colors, etc.)

Use `TreeView` for file browsers, hierarchical data, or tabular displays with columns and headings.

> _Image placeholder:_
> `![TreeView variants](../_img/widgets/treeview/overview.png)`
> Suggested shot: tree view with hierarchy + table view with columns.

---

## Basic usage

### Table with headings

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.TreeView(
    app,
    columns=("size", "modified"),
    show="headings",
    height=8,
)
tree.heading("size", text="Size")
tree.heading("modified", text="Modified")

tree.insert("", "end", values=("1.2 MB", "Jan 1"))
tree.insert("", "end", values=("512 KB", "Jan 2"))
tree.insert("", "end", values=("2.5 MB", "Jan 3"))

tree.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

### Hierarchical tree

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.TreeView(app, show="tree")
tree.pack(fill="both", expand=True, padx=20, pady=20)

# Add parent items
folder1 = tree.insert("", "end", text="Documents")
folder2 = tree.insert("", "end", text="Pictures")

# Add child items
tree.insert(folder1, "end", text="report.pdf")
tree.insert(folder1, "end", text="notes.txt")
tree.insert(folder2, "end", text="photo.jpg")

app.mainloop()
```

---

## Common options

### `columns` and `displaycolumns`

Define columns for tabular data.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Define columns
tree = ttk.TreeView(
    app,
    columns=("name", "email", "role"),
    show="headings",
)

# Set column headings
tree.heading("name", text="Name")
tree.heading("email", text="Email")
tree.heading("role", text="Role")

# Configure column widths
tree.column("name", width=150)
tree.column("email", width=200)
tree.column("role", width=100)

# Insert data
tree.insert("", "end", values=("Alice", "alice@example.com", "Admin"))
tree.insert("", "end", values=("Bob", "bob@example.com", "User"))

tree.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

Use `displaycolumns` to show a subset or reorder columns:

```python
tree = ttk.TreeView(
    app,
    columns=("name", "email", "role"),
    displaycolumns=("name", "role"),  # Hide email column
    show="headings",
)
```

### `show`

Control which parts of the tree to display.

```python
# Show only headings (table mode)
tree = ttk.TreeView(app, columns=("col1", "col2"), show="headings")

# Show only tree (hierarchy mode)
tree = ttk.TreeView(app, show="tree")

# Show both tree and headings (default)
tree = ttk.TreeView(app, columns=("col1", "col2"), show="tree headings")
```

### `height`

Set the number of visible rows.

```python
tree = ttk.TreeView(app, height=10)  # Show 10 rows
```

### `selectmode`

Control selection behavior.

```python
# Single selection (default)
tree = ttk.TreeView(app, selectmode="browse")

# Multiple selection
tree = ttk.TreeView(app, selectmode="extended")

# No selection
tree = ttk.TreeView(app, selectmode="none")
```

---

## Working with items

### Insert items

```python
# Insert at the end
tree.insert("", "end", text="Item 1", values=("Value 1", "Value 2"))

# Insert at a specific position
tree.insert("", 0, text="First Item")

# Insert as a child
parent_id = tree.insert("", "end", text="Parent")
tree.insert(parent_id, "end", text="Child")
```

### Get selected items

```python
selected = tree.selection()  # Returns tuple of item IDs
for item_id in selected:
    item_data = tree.item(item_id)
    print(item_data["text"], item_data["values"])
```

### Update items

```python
tree.item(item_id, text="New Text", values=("New", "Values"))
```

### Delete items

```python
tree.delete(item_id)

# Delete all items
tree.delete(*tree.get_children())
```

---

## Bootstyle variants

Use bootstyle color tokens to change the selection color.

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.TreeView(
    app,
    columns=("col1", "col2"),
    show="headings",
    bootstyle="success",  # Green selection
    height=6,
)
tree.heading("col1", text="Column 1")
tree.heading("col2", text="Column 2")

tree.insert("", "end", values=("Row 1", "Data 1"))
tree.insert("", "end", values=("Row 2", "Data 2"))

tree.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

Available bootstyle colors:  

- `primary` (default)
- `secondary`
- `success`
- `info`
- `warning`
- `danger`
- `dark`
- `light`

> _Image placeholder:_
> `![TreeView bootstyles](../_img/widgets/treeview/bootstyles.png)`
> (Show treeviews with different selection colors.)

---

## Style options

Use `style_options` to customize appearance.

### Hide borders

```python
tree = ttk.TreeView(
    app,
    columns=("col1", "col2"),
    show="headings",
    style_options={"show_border": False},
)
```

### Custom border color

```python
tree = ttk.TreeView(
    app,
    style_options={"border_color": "primary"},
)
```

### Custom selection background

```python
tree = ttk.TreeView(
    app,
    style_options={"select_background": "success"},
)
```

### Custom header background

```python
tree = ttk.TreeView(
    app,
    style_options={"header_background": "primary"},
)
```

### Custom expand/collapse icons

```python
tree = ttk.TreeView(
    app,
    style_options={
        "open_icon": "plus-square",
        "close_icon": "dash-square",
    },
)
```

---

## Tags for custom styling

Use tags to style individual rows or cells.

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.TreeView(app, columns=("status",), show="tree headings")
tree.heading("status", text="Status")
tree.pack(fill="both", expand=True, padx=20, pady=20)

# Configure tags with custom colors
tree.tag_configure("success", background="#d4edda", foreground="#155724")
tree.tag_configure("error", background="#f8d7da", foreground="#721c24")

# Insert items with tags
tree.insert("", "end", text="Task 1", values=("Complete",), tags=("success",))
tree.insert("", "end", text="Task 2", values=("Failed",), tags=("error",))
tree.insert("", "end", text="Task 3", values=("Pending",))

app.mainloop()
```

---

## Events

### `<<TreeviewSelect>>`

Triggered when selection changes.

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.TreeView(app, columns=("data",), show="headings")
tree.heading("data", text="Data")
tree.insert("", "end", values=("Item 1",))
tree.insert("", "end", values=("Item 2",))
tree.pack(fill="both", expand=True, padx=20, pady=20)

def on_select(event):
    selected = tree.selection()
    for item_id in selected:
        print(tree.item(item_id)["values"])

tree.bind("<<TreeviewSelect>>", on_select)

app.mainloop()
```

### `<<TreeviewOpen>>` and `<<TreeviewClose>>`

Triggered when items are expanded or collapsed.

```python
def on_open(event):
    item_id = tree.focus()
    print(f"Opened: {tree.item(item_id)['text']}")

def on_close(event):
    item_id = tree.focus()
    print(f"Closed: {tree.item(item_id)['text']}")

tree.bind("<<TreeviewOpen>>", on_open)
tree.bind("<<TreeviewClose>>", on_close)
```

### Double-click

```python
def on_double_click(event):
    item_id = tree.focus()
    print(f"Double-clicked: {tree.item(item_id)['text']}")

tree.bind("<Double-1>", on_double_click)
```

---

## Scrollbars

Add scrollbars for large datasets.

```python
import ttkbootstrap as ttk

app = ttk.App()

container = ttk.Frame(app)
container.pack(fill="both", expand=True, padx=20, pady=20)

# Create scrollbars
vsb = ttk.Scrollbar(container, orient="vertical")
hsb = ttk.Scrollbar(container, orient="horizontal")

# Create treeview
tree = ttk.TreeView(
    container,
    columns=("col1", "col2", "col3"),
    show="headings",
    yscrollcommand=vsb.set,
    xscrollcommand=hsb.set,
)
tree.heading("col1", text="Column 1")
tree.heading("col2", text="Column 2")
tree.heading("col3", text="Column 3")

# Configure scrollbars
vsb.config(command=tree.yview)
hsb.config(command=tree.xview)

# Grid layout
tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")

container.rowconfigure(0, weight=1)
container.columnconfigure(0, weight=1)

# Add sample data
for i in range(50):
    tree.insert("", "end", values=(f"Row {i}", f"Data {i}", f"Value {i}"))

app.mainloop()
```

---

## When should I use TreeView?

Use `TreeView` when:

- displaying hierarchical data (file systems, organization charts, nested categories)
- showing tabular data with sortable columns
- building file browsers or data explorers
- you need low-level control over rows and columns

Prefer other widgets when:

- **TableView** — for full-featured data grids with built-in filtering, sorting, and paging
- **SelectBox** — for simple dropdown selection from a list
- **Label** — for static text display

---

## Related widgets

- **TableView** — full-featured data grid
- **SelectBox** — dropdown selection
- **Scrollbar** — add scrolling to large trees