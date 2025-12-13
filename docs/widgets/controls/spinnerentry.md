---
title: SpinnerEntry
icon: fontawesome/solid/sort
---


# SpinnerEntry

`SpinnerEntry` is a **Field-powered spinner control** that blends `Spinbox` behaviors with all the
labeling, messaging, and validation helpers you expect from ttkbootstrap composites.

It supports both **predefined lists of values** and **numeric ranges**, complete with optional wrapping
and locale-aware formatting, so it works equally well for enumerations, units, dates, and amounts.

---

## Overview

`SpinnerEntry` builds on `Field` to deliver:

- **Spinner controls** (up/down arrows) built in next to the `Entry`.
- **Text mode** (`values`) that cycles through a list you provide.
- **Numeric mode** (`minvalue`/`maxvalue`/`increment`) for ranged steps.
- **Keyboard + mouse wheel** support for adjustment.
- **Optional wrap** to cycle at boundaries instead of clamping.
- **Locale-aware number formatting** via `value_format` and `locale`.
- **Field goodness** (labels, messages, validation, addons, bootstyles).

The control keeps user input constrained to valid choices while remaining compact and keyboard-friendly.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(title="Spinner Entry Demo", theme="cosmo")

size_spinner = ttk.SpinnerEntry(
    app,
    label="Size",
    values=["XS", "S", "M", "L", "XL"],
    value="M",
    message="Choose a size"
)
size_spinner.pack(fill="x", padx=16, pady=8)

quantity_spinner = ttk.SpinnerEntry(
    app,
    label="Quantity",
    minvalue=1,
    maxvalue=20,
    increment=1,
    value=1,
    message="Use arrows or type a number"
)
quantity_spinner.pack(fill="x", padx=16, pady=8)

currency_spinner = ttk.SpinnerEntry(
    app,
    label="Price",
    value=9.99,
    minvalue=0,
    maxvalue=999.99,
    increment=0.25,
    value_format="$#,##0.00",
    wrap=True
)
currency_spinner.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Modes, wrapping, and validation

SpinnerEntry has two mutually exclusive modes:

- **Text mode** (`values` arg): cycles through the provided list and ignores `minvalue`/`maxvalue`.
- **Numeric mode** (`minvalue` + `maxvalue`): steps through a numeric range with `increment`.

Use `wrap=True` to loop values at the boundaries (useful for priority wheels, days of the week, etc.).
The widget also inherits all `Field` validation hooks, so you can call `add_validation_rule`,
use `required=True`, or configure `allow_blank=True` to handle optional input.

---

## Formatting & localization

```python
spinner = ttk.SpinnerEntry(
    app,
    label="Tax rate",
    minvalue=0,
    maxvalue=1,
    increment=0.01,
    value=0.07,
    value_format="percent",
    locale="en_US"
)
spinner.pack(fill="x", padx=16)
```

`value_format` accepts any `IntlFormatter` pattern (`percent`, `currency`, `#,##0.00`, etc.)
and `locale` keeps the formatting consistent for your audience.

---

## Events & interaction

SpinnerEntry forwards the familiar `Field` events:

- `<<Changed>>`: fires when the committed value changes (blur, Enter, spinner buttons).
- `<<Input>>`: emits on every keystroke.
- `<<Valid>>` / `<<Invalid>>`: tied to validation state changes.

You also get keyboard + mouse wheel handling out of the box, so users can step without touching the buttons.

---

## When to choose SpinnerEntry

Use `SpinnerEntry` whenever your input is a **fixed enumeration or bounded range** that users should cycle through,
and you want built-in spin buttons and strict value control.

If you need freeform text input that still validates (with formatting or addons), pick `TextEntry`.  
If you only need basic numeric typing with optional steppers, consider `NumericEntry`.

---

## Related widgets

- `NumericEntry`
- `TextEntry`
- `Entry`
- `Form`

