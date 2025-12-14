---
title: SpinnerEntry
icon: fontawesome/solid/sort
---

# SpinnerEntry

`SpinnerEntry` is a **high-level “spinbox-style” field control**.

It looks and behaves like a modern input with **up/down step buttons**, but it’s built on ttkbootstrap’s `Field`
foundation — so you also get:

- A **label** and **message** area
- **Validation** + validation feedback
- Optional **localization** and **formatting**
- Consistent **virtual events**
- A layout that fits naturally in **forms** and **dialogs**

Use `SpinnerEntry` when the user is choosing from a *stepped* set of values:
quantities, small ranges, enums like “Low / Medium / High”, or time intervals.

> _Image placeholder:_  
> `![SpinnerEntry overview](../_img/widgets/spinnerentry/overview.png)`  
> Suggested shot: integer stepping, list stepping, disabled, error state.

---

## Basic usage (numeric stepping)

```python
import ttkbootstrap as ttk

app = ttk.App()

count = ttk.SpinnerEntry(
    app,
    label="Count",
    value=1,
    minvalue=0,
    maxvalue=20,
    increment=1,
    message="Use the arrows or type a value",
)
count.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## What problem does SpinnerEntry solve?

A raw `Spinbox` is useful, but it’s still a low-level widget:

- No label or helper/error message
- Validation is ad-hoc per screen
- Styling often differs from other controls
- UX patterns (required fields, errors, add-ons) must be rebuilt repeatedly

`SpinnerEntry` standardizes these behaviors using the same field patterns as `TextEntry` and `NumericEntry`.

---

## Text vs value

Like other entry controls, `SpinnerEntry` distinguishes:

| Concept | Meaning                                         |
|---------|-------------------------------------------------|
| Text    | Raw display text while typing                   |
| Value   | Committed value after validation (blur / Enter) |

```python
# committed value
current = count.value

# set value programmatically
count.value = 10
```

To read raw text at any time:

```python
raw = count.get()
```

---

## Numeric options

`SpinnerEntry` supports the common numeric configuration knobs:

- `minvalue` / `maxvalue` — bounds
- `increment` — step size
- `wrap` — wrap around at boundaries (optional)

```python
import ttkbootstrap as ttk

app = ttk.App()

percent = ttk.SpinnerEntry(
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

> _Image placeholder:_  
> `![SpinnerEntry wrap](../_img/widgets/spinnerentry/wrap.png)`

---

## Stepping behavior

Users can step values via:

- up/down buttons
- Up/Down arrow keys
- mouse wheel (platform-dependent)

You can hide the step buttons if you only want keyboard stepping:

```python
field = ttk.SpinnerEntry(
    app,
    label="Count",
    value=1,
    show_spin_buttons=False,
)
field.pack(fill="x", padx=20, pady=10)
```

---

## List / enum stepping

`SpinnerEntry` can also step through a fixed list of values (commonly used for enums or presets).

```python
import ttkbootstrap as ttk

app = ttk.App()

priority = ttk.SpinnerEntry(
    app,
    label="Priority",
    items=["Low", "Medium", "High"],
    value="Medium",
)
priority.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> Tip: Use `SelectBox` when you want a dropdown list; use `SpinnerEntry` when users benefit from
> quick stepping without opening a popup.

---

## Formatting & localization

If you want formatted display on commit, use `value_format` and optionally `locale`.

```python
import ttkbootstrap as ttk

app = ttk.App()

price = ttk.SpinnerEntry(
    app,
    label="Unit Price",
    value=9.99,
    minvalue=0,
    maxvalue=10000,
    increment=0.01,
    value_format="$#,##0.00",
    locale="en_US",
)
price.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Validation

Because `SpinnerEntry` is `Field`-based, you can add the same validation rules you use for `TextEntry`.

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.SpinnerEntry(app, label="Quantity", required=True, minvalue=1, maxvalue=99)
qty.add_validation_rule("required", message="Quantity is required")
qty.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

Use bounds (`minvalue` / `maxvalue`) for numeric constraints and rules for business logic.

---

## Events

`SpinnerEntry` emits the standard “field” events, plus stepping-related ones. Convenience `on_*` and `off_*` methods
are available for all of these generated events.

### Common field events

- `<<Input>>` — raw typing
- `<<Changed>>` — committed value changed
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

### Spinner events

- `<<Increment>>` — increment requested
- `<<Decrement>>` — decrement requested

Example:

```python
import ttkbootstrap as ttk

app = ttk.App()

field = ttk.SpinnerEntry(app, label="Count", value=1, minvalue=0, maxvalue=10)
field.pack(fill="x", padx=20, pady=10)


def handle_changed(e):
    print("changed:", e.data)


field.on_changed(handle_changed)

app.mainloop()
```

---

## Add-ons (prefix / suffix widgets)

Because this is a field control, you can insert add-ons into the field layout.

```python
import ttkbootstrap as ttk

app = ttk.App()

minutes = ttk.SpinnerEntry(app, label="Timeout", value=5, minvalue=0, maxvalue=60, increment=5)
minutes.insert_addon(ttk.Label, position="after", text="min")
minutes.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_  
> `![SpinnerEntry addon](../_img/widgets/spinnerentry/addon.png)`

---

## When should I use SpinnerEntry?

Use `SpinnerEntry` when:

- users should step through values quickly
- the value is a small numeric range or preset list
- you want the full “field” experience (label, message, validation)

Prefer **NumericEntry** when:

- the value is strictly numeric and you want numeric-first behavior everywhere

Prefer **SelectBox** when:

- users need to browse or search a longer list

Prefer base **Spinbox** when:

- you want the raw ttk widget with minimal structure

---

## Related widgets

- **NumericEntry** — numeric field with bounds and stepping
- **TextEntry** — general text field with label and validation
- **SelectBox** — dropdown picker with optional search
- **Scale** — slider-style numeric adjustment
- **Form** — build complete forms using field controls
