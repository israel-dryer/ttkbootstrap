---
title: QueryBox
---

# QueryBox

`QueryBox` is a **prompt dialog** that asks the user for a single value (text, number, password, etc.) and returns the result.

Use it for quick questions like “Name?”, “Quantity?”, or “Search term?”, where you want an explicit OK/Cancel outcome.

---

## Basic usage

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

## Value model

QueryBox returns:

- the committed value (string/number), or
- `None` when cancelled

---

## Common patterns

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

---

## Behavior

- OK commits the value
- Cancel / Escape closes without committing
- Enter confirms when the input is valid (if supported)

---

## Validation and constraints

Use numeric bounds (`minvalue` / `maxvalue`) where available.
For more complex validation or multiple fields, use **FormDialog**.

---

## When should I use QueryBox?

Use `QueryBox` when:

- you need one value
- the user must explicitly confirm/cancel

Prefer **TextEntry** (inline) when:

- the value is part of a larger form

Prefer **FormDialog** when:

- you need multiple fields or rich validation

---

## Related widgets

- **Dialog** — base dialog API
- **FormDialog** — structured multi-field input
- **MessageBox** — confirmation / alerts

---

## Reference

- **API Reference:** `ttkbootstrap.QueryBox`
