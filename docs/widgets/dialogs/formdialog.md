---
title: FormDialog
---

# FormDialog

`FormDialog` is a **modal dialog** that collects multiple related values using a structured form layout.

Use it when a workflow needs a small set of inputs (2-8 fields) with an explicit OK/Cancel outcome.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.FormDialog(
    title="New connection",
    fields=[
        {"key": "host", "label": "Host", "required": True},
        {"key": "port", "label": "Port", "value": 5432},
        {"key": "user", "label": "User"},
    ],
)
result = dlg.show()

print("result:", result)  # dict or None (implementation-dependent)
app.mainloop()
```

---

## When to use

Use `FormDialog` when:

- you need several inputs at once

- the user should commit/cancel explicitly

- the inputs are part of a single small task

### Consider a different control when...

- you only need one value - use [QueryBox](querybox.md) instead

- the flow is multi-step or requires navigation - use [PageStack](../views/pagestack.md) instead

---

## Examples & patterns

### Common options

- `title` - dialog title

- `fields` - form field definitions

- `initial` - initial values (if supported)

- `validate_on_submit` - run validation before accepting (if supported)

### Value model

Form dialogs typically return:

- a dict-like result mapping field keys to committed values, or

- `None` when cancelled

### Events

Most form dialogs are handled via return value.
If your dialog emits validation lifecycle events, use them for UX only (messages/state), not as the primary result.

### Validation and constraints

Use field-level validation:

- required fields

- type parsing (int/float/date)

- cross-field rules (password confirmation, ranges)

For complex "live" forms, prefer an inline [Form](../forms/form.md) in a normal window or a [PageStack](../views/pagestack.md) flow.

---

## Behavior

- OK commits and closes

- Cancel closes without committing

- Escape cancels (typical)

- Enter may submit the form (implementation-dependent)

---

## Additional resources

### Related widgets

- [Dialog](dialog.md) - base dialog API

- [QueryBox](querybox.md) - single-value prompts

- [QueryDialog](querydialog.md) - alternative query dialog

- [Form](../forms/form.md) - inline multi-field form layouts

- [PageStack](../views/pagestack.md) - multi-step workflows

### API reference

- [`ttkbootstrap.FormDialog`](../../reference/dialogs/FormDialog.md)