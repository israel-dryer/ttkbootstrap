---
title: NumericEntry
icon: fontawesome/solid/hashtag
---

# NumericEntry

`NumericEntry` is a **high-level numeric input control** designed for real desktop apps.

It builds on ttkbootstrap’s `Field` foundation (label + input + message + validation) and uses a numeric entry part under the hood, adding:

- **Min/Max bounds**
- **Stepping** (spin buttons, Up/Down keys, mouse wheel)
- Optional **wrap** at boundaries
- Optional **locale-aware formatting** via `value_format` + `locale`
- Structured virtual events like `<<Input>>`, `<<Changed>>`, `<<Valid>>`, `<<Invalid>>` (and more)

> _Image placeholder:_  
> `![NumericEntry overview](../_img/widgets/numericentry/overview.png)`  
> Suggested shot: quantity + price + percent examples, with spin buttons.

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
    message="How many items?"
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
    wrap=True
)
percent.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![NumericEntry wrap](../_img/widgets/numericentry/wrap.png)`

---

## Stepping (spin buttons, keyboard, mouse wheel)

`NumericEntry` supports stepping in multiple ways:

- **Spin buttons** (default)
- **Up / Down** arrow keys
- **Mouse wheel** (when supported by platform)

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

## Formatting & locale

If you want formatting on commit (blur/Enter), use `value_format` and optionally `locale`.

```python
import ttkbootstrap as ttk

app = ttk.App()

amount = ttk.NumericEntry(
    app,
    label="Amount",
    value=1234.56,
    value_format="$#,##0.00",
    locale="en_US",
)
amount.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![NumericEntry formatted](../_img/widgets/numericentry/formatting.png)`

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

Because it’s a `Field`-based control, you can add validation rules the same way you do for `TextEntry`.

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.NumericEntry(app, label="Quantity", minvalue=0, maxvalue=999, required=True)
qty.add_validation_rule("required", message="Quantity is required")
qty.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

!!! tip "Numeric contraints"
    Rely on `minvalue`/`maxvalue`, and use validation rules for “business rules” (e.g., required, max digits, etc.).

---

## Events

`NumericEntry` forwards structured virtual events from the underlying numeric entry part, including:

- `<<Input>>` — each keystroke (raw text)
- `<<Changed>>` — committed value changed (blur/Enter)
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>` — validation outcomes
- `<<Increment>>`, `<<Decrement>>` — stepping requested (before step occurs)

Example: reacting to committed changes

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.NumericEntry(app, label="Quantity", value=1, minvalue=0, maxvalue=20)
qty.pack(fill="x", padx=20, pady=10)

def on_changed(event):
    # event.data typically includes: value, prev_value, text
    print("changed:", event.data)

qty.bind("<<Changed>>", on_changed)

app.mainloop()
```

Example: intercept increment/decrement requests

```python
def on_increment(event):
    print("increment requested")

qty.bind("<<Increment>>", on_increment)
```

---

## Add-ons

Because this is a `Field`, you can add prefix/suffix widgets inside the field container.

```python
import ttkbootstrap as ttk

app = ttk.App()

amount = ttk.NumericEntry(app, label="Amount", value=0, minvalue=0, maxvalue=9999)
amount.insert_addon(ttk.Label, position="before", text="$")
amount.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![NumericEntry addon](../_img/widgets/numericentry/addons.png)`

---

## When should I use NumericEntry?

Use `NumericEntry` when:

- you want a **single, consistent numeric input control**
- you need **bounds**, **stepping**, and a **message/validation area**
- you’re building forms or dialogs and want a “ready” control

Use the base `Spinbox` / raw `Entry` when:

- you want the lowest-level ttk behavior
- you are building your own composite control

---

## Related widgets

- **TextEntry** — general text input with label, validation, formatting
- **SpinnerEntry** — spinner-style input for text or numeric values
- **Scale** — slider-based numeric adjustment
- **Form** — build forms from definitions and reuse entry widgets
