---
title: NumericEntry
icon: fontawesome/solid/hashtag
---

# NumericEntry

`NumericEntry` is a `Field`-backed numeric spinner that combines themed spin buttons with validation, formatting, and structured events.

---

## Overview

`NumericEntry` bundles:

- Spin buttons (`plus`/`minus` icons) plus keyboard/mouse wheel stepping.
- Min/max bounds enforcement with optional `wrap` behavior.
- Locale-aware formatting via `value_format`, `locale`, and `increment`.
- Full `Field` features (labels, messages, validation rules, addons, bootstyle tokens).

Use it when you need numeric input that stays consistent with your theme and validation rules.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

age = ttk.NumericEntry(
    app,
    label="Age",
    value=25,
    minvalue=0,
    maxvalue=120,
    message="Use the arrows or wheel to adjust"
)
age.pack(fill="x", padx=16, pady=8)

price = ttk.NumericEntry(
    app,
    label="Price",
    value=99.99,
    minvalue=0,
    maxvalue=10000,
    increment=0.25,
    value_format="$#,##0.00",
    bootstyle="success"
)
price.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Validation, bounds, & wrapping

`NumericEntry` enforces bounds automatically:

- `minvalue`/`maxvalue` clamp numeric ranges.
- `wrap=True` cycles values when the user hits the boundary (handy for degrees or times).
- Field validation messages appear in the message area, and you can still call `add_validation_rule()` or use `required=True`/`allow_blank=True` for business logic.

---

## Formatting & localization

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

rate = ttk.NumericEntry(
    app,
    label="Tax rate",
    value=0.075,
    increment=0.005,
    value_format="percent",
    locale="en_US"
)
rate.pack(fill="x", padx=16)

app.mainloop()
```

For `value_format`, use any `IntlFormatter` pattern (`decimal`, `percent`, `currency`, or custom `#,##0.00`) and pair it with `locale` for audience-specific formatting.

---

## Events & interaction

`NumericEntry` exposes Field events plus spin-specific hooks:

- `<<Increment>>` / `<<Decrement>>` fire before a step and support `on_increment`, `on_decrement`, or manual `step()` calls.
- `<<Changed>>` fires when the parsed value commits, and `<<Input>>`, `<<Valid>>`, and `<<Invalid>>` behave like other `Field` widgets.
- Hide the spin buttons (`show_spin_buttons=False`) when you only want keyboard input but still benefit from formatting and validation.

---

## Styling & appearance

- `bootstyle` selects accent colors (`primary`, `danger`, `success`) and `surface_color` tweaks the fill when embedded in cards.
- Use `style_options` to forward tokens (e.g., `{"padding": (8, 6)}`) when you need finer layout control.
- Combine `increment`, `wrap`, and `show_spin_buttons` to define the control’s behavior and message (e.g., add hints when wrapping or hide the buttons for compact forms).

---

## When to use NumericEntry

Choose `NumericEntry` when you need:

- a numeric field that honors bootstyle tokens and validation messaging,
- built-in spin buttons plus keyboard/mouse stepping,
- automatic bounds, wrapping, and locale-aware formatting,
- Field conveniences (labels, messages, addons, structured events).

If you only need an unlabeled text field, use `Entry`; for multi-field forms consider `TextEntry`, `Form`, or `SpinnerEntry`.

---

## Related widgets

- `TextEntry`
- `Entry`
- `DateEntry`
- `TimeEntry`
- `Form`
