---
title: RadioButton
icon: fontawesome/solid/circle-dot
---

# RadioButton

RadioButtons allow users to select **exactly one option from a group**.
Use `RadioButton` when a choice is mutually exclusive and all options should be visible at once.

<figure markdown>
![radiobutton states](../../assets/dark/widgets-radiobutton-states.png#only-dark)
![radiobutton states](../../assets/light/widgets-radiobutton-states.png#only-light)
</figure>

---

## Basic usage

A radio group is defined by a **shared value** and a distinct `value=` for each option.
In ttkbootstrap v2, this shared value is typically managed using a **signal**.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.Signal("medium")

ttk.RadioButton(app, text="Low", signal=choice, value="low").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Medium", signal=choice, value="medium").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="High", signal=choice, value="high").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

The option whose `value` matches the shared signal is selected.

---

## How the value works

`RadioButton` uses a **single shared value** to represent the selected option.

- Each `RadioButton` defines a distinct `value`
- The selected button is the one whose `value` matches the shared signal or variable

```python
choice = ttk.Signal("low")

ttk.RadioButton(app, text="Low", signal=choice, value="low")
ttk.RadioButton(app, text="High", signal=choice, value="high")
```

Updating the signal changes the selected option:

```python
choice.set("high")
```

!!! note "Single source of truth"
    The shared signal or variable is the source of truth.
    Individual RadioButtons do not store state independently.

---

## Using Tkinter variables

You can also bind a Tkinter variable instead of a signal.
This is fully supported, though signals are generally preferred in v2 applications.

```python
choice = ttk.StringVar(value="medium")

ttk.RadioButton(app, text="Low", variable=choice, value="low")
ttk.RadioButton(app, text="Medium", variable=choice, value="medium")
ttk.RadioButton(app, text="High", variable=choice, value="high")

```

---

## Colors

RadioButtons support standard ttkbootstrap styling and theming.

<figure markdown>
![colors](../../assets/dark/widgets-radiobutton-colors.png#only-dark)
![colors](../../assets/light/widgets-radiobutton-colors.png#only-light)
</figure>

```python
ttk.RadioButton(app)  # primary is default
ttk.RadioButton(app, bootstyle="secondary")
ttk.RadioButton(app, bootstyle="success")
ttk.RadioButton(app, bootstyle="info")
ttk.RadioButton(app, bootstyle="warning")
ttk.RadioButton(app, bootstyle="danger")
```

---

## Command callback

Use `command=` to react when the selection changes.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.Signal("low")

def on_change():
    print("selected:", choice.get())

ttk.RadioButton(app, text="Low", signal=choice, value="low", command=on_change).pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="High", signal=choice, value="high", command=on_change).pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

---

## Disabled options

Disable individual options when they are not available.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.Signal("basic")

ttk.RadioButton(app, text="Basic", signal=choice, value="basic").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Pro (unavailable)", signal=choice, value="pro", state="disabled").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, the `text` is treated as a localization key **when a translation exists**.
If the key is not found in the active message catalog, the widget falls back to using the value as **plain text**.

You can override this behavior per widget if needed.

```python
# uses global app localization settings (default)
ttk.RadioButton(app, text="settings.mode.basic").pack()

# explicitly enable localization
ttk.RadioButton(app, text="settings.mode.basic", localize=True).pack()

# explicitly disable localization (always treat text as a literal)
ttk.RadioButton(app, text="Basic", localize=False).pack()
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, you can pass either a localization key or a literal label.
    If no translation is found, the label is shown as-is.

---

## When should I use RadioButton?

Use `RadioButton` when:

- exactly **one option must be selected**
- all options are short and visible

Prefer **CheckButton** when:

- multiple selections are allowed

Prefer **SelectBox / OptionMenu** when:

- the list is long
- screen space is limited
- search or filtering is needed

---

## Related widgets

- **CheckButton** — multiple independent selections (on/off or mixed)
- **SelectBox** — dropdown selection, optional search
- **OptionMenu** — simple menu-based selection
- **Button** — trigger an action
