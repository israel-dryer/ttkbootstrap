---
title: WidgetName
---

# WidgetName

1–2 paragraphs that say:

- what kind of data this widget displays (tabular, hierarchical, list,
  status, progress)
- whether it is **read-only display** or supports interaction
  (selection, expansion, editing)
- a comparison sentence if useful ("Unlike X…", "Similar to Y…")

The intro carries the "what is this" framing — there's no separate
`Framework integration` lead. Its content distributes into Common
options (theme tokens, headers, icons), Behavior (selection,
keyboard, scrolling), Events (selection change, row activation,
data-change events), and Localization & reactivity.

---

## Basic usage

One minimal, runnable example that renders the data.

```python
import ttkbootstrap as ttk

# minimal, copy/paste runnable
```

If the widget supports multiple modes (tree vs table, determinate
vs indeterminate), show only the primary mode here.

---

## Data model

*Optional — include for data-bound widgets (TableView, TreeView,
ListView). Skip for read-only status/progress widgets (Label,
Badge, Progressbar, Floodgauge, Meter) — they don't have a data
model beyond `text`/`value`.*

Describe how data is provided and represented:

- record shape (dict, list/tuple, object, datasource)
- identifiers (iids/keys) and how selection maps back to records
- how to insert / update / delete / reload rows
- the reactive surface (signals, datasource events) if applicable

Include one concise example of inserting or reloading data.

---

## Common options

Curated — what users actually configure. Not an API dump. For
data-display widgets this typically covers:

- `text`, `value`, `accent`, `variant`, `density`
- columns / headings / widths / alignment (data-bound widgets)
- selection mode, paging, sorting, filtering (data-bound widgets)
- `font`, `padding`, `width` (display widgets)
- `localize`, `value_format` (when supported)

Show short representative examples per concern.

---

## Behavior

Interaction and presentation rules:

- selection and focus (data-bound widgets)
- keyboard navigation (Up/Down, Home/End, expand/collapse)
- click / double-click / right-click behavior
- expand/collapse for hierarchical views
- scroll behavior (built-in scrollbars, virtualization)
- determinate vs indeterminate animation (progress widgets)
- visual states (`hover`, `active`, `disabled`)

If the widget has a popup or composes with a menu, describe the
open/close lifecycle here.

---

## Events

Document the primary event hooks. For display widgets this is
often a deliberate negative ("Badge does not emit events");
include the section anyway so readers don't go looking.

Examples:

- selection changed
- row click / double-click / right-click
- open/close for tree items
- data modification events (insert/update/delete/move)
- `on_changed` for value-bearing widgets (progressbar, meter)

```python
def on_select(event):
    ...

widget.on_select(on_select)
```

---

## Performance guidance

*Optional — include for data-bound widgets that scale with row
count (TableView, TreeView, ListView). Skip for lightweight
status/progress widgets.*

For large datasets:

- prefer paging / virtual mode where available
- avoid inserting thousands of rows on the UI thread at once
- batch updates via the datasource API
- cite concrete row-count thresholds where the framework recommends
  a different mode

---

## When should I use WidgetName?

Use WidgetName when:

- …

Prefer OtherWidget when:

- …

This sits near the bottom on purpose: readers reach it after they've
seen what the widget does and how it's configured, so the
recommendation lands with context.

---

## Related widgets

- **OtherWidget** — how it differs
- **AnotherWidget** — complementary role

---

## Reference

- **API reference:** `ttkbootstrap.WidgetName`
- **Related guides:** …
