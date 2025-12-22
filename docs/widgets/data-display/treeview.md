---
title: TreeView
---

# TreeView

`TreeView` displays **hierarchical data** in an expandable tree structure.

It’s ideal for representing parent/child relationships like folders, categories, or outlines.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

tree = ttk.Treeview(app)
tree.pack(fill="both", expand=True)

tree.insert("", "end", text="Root")
app.mainloop()
```

---

## Core concepts

- Items and parents
- Expand/collapse state
- Selection and focus

---

## Common patterns

- File browsers
- Category navigation
- Outline views

---

## When should I use TreeView?

Use TreeView when:

- data has a natural hierarchy

Prefer **TableView** when:

- data is flat and column-based

---

## Related widgets

- **TableView**
- **ListView**
- **ScrollView**

---

## Reference

- **API Reference:** `ttkbootstrap.TreeView`
