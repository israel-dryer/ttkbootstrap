---
title: CheckToggle
---

# CheckToggle

`CheckToggle` is a **selection control** for turning an option **on/off (or mixed)**, rendered with a
**Toolbutton-style toggle** appearance.

It behaves like `CheckButton`, but defaults its `bootstyle` to `"Toolbutton"` and coerces styles to include
the `-toolbutton` variant. fileciteturn10file0

Use `CheckToggle` when you want checkbox semantics in compact UI areas like toolbars, headers, and mode strips.

---

## Overview

`CheckToggle` supports the same logical states as `CheckButton`:

- **checked** (`True`)
- **unchecked** (`False`)
- **indeterminate** (`None`)

It differs from `CheckButton` primarily in presentation: it uses the toolbutton variant style so it reads more like
a pressed/unpressed control than a checkbox indicator. fileciteturn10file0

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

`CheckToggle` is itself the “toggle” presentation of checkbox semantics.

If you want the classic indicator, use `CheckButton` instead.

---

## How the value works

The `value` option sets the initial state (defaults to `None` when unset). fileciteturn10file0

- `True` → checked
- `False` → unchecked
- `None` → indeterminate

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
- `style`, `bootstyle`, `surface_color`, `style_options` fileciteturn10file0

### `bootstyle` coercion

If `bootstyle` does not already include `"toolbutton"`, it is coerced to `"{bootstyle}-toolbutton"`. fileciteturn10file0

```python
ttk.CheckToggle(app, bootstyle="Toolbutton")         # explicit
ttk.CheckToggle(app, bootstyle="primary")            # coerced to "primary-toolbutton"
ttk.CheckToggle(app, bootstyle="success-toolbutton") # already toolbutton
```

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

Use semantic color tokens; they will be applied as toolbutton variants. fileciteturn10file0

```python
ttk.CheckToggle(app, bootstyle="primary")
ttk.CheckToggle(app, bootstyle="secondary")
ttk.CheckToggle(app, bootstyle="success")
ttk.CheckToggle(app, bootstyle="warning")
ttk.CheckToggle(app, bootstyle="danger")
```

---

## Localization

Text localization follows your standard widget localization behavior (`localize="auto"` where supported). fileciteturn10file0

---

## When should I use CheckToggle?

Use `CheckToggle` when:

- you want on/off selection with a **button-like** presentation
- the control lives in a toolbar or compact header area

Prefer **CheckButton** when:

- classic checkbox indicators are expected in forms and settings panels

---

## Related widgets

- **CheckButton** — classic checkbox indicator (multi-selection / tri-state)
- **RadioToggle** — mutually exclusive button-like radios
- **ButtonGroup** — visually grouped controls for toolbars and headers

---

## Reference

- **API Reference:** `ttkbootstrap.CheckToggle`
