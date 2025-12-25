---
title: TreeView
---

# TreeView

`TreeView` displays **hierarchical data** in an expandable tree structure.

It's ideal for representing parent/child relationships like folders, categories, or outlines.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.Treeview(app)
tree.pack(fill="both", expand=True)

tree.insert("", "end", text="Root")
app.mainloop()
```

---

## When to use

Use TreeView when:

- data has a natural hierarchy

- users need to navigate parent/child relationships

- content can be expanded and collapsed

### Consider a different control when...

- **Data is flat and column-based** — use [TableView](tableview.md) instead

- **Data is a simple list without hierarchy** — use [ListView](listview.md) instead

- **You only need to display a single value** — use [Label](label.md) or [Badge](badge.md)

---

## Appearance

### Styling

TreeView supports theming through ttkbootstrap:

```python
ttk.Treeview(app, bootstyle="primary")
```

!!! link "Design System"
    See [Design System](../../design-system/index.md) for color tokens and theming guidelines.

---

## Examples & patterns

### Core concepts

- **Items and parents** — each item can have a parent and children

- **Expand/collapse state** — branches can be opened or closed

- **Selection and focus** — items can be selected and focused

### Building a tree

```python
tree = ttk.Treeview(app)
tree.pack(fill="both", expand=True)

# Insert root item
root = tree.insert("", "end", text="Documents")

# Insert children
tree.insert(root, "end", text="Report.pdf")
tree.insert(root, "end", text="Notes.txt")

# Insert nested folder
subfolder = tree.insert(root, "end", text="Images")
tree.insert(subfolder, "end", text="photo.jpg")
```

### Common patterns

- **File browsers** — navigate folder structures

- **Category navigation** — browse hierarchical categories

- **Outline views** — display document outlines

### With columns

```python
tree = ttk.Treeview(app, columns=("size", "modified"))
tree.heading("#0", text="Name")
tree.heading("size", text="Size")
tree.heading("modified", text="Modified")

tree.insert("", "end", text="file.txt", values=("10 KB", "2024-01-15"))
```

### Common options

- `columns` — additional columns beyond the tree column

- `show` — what to display (`"tree"`, `"headings"`, or both)

- `selectmode` — selection behavior (`"browse"`, `"extended"`, `"none"`)

- `height` — number of visible rows

---

## Behavior

### Events

TreeView emits events for user interactions:

- `<<TreeviewSelect>>` — selection changed

- `<<TreeviewOpen>>` — item expanded

- `<<TreeviewClose>>` — item collapsed

```python
def on_select(event):
    selected = tree.selection()
    print("Selected:", selected)

tree.bind("<<TreeviewSelect>>", on_select)
```

### Item operations

```python
# Get selected items
selected = tree.selection()

# Expand/collapse
tree.item(item_id, open=True)
tree.item(item_id, open=False)

# Get item data
data = tree.item(item_id)

# Delete item
tree.delete(item_id)
```

---

## Reactivity

TreeView can be updated dynamically:

```python
# Clear and rebuild
for item in tree.get_children():
    tree.delete(item)

# Add new items
for item in new_data:
    tree.insert("", "end", text=item["name"])
```

!!! link "Signals"
    See [Signals](../../concepts/signals.md) for reactive programming patterns.

---

## Additional resources

### Related widgets

- [TableView](tableview.md) — tabular record display

- [ListView](listview.md) — virtual scrolling list

- [ScrollView](../layout/scrollview.md) — scrolling containers

### Framework concepts

- [Design System](../../design-system/index.md) — colors, typography, and theming

- [Signals](../../concepts/signals.md) — reactive data binding

### API reference

- [`ttkbootstrap.TreeView`](../../reference/widgets/TreeView.md)