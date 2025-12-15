---
title: NumericEntry
icon: fontawesome/solid/hashtag
---

# NumericEntry

`NumericEntry` is a **high-level numeric input control** for desktop apps.

It builds on ttkbootstrap’s field foundation (label + input + message + validation) and adds:

- **Min/Max bounds**
- **Stepping** (spin buttons, Up/Down keys, mouse wheel)
- Optional **wrap** at boundaries
- **Commit-time formatting** via `value_format`
- Structured events like `<<Input>>`, `<<Changed>>`, `<<Valid>>`, `<<Invalid>>` (and more)

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

## Min/Max bounds

Use `minvalue` and `maxvalue` to constrain input.

```python
import ttkbootstrap as ttk

app = ttk.App()

age = ttk.NumericEntry(app, label="Age", value=25, minvalue=0, maxvalue=120)
age.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

### Clamp vs wrap

- Default behavior is **clamp** (stop at min/max).
- Enable `wrap=True` to cycle through min/max.

```python
import ttkbootstrap as ttk

app = ttk.App()

percent = ttk.NumericEntry(
    app,
    label="Percent",
    value=50,
    minvalue=0,
    maxvalue=100,
    increment=5,
    wrap=True,
)
percent.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Stepping (spin buttons, keyboard, mouse wheel)

`NumericEntry` supports stepping in multiple ways:

- **Spin buttons** (default)
- **Up / Down** arrow keys
- **Mouse wheel** (when supported by the platform)

Control step size with `increment`.

```python
import ttkbootstrap as ttk

app = ttk.App()

price = ttk.NumericEntry(
    app,
    label="Unit Price",
    value=9.99,
    minvalue=0,
    maxvalue=10000,
    increment=0.01,
)
price.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Formatting with `value_format`

`NumericEntry` supports powerful, locale-aware formatting via `value_format`.

This allows you to:

- accept plain numeric input while editing
- normalize the committed value
- reformat the display when the user finishes editing

Formatting is applied **on commit** (blur or Enter), so it doesn’t fight the user while typing.

### Named numeric formats

These examples show common numeric formats you’ll use in real apps:

<figure markdown>
![numeric formats](../../assets/dark/widgets-numericentry-formats.png#only-dark)
![numeric formats](../../assets/light/widgets-numericentry-formats.png#only-light)

</figure>


```python
import ttkbootstrap as ttk

app = ttk.App()

row = ttk.Frame(app, padding=10)
row.pack(fill="x")

ttk.NumericEntry(
    row,
    label="Currency",
    value=1234.56,
    value_format="currency",
).pack(side="left", padx=10)

ttk.NumericEntry(
    row,
    label="Fixed Point",
    value=15422354,
    value_format="fixedPoint",
).pack(side="left", padx=10)

ttk.NumericEntry(
    row,
    label="Percent",
    value=0.35,
    value_format="percent",
).pack(side="left", padx=10)

app.mainloop()
```

!!! tip "Commit-time formatting"
    `value_format` is applied when the value is committed (blur/Enter). While focused, users can type naturally.


---

## Showing or hiding spin buttons

Spin buttons are enabled by default. Turn them off for a cleaner, keyboard-only field.

```python
import ttkbootstrap as ttk

app = ttk.App()

field = ttk.NumericEntry(
    app,
    label="Quantity",
    value=1,
    show_spin_buttons=False,
)
field.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Reading and setting the value

`NumericEntry` separates:

- **Text**: what the user is typing
- **Value**: parsed numeric value committed on blur/Enter

Common patterns:

```python
# get committed value
current = field.value

# set committed value
field.value = 42
```

If you need the raw text at any time, use:

```python
raw_text = field.get()
```

---

## Validation

Because it’s a field-based control, you can add validation rules the same way you do for `TextEntry`.

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.NumericEntry(app, label="Quantity", minvalue=0, maxvalue=999, required=True)
qty.add_validation_rule("required", message="Quantity is required")
qty.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

!!! tip "Numeric constraints"
    Rely on `minvalue`/`maxvalue` for numeric bounds, and use validation rules for “business rules”
    (e.g., required, maximum digits, etc.).

