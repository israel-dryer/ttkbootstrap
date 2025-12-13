---
title: TableView
icon: fontawesome/solid/table
---


# TableView

`TableView` brings a batteries‑included table experience backed by an in-memory SQLite datasource, marrying filtering, sorting, paging, grouping, and context menus with ttkbootstrap theming.

---

## Overview

Key TableView capabilities:

- Datasource-backed rendering: the widget uses `SqliteDataSource` to filter, sort, and cache records before pushing them through a styled `TreeView`.
- Headers support context menus for alignment, column ordering, hiding/showing, grouping, and reset operations.
- Paging modes (`standard`, `virtual`) keep large datasets responsive, complete with status labels, navigation buttons, and optional scrollbars.
- Filtering/search UI can be shown as a search bar plus column filters; you control what is exposed through the `filtering`, `search`, and `header_context` options.
- Editing/exporting pipelines (adding/updating/deleting, CSV/XLSX export) integrate with optional `Form` dialogs and toolbar buttons.
- Selection events (`<<SelectionChanged>>`, `<<RowClick>>`) fire with structured payloads so you can react to row taps or checkbox-type selection changes.

Use TableView when you want a fully featured data grid that just needs column metadata plus a data source, rather than wiring a bare `TreeView` yourself.

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap.datasource import SqliteDataSource

app = ttk.App(theme="cosmo")

data = [
    {"name": "Alice", "email": "alice@example.com", "role": "Admin"},
    {"name": "Bob", "email": "bob@example.com", "role": "Engineer"},
]

table = ttk.TableView(
    app,
    datasource=SqliteDataSource(data),
    columns=[
        {"key": "name", "text": "Name"},
        {"key": "email", "text": "Email"},
        {"key": "role", "text": "Role"},
    ],
    paging={"enabled": False},
    filtering={"enabled": True},
)
table.pack(fill="both", expand=True, padx=16, pady=16)

app.mainloop()
```

---

## Styling & toolbar controls

- The toolbar exposes dropdown buttons for search mode, filtering, exporting, and column chooser controls; everything respects bootstyle tokens and iconography.
- Row alternation (`row_alternation`) injects striping tokens to lighten background rows while preserving theme colors.
- Use `surface_color`, `bootstyle`, and perimeter paddings to keep TableView aligned with surrounding cards, frames, or sections.

---

## Pagination, filtering, and search

- `paging` controls page size, caching, and whether horizontal/vertical scrollbars appear; `mode="virtual"` streams pages smoothly.
- `filtering` toggles filter actions on headers and rows; column filters open `FilterDialog` widgets with searches and select-all support.
- `search` lets you surface a quick searchbar with standard/advanced modes and configurable event triggers (`input` or `enter`).
- Filtering/searching rebuilds the SQL WHERE clause automatically, and TableView reloads from page zero so you always see fresh data.

---

## Editing, exporting & grouping

- `editing` options expose add/update/delete workflows that open `Form` dialogs configured via `editing.form`.
- `exporting` drives CSV/XLSX export buttons (per page or entire dataset) with toolbar hooks.
- Group rows by a column via the header context menu (`Group by Column`) or programmatically; grouped rows expand/collapse around parent nodes.
- Header menu actions handle resetting, aligning text, moving columns, hiding/showing columns, and toggling grouping.

---

## Events & data access

- Listen for `<<SelectionChanged>>`/`<<RowClick>>` to react to user picks; the event `data` payload includes raw record dicts and `iid`s.
- Use `table.get_selected_records()` or access `table.datasource` to read or mutate the backing data.
- Call `table.reload()` to refresh after external edits, and `table.clear_filter()` to reset filters.

---

## When to use TableView

Use `TableView` when you need a rich, data-driven grid (dashboards, admin panels, reporting) with sorting, filtering, paging, and optional editing out of the box. For minimal tables, `TreeView` or `SelectBox` may suffice.

---

## Related widgets

- `TreeView` (low-level tree/table control)
- `Form` (edit records via forms)
- `DropdownButton` (toolbar buttons)
