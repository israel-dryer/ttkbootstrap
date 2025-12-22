---
title: FilterDialog
---

# FilterDialog

`FilterDialog` is a **dialog for selecting filters** (often multi-select) with an explicit Apply/Cancel outcome.

Use it when filtering options are too dense for inline controls, or when you want users to review and apply changes all at once.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FilterDialog(
    title="Filters",
    filters=[
        {"key": "status", "label": "Status", "options": ["New", "In Progress", "Done"]},
        {"key": "priority", "label": "Priority", "options": ["Low", "Medium", "High"]},
    ],
)
result = dlg.show()

print("filters:", result)  # dict-like or None
app.mainloop()
```

---

## Value model

Filter dialogs typically return:

- a dict-like filter state (selected values), or
- `None` when cancelled

---

## Common patterns

- multi-select groups (checkbox lists)
- single-select groups (radio)
- clear/reset actions inside the dialog

---

## Behavior

- Apply commits and closes
- Cancel closes without committing
- Escape cancels (typical)

Popover mode (if supported) works well for quick filter panels.

---

## When should I use FilterDialog?

Use `FilterDialog` when:

- you have many filters and limited space
- apply/cancel is clearer than live filtering

Prefer inline filter controls when:

- there are only a few filters
- live filtering is expected

---

## Related widgets

- **Dialog** — base dialog API
- **FormDialog** — general multi-field input
- **SelectBox** / **CheckButton** — common inline filter controls

---

## Reference

- **API Reference:** `ttkbootstrap.FilterDialog`
