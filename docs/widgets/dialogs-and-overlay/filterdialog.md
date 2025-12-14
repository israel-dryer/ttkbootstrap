---
title: FilterDialog
icon: fontawesome/solid/filter
---

# FilterDialog

`FilterDialog` is a multi-select dialog for filtering and choosing multiple items from a list. It displays items as checkboxes with optional **search** and **select-all** controls, and returns the selected values when the user confirms.

<!--
IMAGE: FilterDialog modal
Suggested: Modal FilterDialog showing search box, Select All, and a scrollable list of checkboxes
Theme variants: light / dark
-->

<!--
IMAGE: FilterDialog frameless popover
Suggested: Frameless FilterDialog anchored to a filter button, auto-flipped near bottom edge
Theme variants: light / dark
-->

---

## Basic usage

Show a filter dialog and read the selected values:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import FilterDialog

app = ttk.App()

dlg = FilterDialog(
    master=app,
    title="Select Colors",
    items=["Red", "Green", "Blue", "Yellow"],
    allow_search=True,
    allow_select_all=True,
)

result = dlg.show()
print(result)  # e.g. ["Red", "Blue"] or None

app.mainloop()
```

---

## What problem it solves

Multi-select lists are common (filters, permissions, column visibility, tags), but building a full UI each time is repetitive. `FilterDialog` provides:

- A checkbox-based multi-select list
- Optional search filtering for long lists
- Optional “Select All” toggle
- A scrollable list container with consistent theming
- A single `show()` call that returns your selected values

---

## Core concepts

### Item format: strings or dictionaries

`items` can be provided as simple strings:

```python
items = ["Red", "Green", "Blue"]
```

Or as dictionaries for more control:

```python
items = [
    {"text": "Red", "value": "red"},
    {"text": "Green", "value": "green", "selected": True},
    {"text": "Blue", "value": "blue", "selected": True},
]
```

Rules:

- `text` is required for dict items (it’s what the user sees)
- `value` defaults to `text` when omitted
- `selected` defaults to `False` when omitted
- Pre-selected items are included in the initial `result` once confirmed

!!! tip "Use dict items for stable values"
    Use `{text, value}` when display labels might change but you want stable, programmatic values (IDs, codes, keys).

---

### Search filtering

When `allow_search=True`, a search box appears at the top. Typing filters the visible checkboxes by substring match on the item **text**.

```python
dlg = FilterDialog(app, items=items, allow_search=True)
```

Search uses “live typing” behavior (filter updates as you type).

---

### Select All

When `allow_select_all=True`, a “Select All” checkbox appears. It toggles all currently available items.

```python
dlg = FilterDialog(app, items=items, allow_select_all=True)
```

!!! note "Select All and filtering"
    Select All applies to the full list of items, not only those currently visible due to a search filter.

---

### Result value

After `show()`, you can read:

- return value from `show()`
- `dlg.result`

Both represent:

- `list[Any]` of selected `value` items if the user clicked **OK**
- `None` if the user cancelled or closed without confirming

---

## Frameless popover mode

`frameless=True` removes window decorations (title bar/borders) and enables “dismiss on outside click” behavior. This is useful for dropdown-style filter pickers attached to a button or header.

```python
dlg = FilterDialog(
    app,
    items=["A", "B", "C"],
    frameless=True,
    allow_search=True,
)

result = dlg.show(
    anchor_to="cursor",
    anchor_point="sw",
    window_point="nw",
    offset=(8, 8),
    auto_flip=True,
)
```

Popover-style usage pairs best with anchor positioning and `auto_flip=True` so the dialog stays on screen.

<!--
IMAGE: Auto-flip behavior
Suggested: Frameless FilterDialog opening upward when near the bottom of the screen
-->

---

## Events

### `<<SelectionChanged>>`

`FilterDialog` emits a `<<SelectionChanged>>` virtual event when the user clicks **OK** and selections are confirmed.

Payload:

```python
event.data = {"selected": list[Any]}
```

Prefer the convenience binders:

```python
def on_selection(event):
    print(event.data["selected"])

funcid = dlg.on_selection_changed(on_selection)
# later...
dlg.off_selection_changed(funcid)
```

!!! tip "Use events for reactive UIs"
    Use `on_selection_changed(...)` when you want to update filters, chips, or table views immediately after confirmation.

---

## Positioning

`show(...)` supports both explicit positioning and anchor-based positioning:

### Explicit coordinates

```python
result = dlg.show(position=(400, 200))
```

### Anchor-based positioning

```python
result = dlg.show(
    anchor_to="screen",      # or a widget, "cursor", "parent"
    anchor_point="center",
    window_point="center",
    offset=(0, 0),
    auto_flip="vertical",
)
```

Anchor positioning is especially useful for `frameless=True` popover-style dialogs.

---

## UX guidance

- Use `allow_search=True` when the list is longer than ~10–15 items
- Use `allow_select_all=True` for “filter toggles” where selecting many is common
- Prefer frameless popover mode for lightweight table/header filters
- Keep titles short (or use `title=" "` for popovers if you don’t want a prominent heading)

!!! tip "Filters should feel fast"
    For filter UIs, a frameless popover with search often feels faster than a full modal dialog.

---

## When to use / when not to

**Use FilterDialog when:**

- Users need to select multiple items
- You want search + checkbox UX without building it from scratch
- Selections should be confirmed with OK/Cancel

**Avoid FilterDialog when:**

- You need single-select behavior (use a selection dialog or `OptionMenu`/`Combobox`)
- You need complex per-item rendering (icons, metadata, grouping)
- You need continuous (unconfirmed) filtering while typing (embed a filter panel inline)

---

## Related widgets

- **Dialog** — generic dialog builder used internally
- **ScrollView** — used internally for the checkbox list
- **CheckButton** — checkbox primitive used for items
- **TextEntry** — used internally for search input