---

## Events

`NumericEntry` forwards structured virtual events from the underlying entry part. Related `on_*` and `off_*`
convenience bindings are available for the generated events:

- `<<Input>>` — each keystroke (raw text)
- `<<Changed>>` — committed value changed (blur/Enter)
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>` — validation outcomes
- `<<Increment>>`, `<<Decrement>>` — stepping requested (before the step occurs)

Example: reacting to committed changes

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.NumericEntry(app, label="Quantity", value=1, minvalue=0, maxvalue=20)
qty.pack(fill="x", padx=20, pady=10)

def handle_changed(event):
    # event.data typically includes: value, prev_value, text
    print("changed:", event.data)

qty.on_changed(handle_changed)

app.mainloop()
```

Example: intercept increment/decrement requests

```python
def handle_increment(event):
    print("increment requested")

qty.on_increment(handle_increment)
```

---

## Add-ons

Because `NumericEntry` is a field control, you can insert widgets inside its layout. This is a **powerful** feature that allows you
to create customized and specialized entry fields.

<figure markdown>
![addons](../../assets/dark/widgets-numericentry-addons.png#only-dark)
![addons](../../assets/light/widgets-numericentry-addons.png#only-light)
</figure>

```python
salary = ttk.NumericEntry(app, label="Salary")
salary.insert_addon(ttk.Label, position='before', icon='currency-euro')
salary.pack(side='left', padx=10, anchor='s')

size = ttk.NumericEntry(app, label="Size", show_spin_buttons=False)
size.insert_addon(ttk.Button, position='before', icon='rulers')
size.insert_addon(ttk.Label, position='after', text='cm', font='label[9]')
size.pack(side='left', padx=10, anchor='s')
```

!!! note "Power Play"
    Most of the specialized _Entry_ widgets in v2 have been created using this very method.

---

## Colors

NumericEntry support standard ttkbootstrap styling and theming.

<div class="only-dark" style="text-align: center;" markdown="1">
  <video controls autoplay muted loop playsinline width="700">
    <source src="../../../assets/dark/widgets-numericentry-colors.mp4" type="video/mp4">
  </video>
</div>

<div class="only-light" style="text-align: center;" markdown="1">
  <video controls autoplay muted loop playsinline width="700">
    <source src="../../../assets/light/widgets-numericentry-colors.mp4" type="video/mp4">
  </video>
</div>

```python
ttk.NumericEntry(app, value=123456)  # primary is default
ttk.NumericEntry(app, value=123456, bootstyle="secondary")
ttk.NumericEntry(app, value=123456, bootstyle="success")
ttk.NumericEntry(app, value=123456, bootstyle="info")
ttk.NumericEntry(app, value=123456, bootstyle="warning")
ttk.NumericEntry(app, value=123456, bootstyle="danger")
```

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, `label`, `message`, and `text` are treated as localization
keys **when a translation exists**. If a key is not found in the active message catalog, the widget falls back to using
the value as **plain text**.

You can override this behavior per widget if needed.

```python
# uses global app localization settings (default)
ttk.NumericEntry(app, label="order.quantity", message="order.quantity.help").pack(fill="x")

# explicitly enable localization for this widget
ttk.NumericEntry(app, label="order.quantity", localize=True).pack(fill="x")

# explicitly disable localization (always treat strings as literals)
ttk.NumericEntry(app, label="Quantity", message="How many items?", localize=False).pack(fill="x")
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, you can mix localization keys and literal strings.
    If no translation is found, the string is shown as-is.

---

## When should I use NumericEntry?

Use `NumericEntry` when:

- you want a **single, consistent numeric input control**
- you need **bounds**, **stepping**, and a **message/validation area**
- you want commit-time numeric formatting via `value_format`

Use the base `Spinbox` / raw `Entry` when:

- you want the lowest-level ttk behavior
- you are building your own composite control

---

## Related widgets

- **TextEntry** — general text input with label, validation, formatting
- **SpinnerEntry** — spinner-style input for text or numeric values
- **Scale** — slider-based numeric adjustment
- **Form** — build forms from definitions and reuse entry widgets
