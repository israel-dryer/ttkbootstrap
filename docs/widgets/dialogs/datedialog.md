---
title: DateDialog
---

# DateDialog

`DateDialog` is a **modal dialog** for selecting a calendar date.

It's useful when date selection is a discrete task (pick once, then continue), and you want the familiar dialog flow:
open -> pick -> confirm/cancel.

If you need an inline field that also supports typing, prefer [DateEntry](../inputs/dateentry.md).

<!--
IMAGE: DateDialog open state
Suggested: Dialog centered over app with month grid and OK/Cancel
Theme variants: light / dark
-->

---

## Quick start

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

## When to use

Use `DateDialog` when:

- date selection is a one-time action (pick then proceed)

- you want an explicit confirm/cancel flow

- the date picker needs more space than an inline popup

### Consider a different control when...

- date is part of a form - use [DateEntry](../inputs/dateentry.md) instead

- users may want to type/paste a date - use [DateEntry](../inputs/dateentry.md) instead

- you want inline validation and messaging - use [DateEntry](../inputs/dateentry.md) instead

---

## Examples & patterns

### Common options

#### `title`

```python
ttk.DateDialog(title="Due date")
```

#### `initial_date`

Sets the date shown/selected when the dialog opens.

```python
ttk.DateDialog(initial_date="2025-01-01")
```

#### `min_date` / `max_date` (if supported)

Constrain selectable dates.

```python
ttk.DateDialog(min_date="2025-01-01", max_date="2025-12-31")
```

#### Locale / formatting (if supported)

Dialog date display should follow your app's localization settings.

### Value model

A date dialog produces a single **committed date** (or no value if cancelled).

- **No live typing** is required (though some implementations may allow it)

- The chosen date is committed when the user confirms (OK / Apply)

### Events

Dialogs are usually handled via return value, but some implementations emit events such as:

- `<<Changed>>` (when selection changes inside the dialog)

- `<<Accepted>>` / `<<Cancelled>>`

If your dialog supports events, treat them as secondary to the `.show()` result.

### Validation and constraints

Use constraints when:

- the date must be within an allowed window

- you want to disable past/future dates

Use validation when:

- selection must satisfy business rules beyond bounds (e.g., working days only)

---

## Behavior

- Opens as a **modal** window (blocks interaction with the parent until closed)

- OK commits the current selection

- Cancel closes without committing

- Escape typically cancels

- Enter typically confirms (depends on focus and implementation)

---

## Additional resources

### Related widgets

- [DateEntry](../inputs/dateentry.md) - inline date field with popup picker

- [TimeEntry](../inputs/timeentry.md) - time-of-day input

- [Calendar](../selection/calendar.md) - standalone calendar widget

- [MessageBox](messagebox.md) - simple modal feedback dialogs

### API reference

!!! link "API Reference"
    `ttkbootstrap.DateDialog`