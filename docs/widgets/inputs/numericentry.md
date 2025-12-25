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

title: NumericEntry
---

# NumericEntry

`NumericEntry` is a form-ready numeric input control that combines a **label**, **numeric field**, and **message region**.

It adds the behavior you almost always need for numeric data: bounds, stepping, formatting, validation, localization, and
consistent field events. If you are building forms or dialogs, `NumericEntry` is usually your **default numeric input**. fileciteturn14file0

<figure markdown>
![NumericEntry states](../../assets/dark/widgets-numericentry-states.png#only-dark)
![NumericEntry states](../../assets/light/widgets-numericentry-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.NumericEntry(
    app,
    label="Quantity",
    value=1,
    minvalue=0,
    maxvalue=999,
    increment=1,
    message="How many items?",
)
qty.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

All Entry-based field controls separate **what the user is typing** from the **committed value**.

| Concept | Meaning |
|---|---|
| Text | Raw, editable string while focused |
| Value | Parsed/validated value committed on blur or Enter |

```python
current = qty.value      # committed value (usually int/float)
raw = qty.get()          # raw text at any time

qty.value = 42
```

!!! tip "Commit semantics"
    Parsing, validation, and `value_format` are applied **only when the value is committed**
    (blur/Enter), never on every keystroke.

---

## Common options

### Bounds: `minvalue` / `maxvalue`

```python
age = ttk.NumericEntry(app, label="Age", value=25, minvalue=0, maxvalue=120)
```

### Stepping: `increment`

Stepping is supported via:

- spin buttons (if enabled)

- Up/Down arrow keys

- mouse wheel (platform-dependent)

```python
price = ttk.NumericEntry(
    app,
    label="Unit Price",
    value=9.99,
    minvalue=0,
    maxvalue=10000,
    increment=0.01,
)
```

### `wrap`

- default behavior clamps at the min/max

- set `wrap=True` to cycle through the range

```python
percent = ttk.NumericEntry(
    app,
    label="Percent",
    value=50,
    minvalue=0,
    maxvalue=100,
    increment=5,
    wrap=True,
)
```

### Spin buttons: `show_spin_buttons`

```python
field = ttk.NumericEntry(app, label="Quantity", value=1, show_spin_buttons=False)
```

### Formatting: `value_format`

Commit-time, locale-aware formatting:

```python
ttk.NumericEntry(app, label="Currency", value=1234.56, value_format="currency").pack()
ttk.NumericEntry(app, label="Fixed Point", value=15422354, value_format="fixedPoint").pack()
ttk.NumericEntry(app, label="Percent", value=0.35, value_format="percent").pack()
```

<figure markdown>
![numeric formats](../../assets/dark/widgets-numericentry-formats.png#only-dark)
![numeric formats](../../assets/light/widgets-numericentry-formats.png#only-light)
</figure>

---

## Behavior

### Add-ons

Like other field controls, `NumericEntry` supports prefix and suffix add-ons.

```python
salary = ttk.NumericEntry(app, label="Salary")
salary.insert_addon(ttk.Label, position="before", icon="currency-euro")

size = ttk.NumericEntry(app, label="Size", show_spin_buttons=False)
size.insert_addon(ttk.Label, position="after", text="cm", font="label[9]")
```

<figure markdown>
![addons](../../assets/dark/widgets-numericentry-addons.png#only-dark)
![addons](../../assets/light/widgets-numericentry-addons.png#only-light)
</figure>

---

## Events

`NumericEntry` emits standard field events:

- `<<Input>>` / `on_input` — live typing

- `<<Changed>>` / `on_changed` — committed value changed

- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>` — validation lifecycle

It also emits step intent events:

- `<<Increment>>` / `on_increment`

- `<<Decrement>>` / `on_decrement`

```python
def handle_changed(event):
    print("changed:", event.data)

qty.on_changed(handle_changed)

def handle_increment(event):
    print("increment requested")

qty.on_increment(handle_increment)
```

!!! tip "Live typing"
    Use `on_input(...)` for live UX (previews), and `on_changed(...)` for committed values.

---

## Validation and constraints

Use numeric options for guardrails:

- `minvalue` / `maxvalue` for bounds

- `increment` for step size

Use validation rules for business logic:

```python
qty = ttk.NumericEntry(app, label="Quantity", minvalue=0, maxvalue=999, required=True)
qty.add_validation_rule("required", message="Quantity is required")
```

---

## When should I use NumericEntry?

Use `NumericEntry` when:

- users type numbers and you want reliable parsing + validation

- bounds and stepping help prevent errors

- you want locale-aware display formatting on commit

Prefer **SpinnerEntry** when:

- stepping is the primary interaction (visible step buttons matter)

Prefer **Scale** when:

- users adjust by feel and live feedback matters

Prefer **Spinbox** when:

- you need the lowest-level ttk spinbox behavior and options

---

## Related widgets

- **TextEntry** — general field control with validation and formatting

- **SpinnerEntry** — stepped field control

- **Spinbox** — low-level stepper primitive

- **Scale** — slider-based numeric adjustment

- **Form** — build forms from field definitions

---

## Reference

- **API Reference:** `ttkbootstrap.NumericEntry`

---

## Additional resources

### Related widgets

- [DateEntry](dateentry.md)

- [LabeledScale](labeledscale.md)

- [PasswordEntry](passwordentry.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.NumericEntry`](../../reference/widgets/NumericEntry.md)
