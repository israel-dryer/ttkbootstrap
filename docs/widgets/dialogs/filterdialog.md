---
title: FilterDialog
---

# FilterDialog

`FilterDialog` is a **dialog for selecting filters** (often multi-select) with an explicit Apply/Cancel outcome.

Use it when filtering options are too dense for inline controls, or when you want users to review and apply changes all at once.

---

## Quick start

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

## When to use

Use `FilterDialog` when:

- you have many filters and limited space

- apply/cancel is clearer than live filtering

### Consider a different control when...

- there are only a few filters - use inline filter controls instead

- live filtering is expected - use inline filter controls instead

---

## Examples & patterns

### Common patterns

- multi-select groups (checkbox lists)

- single-select groups (radio)

- clear/reset actions inside the dialog

### Value model

Filter dialogs typically return:

- a dict-like filter state (selected values), or

- `None` when cancelled

---

## Behavior

- Apply commits and closes

- Cancel closes without committing

- Escape cancels (typical)

Popover mode (if supported) works well for quick filter panels.

---

## Additional resources

### Related widgets

- [Dialog](dialog.md) - base dialog API

- [FormDialog](formdialog.md) - general multi-field input

- [SelectBox](../selection/selectbox.md) - inline selection control

- [CheckButton](../selection/checkbutton.md) - common inline filter control

### API reference

!!! link "API Reference"
    `ttkbootstrap.FilterDialog`