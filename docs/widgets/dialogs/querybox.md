---
title: QueryBox
---

# QueryBox

`QueryBox` is a **prompt dialog** that asks the user for a single value (text, number, password, etc.) and returns the result.

Use it for quick questions like "Name?", "Quantity?", or "Search term?", where you want an explicit OK/Cancel outcome.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

value = ttk.QueryBox.get_string(
    title="Rename",
    prompt="Enter a new name",
    initial="Untitled",
)

print("value:", value)  # None if cancelled
app.mainloop()
```

---

## When to use

Use `QueryBox` when:

- you need one value

- the user must explicitly confirm/cancel

### Consider a different control when...

- the value is part of a larger form - use [TextEntry](../inputs/textentry.md) inline instead

- you need multiple fields or rich validation - use [FormDialog](formdialog.md) instead

---

## Examples & patterns

### Password prompt

```python
pwd = ttk.QueryBox.get_password(
    title="Unlock",
    prompt="Enter your password",
)
```

### Numeric prompt

```python
qty = ttk.QueryBox.get_integer(
    title="Quantity",
    prompt="How many?",
    initial=1,
    minvalue=0,
    maxvalue=999,
)
```

### Value model

QueryBox returns:

- the committed value (string/number), or

- `None` when cancelled

### Validation and constraints

Use numeric bounds (`minvalue` / `maxvalue`) where available.
For more complex validation or multiple fields, use [FormDialog](formdialog.md).

---

## Behavior

- OK commits the value

- Cancel / Escape closes without committing

- Enter confirms when the input is valid (if supported)

---

## Additional resources

### Related widgets

- [Dialog](dialog.md) - base dialog API

- [FormDialog](formdialog.md) - structured multi-field input

- [MessageBox](messagebox.md) - confirmation / alerts

- [QueryDialog](querydialog.md) - alternative query dialog

### API reference

- [`ttkbootstrap.QueryBox`](../../reference/dialogs/QueryBox.md)