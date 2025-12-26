# CheckButton

A control that toggles a boolean option on or off.

---

## Overview

CheckButtons allow users to turn options on or off, or represent a mixed (indeterminate) state when a choice is not fully applied.
Use `CheckButton` when the user is enabling or disabling features, or selecting multiple items independently.


## Basic usage

A `CheckButton` represents an on/off (or mixed) choice. You can control its **initial state**
using the `value` option.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.CheckButton(
    app,
    text="Enable notifications",
    value=True,
)
```

Set to unchecked by default:
```python
ttk.CheckButton(
    app,
    text="Send anonymous usage data",
    value=False,
)
```

Set to indeterminate (mixed) by default:
```python
ttk.CheckButton(
    app,
    text="Apply to all",
    value=None,
)
```

By default, `value=None`, which places the checkbutton in an **indeterminate** state.


---

## Styling checkbuttons

You can customize the checkbutton’s appearance by using **semantic color** and **variant** tokens.
Variants describe the control’s appearance and interaction style, not its meaning.

The supported variants for the checkbutton are default and toggle:

```python
ttk.Checkbutton(text="Option")
ttk.Checkbutton(text="Option", bootstyle="toggle")
```

**Color** and **variant** tokens can be combined to create the desired result (`color-variant`):

```python
ttk.Checkbutton(text="Option", bootstyle="primary")
ttk.Checkbutton(text="Option", bootstyle="success-toggle")
```

---

## Selected state

You can set the initial selected state using the associated signal:

```python
enable = ttk.Signal(True)
ttk.Checkbutton(text="Enable alerts", signal=enable)
```

Or change it at runtime:

```python
enable.set(True)   # selected
enable.set(False)  # unselected
```

Internally, the widget synchronizes this value with either:

- a reactive `signal=...` (recommended), or
- a Tkinter `variable=...`

Once bound, the signal or variable becomes the source of truth.

!!! note "Value precedence"
    The `value` option is used only to establish the initial state.
    After initialization, the bound signal or variable controls the widget state.
---

## Disabled state

The checkbutton can be disabled by setting the disabled state in the constructor:

```python
ttk.Checkbutton(text="Enable alerts", state="disabled")
```

Or at runtime:

```python
cb.configure(state="disabled")
```

You can also remove the disabled state:

```python
cb.configure(state="normal")
```

!!! tip "Shortcut"
    You can also use item assignment: `cb["state"] = "disabled"` or `"normal"`.

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, the `text` value is treated as a localization
key **when a matching translation exists**. If the key is not found in the active message catalog, the
widget falls back to using the value as **plain text**. You can override this behavior per widget if needed.

Use the global localization settings:

```python
ttk.Checkbutton(text="option.enable_alerts")
```

Enable localization explicitly:

```python
ttk.Checkbutton(text="option.enable_alerts", localize=True)
```

Disable localization explicitly (always treat the text as a literal):

```python
ttk.Checkbutton(text="Enable alerts", localize=False)
```

!!! tip "Literal text is safe"
    With `localize="auto"`, you can pass either a localization key or a literal label.
    If no translation is found, the label is shown as-is.

---

## Reactive text

You can bind the label text to a signal (so the checkbutton text updates automatically).

```python
import ttkbootstrap as ttk

app = ttk.App()

label = ttk.Signal("Enable alerts")

cb = ttk.Checkbutton(app, textsignal=label)
cb.pack(padx=20, pady=20)

label.set("Disable alerts")

app.mainloop()
```
