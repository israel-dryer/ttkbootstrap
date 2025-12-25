---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: TimeEntry
---

# TimeEntry

`TimeEntry` is a form-ready input control for entering a **time of day**.

It’s built on the same field foundation as other v2 inputs, so it supports a label and message region, validation,
localization/formatting, and consistent events. fileciteturn12file1

---

## Basic usage

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

## Value model

`TimeEntry` separates **typed text** from the **committed time value**.

- While editing, the widget contains raw text.

- On commit (blur or Enter), the value is parsed and normalized.

```python
current = t.value  # committed value
raw = t.get()      # raw text
```

If parsing fails, the value remains unchanged and validation/event feedback is emitted (see **Validation and constraints**).

---

## Common options

Common field options include:

- `label`, `message`, `required`

- `bootstyle`

- `value` (initial committed value)

- time formatting options (if supported by your implementation)

```python
ttk.TimeEntry(app, label="End time", required=True, bootstyle="secondary")
```

---

## Behavior

`TimeEntry` is designed for quick keyboard entry:

- users can type a time (e.g., `830`, `8:30`, `08:30`, depending on your parser)

- commit occurs on blur or Enter

- formatting (if configured) is applied on commit

If your implementation supports a picker-style interaction, it should be treated as an optional convenience on top of typing.

---

## Events

`TimeEntry` follows the standard field event model:

- `<<Input>>` / `on_input` — live typing

- `<<Changed>>` / `on_changed` — committed value changed

- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>` — validation lifecycle

```python
def on_changed(event):
    print("time:", event.data["value"])

t.on_changed(on_changed)
```

---

## Validation and constraints

Validation is commonly used to ensure:

- the value is a valid time

- a time is required

- time ranges are consistent across fields (e.g., start < end)

Because `TimeEntry` is a structured input, prefer commit-time validation rather than per-keystroke restrictions.

---

## When should I use TimeEntry?

Use `TimeEntry` when:

- users need to enter times (schedules, appointments, thresholds)

- you want consistent field behavior (label, message, validation, events)

Prefer **TextEntry** when:

- the value is not semantically a time

- you want free-form text

Prefer **SpinnerEntry** when:

- users should step through time in fixed increments (minutes, hours)

---

## Related widgets

- **DateEntry** — date input control

- **TextEntry** — general field control

- **NumericEntry** — numeric field with bounds and stepping

- **SpinnerEntry** — stepped input control (useful for minute increments)

---

## Reference

- **API Reference:** `ttkbootstrap.TimeEntry`

---

## Additional resources

### Related widgets

- [DateEntry](dateentry.md)

- [LabeledScale](labeledscale.md)

- [NumericEntry](numericentry.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.TimeEntry`](../../reference/widgets/TimeEntry.md)
