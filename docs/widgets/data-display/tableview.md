---
title: TableView
---

# TableView

`TableView` displays **tabular data** with rows and columns.

It is suitable for datasets where users need to scan, sort, and select structured records.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

tv = ttk.TableView(
    app,
    coldata=["Name", "Status"],
    rowdata=[("Item A", "Ready"), ("Item B", "Pending")],
)
tv.pack(fill="both", expand=True)

app.mainloop()
```

---

## Core concepts

- Column definitions
- Row data
- Selection model

---

## Features

- Sorting
- Row selection
- Scrollbars
- Optional headers and footers

---

## Events

TableView emits events for selection, activation, and edits (if enabled).

---

## When should I use TableView?

Use TableView when:

- data is multi-column
- rows are uniform and comparable

Prefer **ListView** when:

- data is simple or visually rich per row

---

## Related widgets

- **TreeView**
- **ListView**
- **ContextMenu**

---

## Reference

- **API Reference:** `ttkbootstrap.TableView`
