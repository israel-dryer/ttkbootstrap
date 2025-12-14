---
title: DateEntry
icon: fontawesome/solid/calendar-days
---

# DateEntry

`DateEntry` is a **high-level date input control**.

It combines a familiar text field with a date picker popup, built on ttkbootstrap’s `Field` foundation — so it behaves like
your other entry controls (label, message, validation, localization, events), while making date entry fast and consistent.

Use `DateEntry` when:

- users can type a date **or** pick one from a calendar
- you want locale-aware formatting and parsing
- you want the same “field” experience as `TextEntry` / `NumericEntry`

> _Image placeholder:_  
> `![DateEntry overview](../_img/widgets/dateentry/overview.png)`  
> Suggested shot: closed field + open calendar popup + error state.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

due = ttk.DateEntry(
    app,
    label="Due date",
    value="2025-12-13",
    message="Pick a date or type one (YYYY-MM-DD)",
)
due.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## What problem does DateEntry solve?

A plain text `Entry` can accept dates, but apps quickly need more:

- a consistent date format
- parsing (“12/13/25”, “Dec 13”, etc.)
- validation and helpful error messages
- a date picker for speed and accessibility

`DateEntry` standardizes those concerns in one control.

---

## Text vs value

Like other v2 entry controls, `DateEntry` distinguishes:

| Concept | Meaning |
|---|---|
| Text | what the user types |
| Value | a committed date value after parsing/validation |

```python
# committed value (implementation may return date/datetime or normalized string)
current = due.value

# set a new date
due.value = "2025-12-31"
```

To read raw typed text:

```python
raw = due.get()
```

---

## Formatting and locale

`DateEntry` can display dates in a locale-appropriate format and parse user input accordingly.

```python
import ttkbootstrap as ttk

app = ttk.App()

birthday = ttk.DateEntry(
    app,
    label="Birthday",
    value="1990-07-04",
    locale="en_US",
    date_format="MM/dd/yyyy",     # example format
)
birthday.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

!!! tip "Use stable formats"
    Keep your **storage format** stable (e.g., ISO strings) and let the control handle display formatting.

---

## Picker behavior

`DateEntry` includes a calendar popup that opens from the suffix button.

Common behaviors:

- click the calendar button → opens picker
- click a day → commits the date and closes the popup
- Escape → closes the popup without changing the committed value

> _Image placeholder:_  
> `![DateEntry picker](../_img/widgets/dateentry/picker.png)`  
> Suggested shot: open picker with a selected date.

---

## Validation

Because `DateEntry` is field-based, you can use the same validation patterns as other entry controls.

```python
import ttkbootstrap as ttk

app = ttk.App()

d = ttk.DateEntry(app, label="Date", required=True)
d.add_validation_rule("required", message="A date is required")
d.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

Common validation patterns:

- required date
- not in the past
- within a business window (e.g., next 90 days)

---

## Events

`DateEntry` emits standard field events:

- `<<Input>>` — text editing
- `<<Changed>>` — committed value changed (typing + Enter/blur, or picker selection)
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

In addition to `widget.bind(...)`, ttkbootstrap provides convenience methods for **all events** in this family:

- `on_*` to attach a handler
- `off_*` to remove a handler

Example: reacting to committed value changes

```python
import ttkbootstrap as ttk

app = ttk.App()

d = ttk.DateEntry(app, label="Due date")
d.pack(fill="x", padx=20, pady=10)

def handle_changed(event):
    print("changed:", event.data)

d.on_changed(handle_changed)

app.mainloop()
```

!!! tip "Live Typing"
    Use `on_input(...)` when you want “live typing” behavior, and `on_changed(...)` when you want the committed value.

---

## Add-ons

Like other field controls, you can insert prefix/suffix add-ons.

```python
import ttkbootstrap as ttk

app = ttk.App()

d = ttk.DateEntry(app, label="Start date")
d.insert_addon(ttk.Label, position="before", text="📅")
d.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![DateEntry addons](../_img/widgets/dateentry/addons.png)`

---

## When should I use DateEntry?

Use `DateEntry` when:

- users need to enter dates reliably
- you want a picker popup and parsing support
- you want consistent label/message/validation behavior

Prefer `TextEntry` when:

- the value is “date-like” but not a calendar date (e.g., “Q4 2025”, “ASAP”, “Next week”)

---

## Related widgets

- **TimeEntry** — time input control
- **TextEntry** — general field control with validation and formatting
- **NumericEntry** — numeric field with bounds and stepping
- **DateDialog** — date selection in a modal dialog (if you prefer dialogs)
