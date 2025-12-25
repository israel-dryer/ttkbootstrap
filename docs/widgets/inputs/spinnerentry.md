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

title: SpinnerEntry
---

# SpinnerEntry

`SpinnerEntry` is a form-ready input control with integrated step buttons.

It’s designed for values that users change in small steps, while still allowing typing. It supports formatting,
validation, localization, and consistent field events like other entry controls. fileciteturn14file3

<figure markdown>
![spinnerentry states](../../assets/dark/widgets-spinnerentry-states.png#only-dark)
![spinnerentry states](../../assets/light/widgets-spinnerentry-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.SpinnerEntry(
    app,
    label="Quantity",
    value=1,
    increment=1,
    message="How many items?",
)
qty.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

SpinnerEntry uses the same **text vs committed value** model as other field controls.

```python
current = qty.value
raw = qty.get()

qty.value = 10
```

Commit-time parsing/formatting happens on blur or Enter.

---

## Common options

### `increment`

Controls step size for buttons/keys/wheel.

```python
ttk.SpinnerEntry(app, label="Retry limit", value=3, increment=1)
```

### Formatting: `value_format`

```python
ttk.SpinnerEntry(app, label="Price", value=9.99, increment=0.01, value_format="currency").pack()
```

<figure markdown>
![spinnerentry formatting](../../assets/dark/widgets-spinnerentry-formats.png#only-dark)
![spinnerentry formatting](../../assets/light/widgets-spinnerentry-formats.png#only-light)
</figure>

### Add-ons

```python
amount = ttk.SpinnerEntry(app, label="Amount", value=0, increment=1)
amount.insert_addon(ttk.Label, position="before", text="$")
```

<figure markdown>
![spinnerentry addons](../../assets/dark/widgets-spinnerentry-addons.png#only-dark)
![spinnerentry addons](../../assets/light/widgets-spinnerentry-addons.png#only-light)
</figure>

---

## Behavior

SpinnerEntry supports stepping via:

- spin buttons

- Up / Down arrow keys

- mouse wheel (platform-dependent)

Typing is always allowed unless you set the underlying entry to readonly.

---

## Events

SpinnerEntry emits standard field events:

- `<<Input>>` / `on_input`

- `<<Changed>>` / `on_changed`

- validation lifecycle events

It also emits step intent events:

- `<<Increment>>` / `on_increment`

- `<<Decrement>>` / `on_decrement`

```python
def on_changed(event):
    print("new value:", event.data["value"])

qty.on_changed(on_changed)

def on_increment(event):
    print("increment requested")

qty.on_increment(on_increment)
```

---

## Validation and constraints

Use validation rules for business constraints:

```python
limit = ttk.SpinnerEntry(app, label="Retry limit", value=3, increment=1, required=True)
limit.add_validation_rule("required", message="A value is required")
```

If you need numeric bounds, prefer **NumericEntry** (min/max) unless SpinnerEntry also supports them in your implementation.

---

## When should I use SpinnerEntry?

Use `SpinnerEntry` when:

- stepping is the primary interaction

- users frequently increment/decrement values

- visible step buttons improve UX

Prefer **NumericEntry** when:

- users primarily type numbers and stepping is secondary

- you need bounds (`minvalue`/`maxvalue`) and clamping/wrapping behavior

Prefer **Scale** when:

- users adjust continuously

---

## Related widgets

- **NumericEntry** — validated numeric input with bounds

- **Spinbox** — low-level stepper primitive

- **TextEntry** — general field control

- **Scale** — slider-based numeric adjustment

- **Form** — build forms from field definitions

---

## Reference

- **API Reference:** `ttkbootstrap.SpinnerEntry`

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

- [`ttkbootstrap.Spinnerentry`](../../reference/widgets/Spinnerentry.md)
