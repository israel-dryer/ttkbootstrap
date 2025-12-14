---
title: CheckButton
icon: fontawesome/solid/square-check
---

# CheckButton

CheckButtons allow users to turn options on or off, or represent a mixed (indeterminate) state when a choice is not fully applied.
Use `CheckButton` when the user is enabling or disabling features, or selecting multiple items independently.

---

## Basic usage

A `CheckButton` represents an on/off (or mixed) choice. You can control its **initial state**
using the `value` option.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Checked by default
ttk.CheckButton(
    app,
    text="Enable notifications",
    value=True,
).pack(padx=20, pady=6)

# Unchecked by default
ttk.CheckButton(
    app,
    text="Send anonymous usage data",
    value=False,
).pack(padx=20, pady=6)

# Indeterminate (mixed) by default
ttk.CheckButton(
    app,
    text="Apply to all",
    value=None,
).pack(padx=20, pady=6)

app.mainloop()
```

By default, `value=None`, which places the checkbutton in an **indeterminate** state.

---

## Variants

### Checkbutton (default)

Use when you have multiple independent selections.

<figure markdown>
![checkbutton](../../assets/dark/widgets-checkbutton-states.png#only-dark)
![checkbutton](../../assets/light/widgets-checkbutton-states.png#only-light)
</figure>

```python
ttk.CheckButton(app)
```

### Toggle (switch)

Use when the control represents a single on/off feature.

<figure markdown>
![toggle](../../assets/dark/widgets-checkbutton-toggle.png#only-dark)
![toggle](../../assets/light/widgets-checkbutton-toggle.png#only-light)
</figure>

```python
ttk.CheckButton(app, bootstyle="toggle")
```

---

## Label

You can provide a label to the checkbutton using the `text` option.

<figure markdown>
![labeled](../../assets/dark/widgets-checkbutton-labeled.png#only-dark)
![labeled](../../assets/light/widgets-checkbutton-labeled.png#only-light)
</figure>

```python
ttk.CheckButton(app, text="CheckButton")
ttk.CheckButton(app, text="Toggle", bootstyle="toggle")
```

---

## How the value works

`CheckButton` uses a single **logical value** to represent its state.

The `value` option sets the **initial state**:

- `True` → checked
- `False` → unchecked
- `None` → indeterminate (mixed)

```python
ttk.CheckButton(app, text="Auto-sync", value=True)
ttk.CheckButton(app, text="Enable logging", value=False)
ttk.CheckButton(app, text="Apply to all", value=None)
```

Internally, the widget synchronizes this value with either:

- a reactive `signal=...` (recommended), or
- a Tkinter `variable=...`

Once bound, the signal or variable becomes the source of truth.

!!! note "Value precedence"
    The `value` option is used only to establish the initial state.
    After initialization, the bound signal or variable controls the widget state.

---

## Binding to signals or variables

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

!!! note "Variable binding"
    You can also bind a Tkinter variable using the `variable` option, though signals
    are generally more powerful and easier to reason about in v2 applications.

---

## Tri-state (indeterminate) checkboxes

The indeterminate state (`value=None`) is useful when:

- a selection is partially applied
- a parent option represents mixed child values
- the user has not yet made an explicit choice

<figure markdown>
![indeterminate](../../assets/dark/widgets-checkbutton-indeterminate.png#only-dark)
![indeterminate](../../assets/light/widgets-checkbutton-indeterminate.png#only-light)
</figure>

```python
import ttkbootstrap as ttk

app = ttk.App()

cb = ttk.CheckButton(app, text="Partially selected", value=None)
cb.pack(padx=20, pady=10)

app.mainloop()
```

---

## Other common options

### `command` — run a callback when toggled

```python
import ttkbootstrap as ttk

app = ttk.App()

flag = ttk.BooleanVar(value=True)

def on_toggle():
    print("now:", flag.get())

ttk.CheckButton(
    app,
    text="Send notifications",
    variable=flag,
    command=on_toggle,
).pack(padx=20, pady=20)

app.mainloop()
```

### `state` — disable / enable

```python
cb = ttk.CheckButton(app, text="Locked", state="disabled")
cb.pack()

# later...
cb.configure(state="normal")
```

### `padding`, `width`, `underline`

```python
ttk.CheckButton(app, text="Wider", padding=(10, 6), width=18).pack(pady=6)
ttk.CheckButton(app, text="E_xport", underline=1).pack(pady=6)
```

---

## Colors

The `bootstyle` accepts color tokens that are typically combined with the button variant:

<figure markdown>
![colors](../../assets/dark/widgets-checkbutton-colors.png#only-dark)
![colors](../../assets/light/widgets-checkbutton-colors.png#only-light)
</figure>

```python
# standard checkbutton
ttk.CheckButton(app)  # primary is default
ttk.CheckButton(app, bootstyle="secondary")
ttk.CheckButton(app, bootstyle="success")
ttk.CheckButton(app, bootstyle="info")
ttk.CheckButton(app, bootstyle="warning")
ttk.CheckButton(app, bootstyle="danger")

# toggle
ttk.CheckButton(app, bootstyle="toggle")  # primary is default
ttk.CheckButton(app, bootstyle="secondary-toggle")
ttk.CheckButton(app, bootstyle="success-toggle")
ttk.CheckButton(app, bootstyle="info-toggle")
ttk.CheckButton(app, bootstyle="warning-toggle")
ttk.CheckButton(app, bootstyle="danger-toggle")
```

---

## Localization

If you use message catalogs, `localize="auto"` (or `True`) treats the `text` as a translation key.

```python
ttk.CheckButton(app, text="settings.notifications", localize="auto").pack()
```

---

## When should I use CheckButton?

Use `CheckButton` when:

- multiple selections can be on at once
- the value is on/off or mixed (indeterminate)

Use **RadioButton** when:

- only one choice is allowed in a group

---

## Related widgets

- **RadioButton** — choose one option from a group
- **Button** — trigger an action
- **Switch-style CheckButton** — `bootstyle="*-toggle"`
- **Form** — build many controls from a definition
