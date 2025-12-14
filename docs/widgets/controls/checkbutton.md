---
title: CheckButton
icon: fontawesome/solid/square-check
---

# CheckButton

`CheckButton` is a **boolean (or tri-state) control**. It wraps Tkinter’s `ttk.Checkbutton`, adding ttkbootstrap features like **Bootstyle tokens**, **theme-aware icons**, **signals**, and **surface-aware** styling.

Use `CheckButton` when the user is turning something **on/off** (or selecting multiple items independently).

---

<figure markdown>
![CheckButton states](../../assets/light/widgets-checkbutton.png#only-light)
![CheckButton states](../../assets/dark/widgets-checkbutton.png#only-dark)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

agree = ttk.BooleanVar(value=False)

ttk.CheckButton(
    app,
    text="I agree to the terms",
    variable=agree,
    bootstyle="primary",
).pack(padx=20, pady=20)

app.mainloop()
```

---

## How the value works

A `CheckButton` stores its state in a Tk variable.

- **Unchecked** → `offvalue`
- **Checked** → `onvalue`

```python
import ttkbootstrap as ttk

app = ttk.App()

v = ttk.StringVar(value="no")

cb = ttk.CheckButton(
    app,
    text="Enable feature",
    variable=v,
    onvalue="yes",
    offvalue="no",
)
cb.pack(padx=20, pady=20)

app.mainloop()
```

---

## Tri-state (indeterminate) checkboxes

Tk checkbuttons support a third “indeterminate” state (often used for “mixed selection” in tree views).

In ttk, this is represented by the **alternate** state, and ttkbootstrap styles include an indeterminate indicator image. (Your builder maps the `alternate !selected` state.)  

```python
import ttkbootstrap as ttk

app = ttk.App()

v = ttk.StringVar(value="mixed")

cb = ttk.CheckButton(app, text="Partially selected", variable=v,
                     onvalue="on", offvalue="off")
cb.pack(padx=20, pady=10)

# show indeterminate
cb.state(["alternate"])
cb.state(["!selected"])  # common: alternate + not selected

app.mainloop()
```

> _Image placeholder:_  
> `![Indeterminate CheckButton](../_img/widgets/checkbutton/indeterminate.png)`

---

## `command` and common options

### Run logic when toggled

```python
import ttkbootstrap as ttk

app = ttk.App()

flag = ttk.BooleanVar(value=True)

def on_toggle():
    print("now:", flag.get())

ttk.CheckButton(app, text="Send notifications", variable=flag, command=on_toggle).pack(padx=20, pady=20)

app.mainloop()
```

### Disable / enable

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

## Bootstyle and variants

### Standard checkbox styles

Use intent colors like `primary`, `success`, `warning`, `danger`, etc.

```python
import ttkbootstrap as ttk

app = ttk.App()

for style in ["primary", "success", "warning", "danger"]:
    ttk.CheckButton(app, text=style.title(), bootstyle=style).pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

### Toggle (switch) style

ttkbootstrap also supports a **toggle / switch** presentation for checkbuttons (registered as the `toggle` variant in the style builder).

```python
import ttkbootstrap as ttk

app = ttk.App()

dark = ttk.BooleanVar(value=False)

ttk.CheckButton(
    app,
    text="Dark mode",
    variable=dark,
    bootstyle="primary-toggle",
).pack(padx=20, pady=20)

app.mainloop()
```

> _Image placeholder:_  
> `![Toggle CheckButton](../_img/widgets/checkbutton/toggle.png)`

---

## Icons

`CheckButton` supports:

- `icon=...` (theme-aware, preferred)
- `image=...` (raw Tk image)

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.CheckButton(
    app,
    text="Remember me",
    bootstyle="secondary",
    icon="bookmark",  # placeholder for your icon spec/provider
).pack(padx=20, pady=20)

app.mainloop()
```

If you need an icon-only checkbox in a toolbar-like scenario, you can combine `icon_only=True` with an icon spec (supported as a captured style option).

---

## Signals and localization

### Signals

`CheckButton` supports a reactive `signal=...` binding (auto-synced with the underlying Tk `variable`).

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
enabled = ttk.Signal(False)  # pseudo-code

cb = ttk.CheckButton(app, text="Enabled", signal=enabled)
cb.pack(padx=20, pady=20)

enabled.set(True)

app.mainloop()
```

### Localization

If you use message catalogs, `localize="auto"` (or `True`) treats the `text` as a translation key.

```python
ttk.CheckButton(app, text="settings.notifications", localize="auto").pack()
```

---

## When should I use CheckButton?

Use `CheckButton` when:

- multiple selections can be on at once
- the value is on/off (or mixed/indeterminate)

Use **RadioButton** when:

- only one choice is allowed in a group

---

## Related widgets

- **RadioButton** — choose one option from a group
- **Button** — trigger an action
- **Switch-style CheckButton** — `bootstyle="*-toggle"`
- **Form** — build many controls from a definition
