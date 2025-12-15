---
title: TimeEntry
icon: fontawesome/solid/clock
---

# TimeEntry

`TimeEntry` is a **high-level time input control**.

It combines a typed time field with a picker-style interaction (where supported), built on ttkbootstrap’s `Field`
foundation — so it matches the rest of your controls:

- a **label** and **message** area
- **validation** + validation feedback
- optional **localization** and **formatting**
- consistent **virtual events** with `on_*` / `off_*` helpers

Use `TimeEntry` when users need to enter a time reliably (appointments, cutoffs, schedules, durations).

> _Image placeholder:_  
> `![TimeEntry overview](../_img/widgets/timeentry/overview.png)`  
> Suggested shot: standard time field + invalid state + 24h example.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

t = ttk.TimeEntry(
    app,
    label="Start time",
    value="09:30",
    message="Type a time, or use the picker (if enabled)",
)
t.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## What problem does TimeEntry solve?

A plain `Entry` can accept time text, but apps usually need more:

- consistent parsing (e.g., `9:30`, `0930`, `9.30`, `9:30 AM`)
- a stable display format (12h/24h)
- validation (required, valid time, business hours)
- a consistent change event model

`TimeEntry` standardizes those behaviors so every time field works the same.

---

## Text vs value

Like other v2 entry controls, `TimeEntry` distinguishes:

| Concept | Meaning |
|---|---|
| Text | what the user is typing |
| Value | committed time value after parsing/validation |

```python
# committed value (implementation may return time/datetime or normalized string)
current = t.value

# set programmatically
t.value = "13:45"
```

To read raw typed text:

```python
raw = t.get()
```

---

## Formatting and locale

`TimeEntry` can display times in a locale-aware format and parse user input accordingly.

```python
import ttkbootstrap as ttk

app = ttk.App()

time24 = ttk.TimeEntry(
    app,
    label="Start time",
    value="13:45",
    locale="en_GB",
    time_format="HH:mm",    # example format
)
time24.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

!!! note "Formatting vs storage"
    Keep your stored value in a stable format (often ISO-like strings), and let `TimeEntry` handle localized display.

---

## Validation

Because `TimeEntry` is field-based, you can add the same validation rules used by `TextEntry`.

```python
import ttkbootstrap as ttk

app = ttk.App()

t = ttk.TimeEntry(app, label="Time", required=True)
t.add_validation_rule("required", message="Time is required")
t.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

Common validation patterns:

- required time
- valid time
- within business hours (e.g., 08:00–18:00)

---

## Events

`TimeEntry` emits standard field events:

- `<<Input>>` — text editing
- `<<Changed>>` — committed value changed (blur/Enter, or picker selection)
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

You can attach handlers using the `on_*` helpers (and remove them with `off_*`).

```python
import ttkbootstrap as ttk

app = ttk.App()

t = ttk.TimeEntry(app, label="Start time")
t.pack(fill="x", padx=20, pady=10)

def handle_changed(event):
    print("changed:", event.data)

t.on_changed(handle_changed)

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

t = ttk.TimeEntry(app, label="Reminder time")
t.insert_addon(ttk.Label, position="before", text="⏰")
t.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![TimeEntry addons](../_img/widgets/timeentry/addons.png)`

---

## When should I use TimeEntry?

Use `TimeEntry` when:

- you want reliable parsing and consistent display
- you need validation and helper messaging
- you’re building forms or dialogs

Prefer `TextEntry` when:

- the user may enter non-time values like “ASAP”, “after lunch”, or “end of day”

---

## Related widgets

- **DateEntry** — date input control
- **TextEntry** — general field control
- **NumericEntry** — numeric field with bounds and stepping
- **SpinnerEntry** — stepped input control (useful for minute increments)
