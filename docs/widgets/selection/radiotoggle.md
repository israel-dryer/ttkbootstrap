---
title: RadioToggle
---

# RadioToggle

`RadioToggle` is a `RadioButton` variant that renders with a **toggle badge** style.

Use `RadioToggle` when you want mutually exclusive choices, but prefer a more “button-like” presentation
than the classic radio indicator (common in toolbars, view switches, or mode pickers).

---

## Overview

`RadioToggle` behaves like `RadioButton`:

- it participates in a mutually exclusive group via a shared `signal` or `variable`
- selecting it sets the shared value to its `value`

The difference is purely presentational: `RadioToggle` coerces `bootstyle` to a toolbutton-style badge
(e.g. `primary-toolbutton`, `success-toolbutton`).

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

view = ttk.Signal("grid")

ttk.RadioToggle(app, text="Grid", signal=view, value="grid").pack(side="left", padx=4, pady=10)
ttk.RadioToggle(app, text="List", signal=view, value="list").pack(side="left", padx=4, pady=10)

app.mainloop()
```

---

## Variants

### Bootstyle coercion

`RadioToggle` defaults `bootstyle` to `"Toolbutton"`, and ensures it includes `"-toolbutton"`.

```python
ttk.RadioToggle(app)
ttk.RadioToggle(app, bootstyle="success)
```

---

## How the value works

Same as `RadioButton`:

- `value` is the option represented by this toggle
- the shared signal/variable holds the selected value
- selection is committed on click (or keyboard select)

---

## Binding to signals or variables

Bind a shared `signal` (preferred) or `variable` just like a radio button.

```python
mode = ttk.Signal("basic")
ttk.RadioToggle(app, text="Basic", signal=mode, value="basic")
ttk.RadioToggle(app, text="Pro", signal=mode, value="pro")
```

---

## Common options

`RadioToggle` supports the same constructor options as `RadioButton` (text, icon, command, state, etc.).

---

## Behavior

- Mutually exclusive selection through shared state
- Visual emphasis matches toolbutton/badge styling
- Typically used in compact areas like toolbars

---

## Events

Use `command=` for a per-toggle callback, or subscribe to the shared signal for group-level changes.

---

## Validation and constraints

Same as `RadioButton`: selection is constrained to the values represented by the group.

---

## Colors and styling

Use semantic color tokens; they are coerced to the toolbutton variant automatically.

```python
ttk.RadioToggle(app, bootstyle="primary")
ttk.RadioToggle(app, bootstyle="secondary")
ttk.RadioToggle(app, bootstyle="success")
```

---

## Localization

`RadioToggle` text follows the same localization behavior as other widgets that support `text` / `textvariable`.

---

## When should I use RadioToggle?

Use `RadioToggle` when:

- you want single selection
- the control is part of a compact UI (toolbar, header controls)
- a button-like appearance is more discoverable than a radio indicator

Prefer **RadioButton** when:

- classic form-style radio indicators are expected
- the control appears in a traditional settings form

---

## Related widgets

- **RadioButton** — classic radio indicator
- **RadioGroup** — composite group builder
- **ButtonGroup / ToggleGroup** — grouped button-style selection patterns

---

## Reference

- **API Reference:** `ttkbootstrap.RadioToggle`
