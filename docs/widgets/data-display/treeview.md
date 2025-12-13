---
title: TreeView
icon: fontawesome/solid/folder-tree
---


# TreeView

`TreeView` wraps `ttk.Treeview` with bootstyle tokens, surface colors, and optional style overrides so you can render hierarchical or tabular data that matches the rest of your themed UI.

---

## Overview

Key capabilities:

- Configure columns (`columns`, `displaycolumns`, `show`) to mix a tree hierarchy with heading-based columns.
- Use `selectmode` (`browse`, `extended`, `none`) to control selection behavior.
- Apply `bootstyle`, `surface_color`, and `style_options` for consistent colors and typography without writing raw styles.
- `height`, `padding`, and `cursor` mirror normal `ttk.Treeview` options so the widget fits into any layout.
- Events such as `<<TreeviewSelect>>` remain available and work the same way as with native `ttk`.

TreeView is ideal for file browsers, settings tables, or master-detail presentations.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

tree = ttk.TreeView(
    app,
    columns=("size", "modified"),
    show="headings",
    bootstyle="secondary",
    height=8,
)
tree.heading("size", text="Size")
tree.heading("modified", text="Modified")
tree.insert("", "end", text="Report.pdf", values=("1.2 MB", "Jan 1"))
tree.insert("", "end", text="Image.png", values=("512 KB", "Jan 2"))
tree.pack(fill="both", expand=True, padx=16, pady=16)

app.mainloop()
```

---

## Styling & customization

- Pair `bootstyle` with `surface_color` to paint the row background or track in your theme palette.
- Use `style_options` to pass builder-specific tokens for advanced tweaks (e.g., `{"focuscolor": "primary"}`).
- Combine `padding`, `cursor`, `font`, or `height` to tune density.
- Provide `displaycolumns` when you need to show a subset or re-order columns differently from your internal data model.

---

## Selection & events

- TreeView emits standard Tk virtual events such as `<<TreeviewSelect>>`, `<<TreeviewOpen>>`, and `<<TreeviewClose>>`.
- Read selected items with `tree.selection()` and fetch data via `tree.item(item_id)`.
- Use `selectmode="extended"` for multi-select lists or `selectmode="browse"` for single selection.
- Customize click handling by binding `<Double-1>` or `<<TreeviewSelect>>` to your handlers.

---

## When to use TreeView

Choose `TreeView` for hierarchical lists (file explorers, category trees) or when you need grid-style columns rendered with ttk theme support. It pairs well with `Label`/`Button` controls to build master-detail panes.

For simpler dropdown pickers use `SelectBox`, and for editable lists use `TableView`.

---

## Related widgets

- `TableView` (tabular data with built-in headers)
- `SelectBox` (dropdown selection)
- `Label` (descriptive headers)
