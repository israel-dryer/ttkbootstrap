---
title: DataDisplayWidgetName
---

# DataDisplayWidgetName

1–2 paragraphs describing:

- what kind of data this widget displays (tabular, hierarchical, list, status)
- whether it is **read-only display** or supports interaction (selection, editing)
- what it is built on (if relevant) and what “extras” it provides over the base Tk widget

If useful, include a short “Use it for…” sentence (file browsers, admin grids, dashboards, etc.).

---

## Basic usage

Show the smallest runnable example that renders data.

```python
# minimal, copy/paste runnable
```

If the widget supports multiple modes (tree vs table, determinate vs indeterminate), show only the primary mode here.

---

## What problem it solves

Explain the UI problem this widget addresses, such as:

- displaying large datasets efficiently
- presenting hierarchy + columns
- adding sorting / filtering / paging
- communicating progress or status

Focus on why this widget exists versus simpler alternatives.

---

## Core concepts

Explain how to think about the widget’s model and capabilities.

Common subsections:

- data model (rows/records/items) and identifiers
- columns/headings and formatting
- selection model (single/multiple/none)
- modes (tree vs table, determinate vs indeterminate)
- composition (built on TreeView, datasource, etc.)

---

## Data model

Describe how data is provided and represented:

- `rows` / `items` / `datasource`
- record shape (dict, list/tuple, object)
- identifiers (iids/keys) and how selection maps back to records
- updating/reloading data

Include one concise example of inserting/updating or reloading data.

---

## Common options

Curated options only (avoid full API dumps), such as:

- columns / headings / widths / alignment
- selection and selection mode
- paging / virtualization
- sorting / filtering / searching
- scrollbars
- styling tokens (`bootstyle`) and key style options

Use short examples per topic.

---

## Interaction and behavior

Describe interaction rules:

- selection and focus
- keyboard navigation
- expand/collapse behavior (hierarchical views)
- click / double-click / context menu behavior (if supported)
- editing flows (if supported)

---

## Events

Document the primary events or callbacks.

Examples:

- selection changed
- row click / double-click / right-click
- open/close for tree items
- data modification events (insert/update/delete/move)

Provide one clear example showing subscribe/unsubscribe patterns (on_* / off_*), if applicable.

---

## Styling

Explain practical styling knobs:

- bootstyle tokens and what they affect (e.g., selection color)
- style options for borders, headers, selection colors, icons
- row alternation / tags (if supported)

Keep examples representative, not exhaustive.

---

## Performance guidance

For large datasets, include guidance such as:

- prefer paging/virtual mode where available
- avoid inserting thousands of rows on the UI thread at once
- use update batching, reload, or datasource patterns

If the widget is lightweight (e.g., progress indicator), state that this section is not applicable.

---

## UX guidance

Prescriptive guidance:

- when to use this widget vs a simpler display control
- how to keep tables readable (column widths, alignment, striping)
- when to show progress and how to label it
- avoid excessive affordances (too many menus, heavy chrome)

---

## When should I use DataDisplayWidgetName?

Use it when:
- …

Prefer OtherWidget when:
- …

---

## Related widgets

- **OtherDataWidget** — how it differs
- **Selection widget** — when a picker is enough
- **Form** — when input/validation is the goal

---

## Reference

- **API Reference:** `ttkbootstrap.DataDisplayWidgetName`
- **Related guides:** Data Display, Styling, Performance
