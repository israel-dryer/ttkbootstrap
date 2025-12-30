---
title: CheckToggle
---

# CheckToggle

`CheckToggle` is a **selection control** for turning an option **on/off (or mixed)**, rendered with a
**Toolbutton-style toggle** appearance.

It behaves like `CheckButton`, but uses the Toolbutton variant style by default.

Use `CheckToggle` when you want checkbox semantics in compact UI areas like toolbars, headers, and mode strips.

---

## Overview

`CheckToggle` supports the same logical states as `CheckButton`:

- **checked** (`True`)

- **unchecked** (`False`)

- **indeterminate** (`None`)

It differs from `CheckButton` primarily in presentation: it uses the toolbutton variant style so it reads more like
a pressed/unpressed control than a checkbox indicator.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.CheckToggle(app, text="Bold", value=False).pack(side="left", padx=4, pady=10)
ttk.CheckToggle(app, text="Italic", value=True).pack(side="left", padx=4, pady=10)

app.mainloop()
```

---

## Variants

`CheckToggle` is itself the "toggle" presentation of checkbox semantics.

If you want the classic indicator, use `CheckButton` instead.

---

## How the value works

The `value` option sets the initial state (defaults to `None` when unset).

- `True` -> checked

- `False` -> unchecked

- `None` -> indeterminate

Once bound, the signal or variable becomes the source of truth.

!!! note "Value precedence"
    The `value` option is only used during initialization.
    After creation, the bound signal or variable controls the widget state.

---

## Binding to signals or variables

`CheckToggle` supports the same bindings as `CheckButton`:

- `signal=...` (reactive, preferred in v2)

- `variable=...` (Tk variable)

```python
import ttkbootstrap as ttk

app = ttk.App()

enabled = ttk.Signal(False)

t = ttk.CheckToggle(app, text="Snap", signal=enabled)
t.pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

`CheckToggle` accepts the same constructor options as `CheckButton`, including:

- `text`, `textvariable`, `textsignal`

- `command`

- `variable`, `signal`, `value`

- `onvalue`, `offvalue`

- `padding`, `width`, `underline`

- `state`, `takefocus`

- `style`, `color`, `variant`, `surface_color`, `style_options`

---

## Behavior

- Click toggles between checked/unchecked.

- Indeterminate behavior is driven by your app logic (commonly used for mixed/partial states).

- Visual emphasis matches toolbutton styling, making it suitable for dense UI regions.

---

## Events

Use `on_changed` (or `command`) the same way you would for `CheckButton`.

```python
def on_changed(e):
    print("value:", t.value)

t.on_changed(on_changed)
```

---

## Validation and constraints

Validation is usually minimal.

Use validation when:

- the toggle must be set to proceed

- indeterminate must be resolved

- the selection participates in cross-field rules

---

## Colors and styling

Use semantic color tokens with the `color` parameter.

```python
ttk.CheckToggle(app, color="primary")
ttk.CheckToggle(app, color="secondary")
ttk.CheckToggle(app, color="success")
ttk.CheckToggle(app, color="warning")
ttk.CheckToggle(app, color="danger")
```

---

## Localization

Text localization follows your standard widget localization behavior (`localize="auto"` where supported).

---

## When should I use CheckToggle?

Use `CheckToggle` when:

- you want on/off selection with a **button-like** presentation

- the control lives in a toolbar or compact header area

Prefer **CheckButton** when:

- classic checkbox indicators are expected in forms and settings panels

Prefer **Switch** when:

- you want a slider-style on/off toggle for settings

---

## Additional resources

### Related widgets

- [Switch](switch.md) - slider-style on/off toggle for settings
- [CheckButton](checkbutton.md) - classic checkbox indicator (multi-selection / tri-state)
- [RadioToggle](radiotoggle.md) - mutually exclusive button-like radios
- [ButtonGroup](../actions/buttongroup.md) - visually grouped controls for toolbars and headers

### API reference

- [`ttkbootstrap.CheckToggle`](../../reference/widgets/CheckToggle.md)