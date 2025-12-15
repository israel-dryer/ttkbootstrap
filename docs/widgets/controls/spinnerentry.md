---
title: SpinnerEntry
icon: fontawesome/solid/sort
---

# SpinnerEntry

`SpinnerEntry` is a fully featured input control with built-in step buttons, including a label,
input field, and message text.

It builds on ttkbootstrap’s field system and spinbox behavior, adding the things you almost
always need when users step through values.

If you are building forms or dialogs where values change incrementally,
`SpinnerEntry` is usually your **default stepped input**.

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

## Text vs value

All Entry-based controls separate **what the user is typing** from the **committed value**.

| Concept | Meaning |
|---|---|
| Text | Raw, editable string while the field is focused |
| Value | Parsed, validated value committed on blur or Enter |

```python
# get committed value
current = field.value

# set committed value programmatically
field.value = ...
```

If you need the raw text at any time:

```python
raw = field.get()
```

!!! tip "Commit semantics"
    Parsing, validation, and `value_format` are applied **only when the value is committed**
    (blur or Enter), never on every keystroke.

---

## Stepping behavior

SpinnerEntry supports several stepping interactions:

- Step buttons (mouse)
- Up / Down arrow keys
- Mouse wheel (platform-dependent)

Control the step size with `increment`.

```python
price = ttk.SpinnerEntry(
    app,
    label="Unit price",
    value=9.99,
    increment=0.01,
)
price.pack(fill="x", padx=20, pady=10)
```

---

## Formatting with `value_format`

`SpinnerEntry` supports the same **commit-time formatting** model as `TextEntry`
and `NumericEntry`.

Formatting is applied when the value is committed (blur or Enter), allowing users
to type naturally while editing.

### Named formats

```python
row = ttk.Frame(app, padding=10)
row.pack(fill="x")

ttk.SpinnerEntry(
    row,
    label="Currency",
    value=9.99,
    increment=0.01,
    value_format="currency",
).pack(side="left", padx=10)

ttk.SpinnerEntry(
    row,
    label="Fixed Point",
    value=1500,
    increment=10,
    value_format="fixedPoint",
).pack(side="left", padx=10)

ttk.SpinnerEntry(
    row,
    label="Percent",
    value=0.25,
    increment=0.05,
    value_format="percent",
).pack(side="left", padx=10)
```

!!! tip "Commit-time formatting"
    Formatting is applied only when the value is committed, not while typing.

<figure markdown>
![spinnerentry formatting](../../assets/dark/widgets-spinnerentry-formats.png#only-dark)
![spinnerentry formatting](../../assets/light/widgets-spinnerentry-formats.png#only-light)
</figure>

---

## Validation

SpinnerEntry supports validation rules just like other field controls.

```python
limit = ttk.SpinnerEntry(
    app,
    label="Retry limit",
    value=3,
    increment=1,
    required=True,
)
limit.add_validation_rule("required", message="A value is required")
limit.pack(fill="x", padx=20, pady=10)
```

---

## Events

SpinnerEntry emits structured events with convenience bindings:

- `<<Input>>` — raw typing
- `<<Changed>>` — committed value changed
- `<<Increment>>`, `<<Decrement>>` — step requested
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

Example:

```python
def on_changed(event):
    print("new value:", event.data["value"])

qty.on_changed(on_changed)
```

---

## Add-ons

Because this is a field control, you can insert prefix or suffix widgets.

```python
amount = ttk.SpinnerEntry(app, label="Amount", value=0, increment=1)
amount.insert_addon(ttk.Label, position="before", text="$")
amount.pack(fill="x", padx=20, pady=10)
```

<figure markdown>
![spinnerentry addons](../../assets/dark/widgets-spinnerentry-addons.png#only-dark)
![spinnerentry addons](../../assets/light/widgets-spinnerentry-addons.png#only-light)
</figure>

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, `label`, `message`, and `text`
are treated as localization keys **when a translation exists**.
If no translation is found, the value is shown as **plain text**.

You can override this behavior per widget if needed.

```python
# global app localization (default)
ttk.SpinnerEntry(app, label="order.quantity").pack(fill="x")

# explicitly enable localization
ttk.SpinnerEntry(app, label="order.quantity", localize=True).pack(fill="x")

# explicitly disable localization
ttk.SpinnerEntry(app, label="Quantity", localize=False).pack(fill="x")
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, you may pass either localization keys or literal strings.

---

## When should I use SpinnerEntry?

Use `SpinnerEntry` when:

- stepping is the **primary interaction**
- users frequently adjust values up or down
- you want a labeled field with built-in step controls

Prefer **NumericEntry** when:

- users primarily type numbers
- stepping is optional or secondary

---

## Related widgets

- **NumericEntry** — typed numeric input with optional stepping
- **TextEntry** — general text input with validation and formatting
- **Scale** — slider-based numeric adjustment
- **Form** — build forms from definitions
