---
title: TimeEntry
icon: fontawesome/solid/clock
---


# TimeEntry

`TimeEntry` is a **time-focused SelectBox** that combines a searchable dropdown of time intervals with ttkbootstrap’s `Field` behaviors (labels, messages, validation, bootstyles).

It prefills a list of values between `min_time` and `max_time` at the configured `interval`, formats them via ICU patterns, and still allows typing or pasting custom times.

---

## Overview

TimeEntry delivers:

- **Auto-generated dropdown** of formatted times (default 30-minute steps).
- **Searchable SelectBox**, so typing filters the choices instantly.
- **Locale-aware formatting** with presets like `shortTime`, `longTime`, or custom patterns (`HH:mm`, `h:mm a`).
- **Configurable range** through `min_time`, `max_time`, and `interval`.
- **Clock icon button** and SelectBox keyboard/mouse interactions.
- **Field validation** and messaging (via underlying `SelectBox`).
- **Optional custom values**, so users can enter times not present in the dropdown.

The widget is ideal for scheduling UIs, appointment dialogs, and other areas where consistent time input matters.

---

## Quick example

```python
import ttkbootstrap as ttk
from datetime import time

app = ttk.App(title="Time Entry Demo", theme="cosmo")

start_time = ttk.TimeEntry(
    app,
    label="Start time",
    interval=15,
    min_time="08:00",
    max_time="17:00",
    value_format="h:mm a"
)
start_time.pack(fill="x", padx=16, pady=8)

end_time = ttk.TimeEntry(
    app,
    label="End time",
    value_format="HH:mm",
    value=time(17, 30),
    allow_blank=True,
    message="You can still type a custom time"
)
end_time.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Intervals, ranges, & custom input

- `interval` (minutes) controls how granular the dropdown values are; 5, 15, 30, 60 are common choices.
- `min_time`/`max_time` define the bounds of the dropdown; you can use `datetime.time` or strings like `"9:00 AM"`.
- `allow_custom_values` remains enabled so users can commit times that fall between intervals or extend the range without breaking validation.
- The dropdown wraps at midnight by default (generating values even when `max_time` is earlier than `min_time`).

If you need stricter validation, layer in `SelectBox` validation rules or make the field `required=True`.

---

## Formatting & locale

TimeEntry uses ICU presets or patterns supported by `IntlFormatter`.

- `shortTime` (default) renders times like `3:30 PM`.
- `longTime` includes seconds and time zone.
- `HH:mm` forces 24-hour formatting.
- You can supply any pattern that `IntlFormatter` understands (`h:mm a`, `hh:mm`, etc.).

Pair `value_format` with `locale` when you need to respect user regional settings.

---

## Events & interaction

Inherited `Field` events apply:

- `<<Changed>>`: fires when the selected or typed time commits.
- `<<Input>>`: fires on every keystroke (useful for custom filtering/UI feedback).
- `<<Valid>>` / `<<Invalid>>`: report validation state transitions.

The dropdown is searchable, so typing filters in real time, and the `SelectBox` keyboard handling (Arrow keys, Enter, Escape) works as expected.

---

## When to choose TimeEntry

Pick `TimeEntry` when you want a time picker that:

- Ships with sensible defaults (intervals, icons, formatting).
- Lets users type or choose times.
- Keeps values consistent via presets and locales.
- Integrates with `Field` for validation messaging.

For pure text validation, `TextEntry` works; for full datetime capture, combine `DateEntry` + `TimeEntry` in a `Form`.

---

## Related widgets

- `DateEntry`
- `TextEntry`
- `SelectBox`
- `Form`

