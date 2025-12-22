---
title: DateDialog
---

# DateDialog

`DateDialog` is a **modal dialog** for selecting a calendar date.

It’s useful when date selection is a discrete task (pick once, then continue), and you want the familiar dialog flow:
open → pick → confirm/cancel.

If you need an inline field that also supports typing, prefer **DateEntry**.

<!--
IMAGE: DateDialog open state
Suggested: Dialog centered over app with month grid and OK/Cancel
Theme variants: light / dark
-->

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

dialog = ttk.DateDialog(
    title="Choose a date",
    initial_date="2025-12-31",
)
result = dialog.show()

print("Selected:", result)  # depends on your API: date / string / None

app.mainloop()
```

!!! note "Return value"
    Dialogs typically return `None` when cancelled. If your implementation returns a structured result
    (e.g., `{ "value": ... }`), prefer reading from that.

---

## Value model

A date dialog produces a single **committed date** (or no value if cancelled).

- **No live typing** is required (though some implementations may allow it)
- The chosen date is committed when the user confirms (OK / Apply)

---

## Common options

### `title`

```python
ttk.DateDialog(title="Due date")
```

### `initial_date`

Sets the date shown/selected when the dialog opens.

```python
ttk.DateDialog(initial_date="2025-01-01")
```

### `min_date` / `max_date` (if supported)

Constrain selectable dates.

```python
ttk.DateDialog(min_date="2025-01-01", max_date="2025-12-31")
```

### Locale / formatting (if supported)

Dialog date display should follow your app’s localization settings.

---

## Behavior

- Opens as a **modal** window (blocks interaction with the parent until closed)
- OK commits the current selection
- Cancel closes without committing
- Escape typically cancels
- Enter typically confirms (depends on focus and implementation)

---

## Events

Dialogs are usually handled via return value, but some implementations emit events such as:

- `<<Changed>>` (when selection changes inside the dialog)
- `<<Accepted>>` / `<<Cancelled>>`

If your dialog supports events, treat them as secondary to the `.show()` result.

---

## Validation and constraints

Use constraints when:

- the date must be within an allowed window
- you want to disable past/future dates

Use validation when:

- selection must satisfy business rules beyond bounds (e.g., working days only)

---

## When should I use DateDialog?

Use `DateDialog` when:

- date selection is a one-time action (pick then proceed)
- you want an explicit confirm/cancel flow
- the date picker needs more space than an inline popup

Prefer **DateEntry** when:

- date is part of a form
- users may want to type/paste a date
- you want inline validation and messaging

---

## Related widgets

- **DateEntry** — inline date field with popup picker
- **TimeEntry** — time-of-day input
- **MessageBox** — simple modal feedback dialogs

---

## Reference

- **API Reference:** `ttkbootstrap.DateDialog`
