---
title: FormDialog
---

# FormDialog

`FormDialog` is a **modal dialog** that collects multiple related values using a structured form layout.

Use it when a workflow needs a small set of inputs (2–8 fields) with an explicit OK/Cancel outcome.

---

## Basic usage

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

## Value model

Form dialogs typically return:

- a dict-like result mapping field keys to committed values, or
- `None` when cancelled

---

## Common options

- `title`
- `fields` — form field definitions
- `initial` — initial values (if supported)
- `validate_on_submit` — run validation before accepting (if supported)

---

## Events

Most form dialogs are handled via return value.
If your dialog emits validation lifecycle events, use them for UX only (messages/state), not as the primary result.

---

## Validation and constraints

Use field-level validation:

- required fields
- type parsing (int/float/date)
- cross-field rules (password confirmation, ranges)

For complex “live” forms, prefer an inline **Form** in a normal window or a PageStack flow.

---

## When should I use FormDialog?

Use `FormDialog` when:

- you need several inputs at once
- the user should commit/cancel explicitly
- the inputs are part of a single small task

Prefer **QueryBox** when:

- you only need one value

Prefer **PageStack** when:

- the flow is multi-step or requires navigation

---

## Related widgets

- **Dialog** — base dialog API
- **QueryBox** — single-value prompts
- **Form** — inline multi-field form layouts
- **PageStack** — multi-step workflows

---

## Reference

- **API Reference:** `ttkbootstrap.FormDialog`
