---
title: CheckButton
---

# CheckButton

`CheckButton` is a **selection control** that represents an option being **on**, **off**, or **mixed (indeterminate)**.

Use `CheckButton` when users can enable multiple options independently (settings, filters, feature flags).

<figure markdown>
![checkbutton](../../assets/dark/widgets-checkbutton-states.png#only-dark)
![checkbutton](../../assets/light/widgets-checkbutton-states.png#only-light)
</figure>

---

## Quick start

Use `value` to set the initial state.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.CheckButton(app, text="Enable notifications", value=True).pack(padx=20, pady=6)
ttk.CheckButton(app, text="Send anonymous usage data", value=False).pack(padx=20, pady=6)
ttk.CheckButton(app, text="Apply to all", value=None).pack(padx=20, pady=6)

app.mainloop()
```

By default, `value=None`, which places the checkbutton in an **indeterminate** state.

---

## When to use

Use `CheckButton` when:

- multiple selections may be enabled at once
- the value is on/off or mixed
- you need independent option toggles

### Consider a different control when...

- only one choice is allowed in a group -> use [RadioButton](radiobutton.md)
- you want a dropdown list -> use [SelectBox](selectbox.md) or [OptionMenu](optionmenu.md)
- you want a button-like toggle -> use [CheckToggle](checktoggle.md)
- you want a dedicated on/off switch -> use [Switch](switch.md)

---

## Appearance

<figure markdown>
![checkbutton](../../assets/dark/widgets-checkbutton-states.png#only-dark)
![checkbutton](../../assets/light/widgets-checkbutton-states.png#only-light)
</figure>

### Colors and styling

Use semantic color tokens with `color`.

```python
ttk.CheckButton(app)
ttk.CheckButton(app, color="secondary")
ttk.CheckButton(app, color="success")
ttk.CheckButton(app, color="warning")
ttk.CheckButton(app, color="danger")
```

<figure markdown>
![colors](../../assets/dark/widgets-checkbutton-colors.png#only-dark)
![colors](../../assets/light/widgets-checkbutton-colors.png#only-light)
</figure>

!!! link "See [Design System - Variants](../../design-system/variants.md) for how color tokens apply consistently across widgets."

---

## Examples & patterns

### How the value works

`CheckButton` uses a single logical value.

The `value` option sets the **initial state**:

- `True` -> checked
- `False` -> unchecked
- `None` -> indeterminate

Once bound, the signal or variable becomes the source of truth.

!!! note "Value precedence"
    The `value` option is only used during initialization.
    After creation, the bound signal or variable controls the widget state.

### Common options

#### `text`

Label shown next to the indicator.

```python
ttk.CheckButton(app, text="Auto-sync")
```

#### `command`

Run a callback when the value toggles.

```python
flag = ttk.BooleanVar(value=True)

def on_toggle():
    print("now:", flag.get())

ttk.CheckButton(app, text="Send notifications", variable=flag, command=on_toggle).pack(padx=20, pady=20)
```

#### `state`

Disable or enable the widget.

```python
cb = ttk.CheckButton(app, text="Locked", state="disabled")
cb.pack()

cb.configure(state="normal")
```

#### `padding`, `width`, `underline`

```python
ttk.CheckButton(app, text="Wider", padding=(10, 6), width=18).pack(pady=6)
ttk.CheckButton(app, text="E_xport", underline=1).pack(pady=6)
```

### Events

`CheckButton` emits selection change events consistent with other selection widgets.

```python
def on_changed(e):
    print("value:", cb.value)

cb.on_changed(on_changed)
```

Most commonly used:

- `<<Changed>>` - fired when the committed value changes

### Validation and constraints

Validation is usually minimal for `CheckButton`.

Use validation when:

- the option is required to proceed
- the indeterminate state must be resolved before submission
- the selection participates in cross-field rules

---

## Behavior

- Click toggles between checked/unchecked.
- Indeterminate behavior depends on your app logic (commonly used for "mixed" parent selections).
- Keyboard navigation follows standard ttk checkbutton behavior (focus + Space to toggle).

---

## Localization

By default, widgets use `localize="auto"`:

- if a translation key exists, it is used
- otherwise, the label is treated as a literal string

```python
ttk.CheckButton(app, text="settings.notifications")
ttk.CheckButton(app, text="settings.notifications", localize=True)
ttk.CheckButton(app, text="Notifications", localize=False)
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, passing literal text is safe when no translation exists.

!!! link "See [Localization](../../capabilities/localization.md) for configuring translations and message catalogs."

---

## Reactivity

Prefer a reactive `signal=...` in v2 apps:

```python
import ttkbootstrap as ttk

app = ttk.App()

v = ttk.Signal("no")

cb = ttk.CheckButton(
    app,
    text="Enable feature",
    signal=v,
    onvalue="yes",
    offvalue="no",
)
cb.pack(padx=20, pady=20)

app.mainloop()
```

You can also bind a Tk variable with `variable=...`.

!!! link "See [Signals](../../capabilities/signals.md) for reactive programming patterns."

---

## Additional resources

### Related widgets

- [Switch](switch.md) - dedicated on/off switch control
- [RadioButton](radiobutton.md) - choose one option from a group
- [RadioGroup](radiogroup.md) - manage a group of radio options as one control
- [CheckToggle](checktoggle.md) - button-like toggle presentation
- [SelectBox](selectbox.md) - select one item from a list
- [Form](../forms/form.md) - build grouped selection controls declaratively

### Framework concepts

- [Signals](../../capabilities/signals.md) - reactive state management
- [Localization](../../capabilities/localization.md) - text translation
- [Design System](../../design-system/variants.md) - color tokens and variants

### API reference

- [`ttkbootstrap.CheckButton`](../../reference/widgets/CheckButton.md)