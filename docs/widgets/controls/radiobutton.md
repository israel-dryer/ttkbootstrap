---
title: RadioButton
icon: fontawesome/solid/circle-dot
---

# RadioButton

`RadioButton` lets the user choose **one option from a group**.

It wraps Tkinter’s `ttk.Radiobutton`, keeping the familiar API while adding ttkbootstrap features like:

- **Bootstyle tokens** (`bootstyle="primary"`, `bootstyle="success"`, etc.)
- **Theme-aware icons** via `icon=...`
- Optional **signals** for reactive apps (`signal=...`)
- **Surface-aware** styling (`surface_color=...`)

> _Image placeholder:_  
> `![RadioButton group](../_img/widgets/radiobutton/overview.png)`  
> Suggested shot: 3-option group + disabled option + different bootstyles.

---

## Basic usage

A radio group is defined by a **shared variable** and different `value=` settings for each button.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="medium")

ttk.RadioButton(app, text="Low", variable=choice, value="low").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Medium", variable=choice, value="medium").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="High", variable=choice, value="high").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

---

## Reading and setting the value

```python
print(choice.get())
choice.set("high")
```

You can also set the selected option by updating the variable.

---

## `command` callback

`command=` is called when the selection changes.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="low")

def on_change():
    print("selected:", choice.get())

ttk.RadioButton(app, text="Low", variable=choice, value="low", command=on_change).pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="High", variable=choice, value="high", command=on_change).pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

---

## Bootstyle

Use intent colors to match your app’s design system.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="a")

for style in ["primary", "success", "warning", "danger", "info"]:
    ttk.RadioButton(
        app,
        text=style.title(),
        variable=choice,
        value=style[0],
        bootstyle=style,
    ).pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

> _Image placeholder:_  
> `![RadioButton bootstyles](../_img/widgets/radiobutton/bootstyles.png)`

---

## Disabled options

Disable individual choices when they are not available.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="basic")

ttk.RadioButton(app, text="Basic", variable=choice, value="basic").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Pro (unavailable)", variable=choice, value="pro", state="disabled").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

---

## Layout patterns

### Inline (row of choices)

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="left")

row = ttk.Frame(app, padding=20)
row.pack(fill="x")

ttk.RadioButton(row, text="Left", variable=choice, value="left").pack(side="left", padx=(0, 10))
ttk.RadioButton(row, text="Center", variable=choice, value="center").pack(side="left", padx=(0, 10))
ttk.RadioButton(row, text="Right", variable=choice, value="right").pack(side="left")

app.mainloop()
```

### Group label (common desktop pattern)

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="email")

box = ttk.LabelFrame(app, text="Notifications", padding=20)
box.pack(fill="x", padx=20, pady=20)

ttk.RadioButton(box, text="Email", variable=choice, value="email").pack(anchor="w", pady=2)
ttk.RadioButton(box, text="SMS", variable=choice, value="sms").pack(anchor="w", pady=2)
ttk.RadioButton(box, text="None", variable=choice, value="none").pack(anchor="w", pady=2)

app.mainloop()
```

---

## Icons

`RadioButton` supports:

- `icon=...` (theme-aware, preferred)
- `image=...` (raw Tk image)

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="list")

ttk.RadioButton(app, text="List view", variable=choice, value="list", icon="list").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Grid view", variable=choice, value="grid", icon="border-all").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

> _Image placeholder:_  
> `![RadioButton icons](../_img/widgets/radiobutton/icons.png)`

---

## Signals and localization

### Signals

Bind the selection to a signal (reactive apps).

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
mode = ttk.Signal("basic")  # pseudo-code

ttk.RadioButton(app, text="Basic", signal=mode, value="basic").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Advanced", signal=mode, value="advanced").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

### Localization

If you use message catalogs, `localize="auto"` treats the `text` as a translation key.

```python
ttk.RadioButton(app, text="settings.mode.basic", localize="auto").pack()
```

---

## Surface-aware styling

If your UI uses inherited surfaces (elevated panels), you can pin the radiobuttons to a specific surface token.

```python
import ttkbootstrap as ttk

app = ttk.App()

panel = ttk.Frame(app, padding=20, bootstyle="background")
panel.pack(fill="both", expand=True)

choice = ttk.StringVar(value="a")

ttk.RadioButton(panel, text="Option A", variable=choice, value="a", surface_color="background[+1]").pack(anchor="w")
ttk.RadioButton(panel, text="Option B", variable=choice, value="b", surface_color="background[+1]").pack(anchor="w")

app.mainloop()
```

---

## When should I use RadioButton?

Use `RadioButton` when:

- there must be **exactly one** selection
- the choices are short and visible

Prefer `SelectBox` / `OptionMenu` when:

- the list is long
- screen space is limited
- you want search/filter behavior

---

## Related widgets

- **CheckButton** — multiple independent selections (on/off)
- **SelectBox** — dropdown selection, optional search
- **OptionMenu** — simple menu-based selection
- **Button** — trigger an action
