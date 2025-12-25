---
title: CheckButton
---

# CheckButton

`CheckButton` is a **selection control** that represents an option being **on**, **off**, or **mixed (indeterminate)**.

Use `CheckButton` when users can enable multiple options independently (settings, filters, feature flags). Use the
toggle variants (`CheckToggle`) when the control represents a single on/off feature and you want a stronger visual cue.

<figure markdown>
![checkbutton states](../../assets/dark/widgets-checkbutton-states.png#only-dark)
![checkbutton states](../../assets/light/widgets-checkbutton-states.png#only-light)
</figure>

---

## Framework integration

**Signals & Events**

- Many selection widgets can participate in **Signals** for reactive state sharing.
- Signals are built on **Tk variables**, but expose a modern subscription API (`subscribe()` / `unsubscribe()`).
- If the widget emits a virtual event (such as `<<Changed>>`), use it for Tk-level integration—not application state.

See:

- [Signals](../../capabilities/signals.md)
- [Virtual Events](../../capabilities/virtual-events.md)

**Design System**

- `bootstyle` controls semantic color and variant (checkbox vs toggle look, emphasis, and state styling).
- Disabled, pressed, hover, and focus visuals follow the theme’s state rules.

See:

- [Colors](../../design-system/colors.md)
- [Variants](../../design-system/variants.md)

**State & Interaction**

- Supports 2-state and 3-state behavior (indeterminate).
- Keyboard interaction and focus are consistent with other selection controls.

See:

- [State & Interaction](../../capabilities/state-and-interaction.md)

---

## Basic usage

Use `value` to set the initial state.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.CheckButton(app, text="Enable notifications", value=True).pack(padx=20, pady=6)
ttk.CheckButton(app, text="Send anonymous usage data", value=False).pack(padx=20, pady=6)

# Indeterminate (mixed) state
ttk.CheckButton(app, text="Apply to all", value=None).pack(padx=20, pady=6)

app.mainloop()
```

---

## Value model

`CheckButton` represents a boolean-like value:

- `True` → checked
- `False` → unchecked
- `None` → indeterminate (mixed)

Use indeterminate when a checkbox represents a *group state* (e.g., “Some items selected”).

<figure markdown>
![checkbutton indeterminate](../../assets/dark/widgets-checkbutton-indeterminate.png#only-dark)
![checkbutton indeterminate](../../assets/light/widgets-checkbutton-indeterminate.png#only-light)
</figure>

---

## Styling

Use `bootstyle` to control color emphasis.

```python
ttk.CheckButton(app, text="Primary", value=True, bootstyle="primary").pack()
ttk.CheckButton(app, text="Success", value=True, bootstyle="success").pack()
ttk.CheckButton(app, text="Danger", value=True, bootstyle="danger").pack()
```

<figure markdown>
![checkbutton colors](../../assets/dark/widgets-checkbutton-colors.png#only-dark)
![checkbutton colors](../../assets/light/widgets-checkbutton-colors.png#only-light)
</figure>

---

## Toggle style

If you want a toggle-style affordance (switch), use `CheckToggle`.

<figure markdown>
![checkbutton toggle](../../assets/dark/widgets-checkbutton-toggle.png#only-dark)
![checkbutton toggle](../../assets/light/widgets-checkbutton-toggle.png#only-light)
</figure>

---

## Events

For application logic, prefer **Signals** when available.

For Tk-level interoperability, you may use virtual events such as `<<Changed>>` (if exposed by the widget),
or bind to standard Tk events.

See:

- [Signals](../../capabilities/signals.md)
- [Virtual Events](../../capabilities/virtual-events.md)

---

## See also

**Related widgets**

- [CheckToggle](checktoggle.md) — toggle-style boolean
- [RadioButton](radiobutton.md) — mutually exclusive selection
- [ToggleGroup](togglegroup.md) — grouped selection buttons

**Framework concepts**

- [Signals](../../capabilities/signals.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)
- [Variants](../../design-system/variants.md)

**API reference**

- `ttkbootstrap.CheckButton` — [API Reference](../../reference/widgets/CheckButton.md)
