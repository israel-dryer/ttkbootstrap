---
title: DateEntry
icon: fontawesome/solid/calendar-day
---


# DateEntry

`DateEntry` is a **Field-based date input** designed for structured, locale-aware capture of calendar values.
It decorates an `Entry` with validation, formatting, messaging, and an optional calendar picker button so users
can type dates or choose them from a dialog.

---

## Overview

`DateEntry` provides:

- Locale-aware parsing/formatting driven by ICU-style patterns or format presets (`shortDate`, `longDate`, `monthAndYear`, etc.).
- Accepts `date`, `datetime`, or string input and commits a normalized `date` value on blur/Enter.
- Optional calendar picker button that launches `DateDialog`, mirroring standard dialog behavior with customizable title and first weekday.
- All `Field` amenities (labels, messages, validation, addon widgets, bootstyles).
- Hide/show the picker button with `show_picker_button=False` when you only need typed input.

The control was built for forms where dates must be displayed consistently and validated before submission.

---

## Quick example

```python
import ttkbootstrap as ttk
from datetime import date

app = ttk.App(title="Date Entry Demo", theme="cosmo")

birth_date = ttk.DateEntry(
    app,
    label="Birth date",
    value=date(1990, 1, 15),
    value_format="shortDate",
    message="Enter your birthday",
)
birth_date.pack(fill="x", padx=16, pady=8)

event_date = ttk.DateEntry(
    app,
    label="Event date",
    value_format="longDate",
    locale="en_US",
)
event_date.pack(fill="x", padx=16, pady=8)

iso_date = ttk.DateEntry(
    app,
    label="ISO date",
    value="2025-01-15",
    value_format="yyyy-MM-dd",
)
iso_date.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Formatting, presets, & parsing

DateEntry relies on `IntlFormatter` patterns. Pass a preset like `longDate`, `monthAndYear`, or `dayOfWeek`, or provide a custom pattern such as `yyyy-MM-dd` or `MMMM dd, yyyy`.

The widget keeps the text synchronized with the parsed date object and automatically re-formats after the user commits input. Invalid dates revert to the last valid value and show validation messages through the `Field` messaging system.

---

## Picker button

By default DateEntry shows a calendar button (with the `calendar-week` icon). Clicking it opens `DateDialog` using the current value as the initial date; dragging through the spinner updates the entry when the dialog returns a result.

Configure:

- `picker_title`: Title for the dialog window.
- `picker_first_weekday`: First weekday (0=Monday, 6=Sunday).
- `show_picker_button=False`: Hide the button for inline-only entry.

Since `DateDialog` is modal, focus returns to the entry automatically, and the result is applied even if the dialog returns a `datetime`. The button is part of the `Field` addon system, so you can reposition or remove it if needed.

---

## Events & interaction

DateEntry forwards the standard `Field` signals:

- `<<Changed>>`: Fires after a new date commits.
- `<<Input>>`: Fires on every keystroke.
- `<<Valid>>` / `<<Invalid>>`: Track validation status changes.

The field also exposes the underlying datetime value through the `.value` property (which can return `None` if `allow_blank=True`).

---

## When to use DateEntry

Choose `DateEntry` when your form collects dates that must be parsed, formatted, localized, and validated consistently, and when a calendar picker improves discoverability for non-text-savvy users.

If you need a broader date/time field (including time), combine it with `TimeEntry` or use `Form`. For purely text validation, `TextEntry` remains an alternative.

---

## Related widgets

- `TimeEntry`
- `TextEntry`
- `Form`
- `SpinnerEntry`

