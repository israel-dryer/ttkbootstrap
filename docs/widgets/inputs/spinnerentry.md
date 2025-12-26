---
title: SpinnerEntry
---

# SpinnerEntry

`SpinnerEntry` is a form-ready input control with integrated step buttons.

It's designed for values that users change in small steps, while still allowing typing. It supports formatting,
validation, localization, and consistent field events like other entry controls.

<figure markdown>
![spinnerentry states](../../assets/dark/widgets-spinnerentry-states.png#only-dark)
![spinnerentry states](../../assets/light/widgets-spinnerentry-states.png#only-light)
</figure>

---

## Quick start

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

## When to use

Use `SpinnerEntry` when:

- stepping is the primary interaction
- users frequently increment/decrement values
- visible step buttons improve UX

### Consider a different control when...

- users primarily type numbers and stepping is secondary -> use [NumericEntry](numericentry.md)
- you need bounds (`minvalue`/`maxvalue`) and clamping/wrapping behavior -> use [NumericEntry](numericentry.md)
- users adjust continuously -> use [Scale](scale.md)

---

## Examples and patterns

### Value model

SpinnerEntry uses the same **text vs committed value** model as other field controls.

```python
current = qty.value
raw = qty.get()

qty.value = 10
```

Commit-time parsing/formatting happens on blur or Enter.

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

!!! link "Localization"
    Currency and number formatting respects locale settings. See [Localization](../../capabilities/localization.md) for details.

### Add-ons

```python
amount = ttk.SpinnerEntry(app, label="Amount", value=0, increment=1)
amount.insert_addon(ttk.Label, position="before", text="$")
```

<figure markdown>
![spinnerentry addons](../../assets/dark/widgets-spinnerentry-addons.png#only-dark)
![spinnerentry addons](../../assets/light/widgets-spinnerentry-addons.png#only-light)
</figure>

### Events

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

### Validation and constraints

Use validation rules for business constraints:

```python
limit = ttk.SpinnerEntry(app, label="Retry limit", value=3, increment=1, required=True)
limit.add_validation_rule("required", message="A value is required")
```

If you need numeric bounds, prefer **NumericEntry** (min/max) unless SpinnerEntry also supports them in your implementation.

---

## Behavior

SpinnerEntry supports stepping via:

- spin buttons
- Up / Down arrow keys
- mouse wheel (platform-dependent)

Typing is always allowed unless you set the underlying entry to readonly.

---

## Additional resources

### Related widgets

- [NumericEntry](numericentry.md) - validated numeric input with bounds
- [Spinbox](../primitives/spinbox.md) - low-level stepper primitive
- [TextEntry](textentry.md) - general field control
- [Scale](scale.md) - slider-based numeric adjustment
- [Form](../forms/form.md) - build forms from field definitions

### API reference

- [`ttkbootstrap.SpinnerEntry`](../../reference/widgets/SpinnerEntry.md)