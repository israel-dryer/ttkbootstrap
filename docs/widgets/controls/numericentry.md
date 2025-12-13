---
title: NumericEntry
icon: fontawesome/solid/hashtag
---


# NumericEntry

`NumericEntry` is a **specialized numeric field control** that builds on `TextEntry` and `Entry` to deliver
stepper buttons, bounds checking, locale-aware formatting, and data-aware events in one composable widget.

Use it whenever you accept integer or floating-point input and want consistent validation, messaging, and keyboard/mouse-friendly stepping.

---

## Overview

`NumericEntry` renders an entry field augmented with:

- **Spin buttons** (plus/minus icons) for mouse-friendly stepping.
- **Keyboard stepping** via Up/Down arrow keys and optional mouse-wheel support.
- **Min/max bounds checking** with optional wrapping behavior.
- **Locale-aware value formatting** through `value_format` and `locale` arguments.
- **All `Field` features** such as labels, messages, validation hooks, and addons.

The widget produces the same consistent experience whether you are asking for quantities, prices, ratios, or percentages.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(title="Numeric Entry Demo", themename="cosmo")

age = ttk.NumericEntry(
    app,
    label="Age",
    value=25,
    minvalue=0,
    maxvalue=120,
    message="Use arrows, wheel, or buttons to adjust"
)
age.pack(fill="x", padx=16, pady=8)

price = ttk.NumericEntry(
    app,
    label="Price",
    value=99.99,
    minvalue=0,
    maxvalue=10000,
    increment=0.25,
    value_format="$#,##0.00"
)
price.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Validation, bounds, & wrapping

`NumericEntry` enforces bounds automatically:

- Use `minvalue`/`maxvalue` to clamp values to a known range.
- Set `wrap=True` to cycle at the boundaries (handy for degrees, clocks, etc.).
- The underlying `Field` validation infrastructure surfaces messages in the `message` area, and you can still call `add_validation_rule` for business-specific checks.

You can also enable `required=True` or `allow_blank=True` from `FieldOptions` to control whether empty input is permitted.

---

## Formatting & localization

```python
rate = ttk.NumericEntry(
    app,
    label="Tax rate",
    value=0.075,
    increment=0.005,
    value_format="percent",
    locale="en_US"
)
rate.pack(fill="x", padx=16)
```

Set `value_format` to any format that `IntlFormatter` supports (decimal, percent, currency, or a custom pattern like `#,##0.00`).
Combine that with `locale` to keep formatting consistent across regions.

---

## Events & interaction

`NumericEntry` exposes event hooks from the internal spin buttons and entry part:

- `<<Increment>>` / `<<Decrement>>`: fire before a step occurs.
- `<<Changed>>`: fires whenever the parsed value commits (on blur or Enter).
- `<<Input>>`, `<<Valid>>`, and `<<Invalid>>` behave the same as other `Field` widgets.

You can also call `on_increment`, `on_decrement`, and `step()` to customize behavior programmatically.

Spin buttons can be hidden via `show_spin_buttons=False` if you only want the `Entry` experience while keeping validation and formatting.

---

## When to use NumericEntry

Choose `NumericEntry` when you need:

- an entry that speaks numbers rather than free text,
- built-in stepping via mouse/keyboard + spin buttons,
- automatic min/max clamping or wrapping,
- formatted values tied to a locale or currency,
- and every `Field` nicety (labels, messages, validation, addons).

If you only need a bare `ttk.Entry`, use `Entry`; if you want the same features with a wider range of edit types, consider `TextEntry` or `Form` integrations.

---

## Related widgets

- `TextEntry`
- `Entry`
- `DateEntry`
- `TimeEntry`
- `Form`
