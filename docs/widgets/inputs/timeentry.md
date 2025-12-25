---
title: TimeEntry
---

# TimeEntry

`TimeEntry` is a form-ready input control for entering a **time of day**.

It's built on the same field foundation as other v2 inputs, so it supports a label and message region, validation,
localization/formatting, and consistent events.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

t = ttk.TimeEntry(
    app,
    label="Start time",
    value="08:30",
)
t.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## When to use

Use `TimeEntry` when:

- users need to enter times (schedules, appointments, thresholds)

- you want consistent field behavior (label, message, validation, events)

Consider a different control when:

- the value is not semantically a time — use [TextEntry](textentry.md)

- you want free-form text — use [TextEntry](textentry.md)

- users should step through time in fixed increments (minutes, hours) — use [SpinnerEntry](spinnerentry.md)

---

## Appearance

### `bootstyle`

```python
ttk.TimeEntry(app, label="Start time")  # primary (default)
ttk.TimeEntry(app, label="Start time", bootstyle="secondary")
ttk.TimeEntry(app, label="Start time", bootstyle="success")
ttk.TimeEntry(app, label="Start time", bootstyle="warning")
```

!!! link "Design System"
    For a complete list of available colors and styling options, see the [Design System](../../design-system/index.md) documentation.

---

## Examples and patterns

### Value model

`TimeEntry` separates **typed text** from the **committed time value**.

- While editing, the widget contains raw text.

- On commit (blur or Enter), the value is parsed and normalized.

```python
current = t.value  # committed value
raw = t.get()      # raw text
```

If parsing fails, the value remains unchanged and validation/event feedback is emitted (see **Validation**).

### Common options

Common field options include:

- `label`, `message`, `required`

- `bootstyle`

- `value` (initial committed value)

- time formatting options (if supported by your implementation)

```python
ttk.TimeEntry(app, label="End time", required=True, bootstyle="secondary")
```

### Events

`TimeEntry` follows the standard field event model:

- `<<Input>>` / `on_input` — live typing

- `<<Changed>>` / `on_changed` — committed value changed

- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>` — validation lifecycle

```python
def on_changed(event):
    print("time:", event.data["value"])

t.on_changed(on_changed)
```

### Validation

Validation is commonly used to ensure:

- the value is a valid time

- a time is required

- time ranges are consistent across fields (e.g., start < end)

Because `TimeEntry` is a structured input, prefer commit-time validation rather than per-keystroke restrictions.

---

## Behavior

`TimeEntry` is designed for quick keyboard entry:

- users can type a time (e.g., `830`, `8:30`, `08:30`, depending on your parser)

- commit occurs on blur or Enter

- formatting (if configured) is applied on commit

If your implementation supports a picker-style interaction, it should be treated as an optional convenience on top of typing.

---

## Localization

`TimeEntry` supports locale-aware time formatting. Times are displayed according to the current locale's conventions (12-hour vs 24-hour format, AM/PM indicators).

!!! link "Localization"
    For complete localization configuration and supported formats, see the [Localization](../../capabilities/localization.md) documentation.

---

## Reactivity

`TimeEntry` integrates with the signals system for reactive data binding. Changes to the field value can automatically propagate to other parts of your application.

!!! link "Signals"
    For details on reactive patterns and data binding, see the [Signals](../../capabilities/signals/signals.md) documentation.

---

## Additional resources

### Related widgets

- [DateEntry](dateentry.md) — date input control
- [TextEntry](textentry.md) — general field control
- [NumericEntry](numericentry.md) — numeric field with bounds and stepping
- [SpinnerEntry](spinnerentry.md) — stepped input control (useful for minute increments)
- [Form](../forms/form.md) — build forms from field definitions

### Framework concepts

- [Forms](../../guides/forms.md) — working with form controls
- [Localization](../../capabilities/localization.md) — internationalization and formatting
- [Signals](../../capabilities/signals/signals.md) — reactive data binding

### API reference

- [`ttkbootstrap.TimeEntry`](../../reference/widgets/TimeEntry.md)