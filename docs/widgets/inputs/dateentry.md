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

title: DateEntry
---

# DateEntry

`DateEntry` is a form-ready calendar date input that combines a text field with a picker popup.

It behaves like other v2 entry controls (message, validation, localization, events), while making date entry fast and consistent
using a calendar picker when needed. If you are building forms or dialogs, `DateEntry` is usually your **default date input**. fileciteturn14file6

<figure markdown>
![dateentry states](../../assets/dark/widgets-dateentry-states.png#only-dark)
![dateentry states](../../assets/light/widgets-dateentry-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

due = ttk.DateEntry(
    app,
    label="Due date",
    value="2025-12-31",
    message="Pick a date or type one",
)
due.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

DateEntry uses the standard **text vs committed value** model.

| Concept | Meaning |
|---|---|
| Text | Raw, editable string while focused |
| Value | Parsed/validated date committed on blur, Enter, or picker selection |

```python
current = due.value
raw = due.get()
```

!!! tip "Commit semantics"
    Parsing, validation, and `value_format` are applied when the value is committed
    (blur/Enter or picker selection), not while typing.

---

## Common options

### Formatting: `value_format`

Commit-time formatting shared with other field controls:

```python
ttk.DateEntry(app, label="Short Date", value="March 14, 1981", value_format="shortDate").pack()
```

<figure markdown>
![dateentry formats](../../assets/dark/widgets-dateentry-formats.png#only-dark)
![dateentry formats](../../assets/light/widgets-dateentry-formats.png#only-light)
</figure>

### Add-ons

```python
d = ttk.DateEntry(app, label="Birthday")
d.insert_addon(ttk.Label, position="before", icon="cake-fill")
```

<figure markdown>
![dateentry addons](../../assets/dark/widgets-dateentry-addons.png#only-dark)
![dateentry addons](../../assets/light/widgets-dateentry-addons.png#only-light)
</figure>

---

## Behavior

### Picker behavior

- Click the calendar button → opens the picker

- Click a day → commits the date and closes the popup

- Escape → closes the popup without committing

<figure markdown>
![dateentry picker](../../assets/dark/widgets-dateentry-popup.png#only-dark)
![dateentry picker](../../assets/light/widgets-dateentry-popup.png#only-light)
</figure>

---

## Events

DateEntry emits the standard field events:

- `<<Input>>` / `on_input`

- `<<Changed>>` / `on_changed`

- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

```python
def handle_changed(event):
    print("changed:", event.data)

due.on_changed(handle_changed)
```

!!! tip "Live typing vs commit"
    Use `on_input(...)` for live typing, and `on_changed(...)` for committed values.

---

## Validation and constraints

Common validation patterns:

- required date

- not in the past

- within a window (e.g., next 90 days)

```python
d = ttk.DateEntry(app, label="Date", required=True)
d.add_validation_rule("required", message="A date is required")
```

---

## When should I use DateEntry?

Use `DateEntry` when:

- users need to enter calendar dates reliably

- you want both typing and a picker UI

- validation and formatting should be consistent with other field controls

Prefer **TimeEntry** when:

- you need time-of-day input

Prefer **TextEntry** when:

- the value is “date-like” but not an actual calendar date

Prefer **DateDialog** when:

- date selection should be modal (dialog-based)

---

## Related widgets

- **TimeEntry** — time input control

- **TextEntry** — general field control with validation and formatting

- **DateDialog** — modal date selection

- **Form** — build forms from field definitions

---

## Reference

- **API Reference:** `ttkbootstrap.DateEntry`

---

## Additional resources

### Related widgets

- [LabeledScale](labeledscale.md)

- [NumericEntry](numericentry.md)

- [PasswordEntry](passwordentry.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.DateEntry`](../../reference/widgets/DateEntry.md)
