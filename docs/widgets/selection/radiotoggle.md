---
title: RadioToggle
---

# RadioToggle

`RadioToggle` is a `RadioButton` variant that renders with a **toggle badge** style.

Use `RadioToggle` when you want mutually exclusive choices, but prefer a more "button-like" presentation
than the classic radio indicator (common in toolbars, view switches, or mode pickers).

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

view = ttk.Signal("grid")

ttk.RadioToggle(app, text="Grid", signal=view, value="grid").pack(side="left", padx=4, pady=10)
ttk.RadioToggle(app, text="List", signal=view, value="list").pack(side="left", padx=4, pady=10)

app.mainloop()
```

---

## When to use

Use `RadioToggle` when:

- you want single selection

- the control is part of a compact UI (toolbar, header controls)

- a button-like appearance is more discoverable than a radio indicator

### Consider a different control when...

- classic form-style radio indicators are expected — use **RadioButton**

- the control appears in a traditional settings form — use **RadioButton**

---

## Appearance

`RadioToggle` behaves like `RadioButton`:

- it participates in a mutually exclusive group via a shared `signal` or `variable`

- selecting it sets the shared value to its `value`

The difference is purely presentational: `RadioToggle` coerces `bootstyle` to a toolbutton-style badge
(e.g. `primary-toolbutton`, `success-toolbutton`).

### Variants

#### Bootstyle coercion

`RadioToggle` defaults `bootstyle` to `"Toolbutton"`, and ensures it includes `"-toolbutton"`.

```python
ttk.RadioToggle(app)
ttk.RadioToggle(app, bootstyle="success")
```

### Colors and styling

Use semantic color tokens; they are coerced to the toolbutton variant automatically.

```python
ttk.RadioToggle(app, bootstyle="primary")
ttk.RadioToggle(app, bootstyle="secondary")
ttk.RadioToggle(app, bootstyle="success")
```

!!! link "Design System"
    See [Design System](../../concepts/design-system.md) for color tokens, theming, and styling guidelines.

---

## Examples and patterns

### How the value works

Same as `RadioButton`:

- `value` is the option represented by this toggle

- the shared signal/variable holds the selected value

- selection is committed on click (or keyboard select)

### Binding to signals or variables

Bind a shared `signal` (preferred) or `variable` just like a radio button.

```python
mode = ttk.Signal("basic")
ttk.RadioToggle(app, text="Basic", signal=mode, value="basic")
ttk.RadioToggle(app, text="Pro", signal=mode, value="pro")
```

### Common options

`RadioToggle` supports the same constructor options as `RadioButton` (text, icon, command, state, etc.).

### Events

Use `command=` for a per-toggle callback, or subscribe to the shared signal for group-level changes.

### Validation and constraints

Same as `RadioButton`: selection is constrained to the values represented by the group.

---

## Behavior

- Mutually exclusive selection through shared state

- Visual emphasis matches toolbutton/badge styling

- Typically used in compact areas like toolbars

---

## Localization

`RadioToggle` text follows the same localization behavior as other widgets that support `text` / `textvariable`.

!!! link "Localization"
    See [Localization](../../concepts/localization.md) for details on internationalizing widget text.

---

## Reactivity

Bind a shared `signal` (preferred) or `variable` to enable reactive updates across the toggle group.

!!! link "Signals"
    See [Signals](../../concepts/signals.md) for reactive programming patterns and state management.

---

## Additional resources

### Related widgets

- [RadioButton](radiobutton.md) — classic radio indicator
- [RadioGroup](radiogroup.md) — composite group builder
- [ToggleGroup](togglegroup.md) — grouped button-style selection patterns

### Framework concepts

- [Design System](../../concepts/design-system.md) — color tokens and theming
- [Signals](../../concepts/signals.md) — reactive state management
- [Localization](../../concepts/localization.md) — internationalizing widget text

### API reference

- [`ttkbootstrap.RadioToggle`](../../reference/widgets/RadioToggle.md)