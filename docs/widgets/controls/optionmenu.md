---
title: OptionMenu
icon: fontawesome/solid/square-caret-down
---

# OptionMenu

`OptionMenu` lets users pick one value from a list.

In ttkbootstrap v2, `OptionMenu` wraps Tkinter's `ttk.Menubutton` to create a simple dropdown control. It adds:

- **Bootstyle tokens** (`bootstyle="primary"`, `bootstyle="outline"`, etc.)
- **Theme-aware icons** via `icon=...`
- Optional **reactive binding** with `textsignal=...`
- **Surface-aware** styling via `surface_color=...`
- Built-in **`<<Changed>>` events** with `on_changed(...)`

Use `OptionMenu` when the list is short (3–15 items) and users know the available choices. For longer lists with search/filter, prefer **SelectBox**.

> _Image placeholder:_
> `![OptionMenu states](../_img/widgets/optionmenu/overview.png)`
> Suggested shot: collapsed + open menu + disabled + selected item highlighted.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.StringVar(value="Medium")

menu = ttk.OptionMenu(
    app,
    value="Medium",
    options=["Low", "Medium", "High"],
    bootstyle="primary",
)
menu.pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

### Initial value and options list

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.OptionMenu(
    app,
    value="Red",
    options=["Red", "Green", "Blue"],
)
menu.pack(padx=20, pady=10)

app.mainloop()
```

### Using a variable

You can provide a `textvariable` to sync with other widgets or app state.

```python
import ttkbootstrap as ttk

app = ttk.App()

color = ttk.StringVar(value="Green")

menu = ttk.OptionMenu(
    app,
    textvariable=color,
    options=["Red", "Green", "Blue"],
)
menu.pack(padx=20, pady=10)

print("selected:", color.get())

app.mainloop()
```

### `state`

Disable the menu when selection shouldn't be changed.

```python
menu = ttk.OptionMenu(app, value="Locked", options=["A", "B"], state="disabled")
menu.pack()

# later…
menu.configure(state="normal")
```

### `width` and `padding`

```python
ttk.OptionMenu(app, value="A", options=["A", "B"], width=20, padding=(10, 6)).pack(pady=6)
```

---

## Getting and setting the value

### `.value` property

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.OptionMenu(app, value="Medium", options=["Low", "Medium", "High"])
menu.pack(padx=20, pady=10)

print("current:", menu.value)

# Change the value
menu.value = "High"

app.mainloop()
```

### Using `configure(value=...)`

```python
menu.configure(value="Low")
```

---

## Updating the options list

Use `configure(options=...)` to change the available choices.

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.OptionMenu(app, value="Apple", options=["Apple", "Banana"])
menu.pack(padx=20, pady=10)

def add_more():
    menu.configure(options=["Apple", "Banana", "Cherry", "Date"])

ttk.Button(app, text="Add more fruits", command=add_more).pack(pady=10)

app.mainloop()
```

---

## Bootstyle variants

`OptionMenu` accepts the same bootstyle variants as `MenuButton`.

### Solid (default)

```python
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="primary").pack(pady=4)
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="success").pack(pady=4)
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="danger").pack(pady=4)
```

### Outline

```python
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="primary-outline").pack(pady=4)
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="secondary-outline").pack(pady=4)
```

### Ghost

```python
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="primary-ghost").pack(pady=4)
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="info-ghost").pack(pady=4)
```

### Text

```python
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="text").pack(pady=4)
```

> _Image placeholder:_
> `![OptionMenu bootstyles](../_img/widgets/optionmenu/bootstyles.png)`
> (Show solid / outline / ghost / text variants.)

---

## Icons

### Theme-aware icon (recommended)

Use `icon=...` for an icon that responds to the current theme.

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.OptionMenu(
    app,
    value="Dark",
    options=["Light", "Dark", "Auto"],
    icon="palette",  # placeholder: your icon spec / provider name
    bootstyle="primary",
)
menu.pack(padx=20, pady=10)

app.mainloop()
```

> _Image placeholder:_
> `![OptionMenu with icon](../_img/widgets/optionmenu/icon.png)`

!!! warning "Using `image=...`"
    You can still pass a Tk `PhotoImage` via `image=...`, but it won't automatically recolor for theme changes.

---

## Dropdown indicator

By default, `OptionMenu` shows a dropdown chevron on the right. You can hide it or customize the icon.

### Hide the dropdown button

```python
ttk.OptionMenu(
    app,
    value="A",
    options=["A", "B", "C"],
    show_dropdown_button=False,
).pack(pady=6)
```

### Custom dropdown icon

```python
ttk.OptionMenu(
    app,
    value="A",
    options=["A", "B", "C"],
    dropdown_button_icon="chevron-down",  # placeholder: your icon name
).pack(pady=6)
```

---

## Events

### `on_changed(...)` and `off_changed(...)`

`OptionMenu` emits a `<<Changed>>` event when the user selects a new value. Use `on_changed(...)` to bind a callback.

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.OptionMenu(app, value="Medium", options=["Low", "Medium", "High"])
menu.pack(padx=20, pady=10)

def handle_change(event):
    print("Selected:", event.data["value"])

menu.on_changed(handle_change)

app.mainloop()
```

To unbind:

```python
bind_id = menu.on_changed(handle_change)
menu.off_changed(bind_id)
```

---

## Signals

If your app uses signals, you can bind the text to a `textsignal=` so changes flow through your app state.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
selected = ttk.Signal("Medium")  # pseudo-code

menu = ttk.OptionMenu(
    app,
    textsignal=selected,
    options=["Low", "Medium", "High"],
)
menu.pack(padx=20, pady=10)

selected.subscribe(lambda v: print("value changed:", v))

app.mainloop()
```

---

## When should I use OptionMenu?

Use `OptionMenu` when:

- the list is short (3–15 items)
- the dropdown is purely value selection
- you want a classic, compact desktop control

Prefer **SelectBox** when:

- the list is long (more than 15 items)
- users need search/filter
- you want richer presentation (icons, descriptions, grouping)

Prefer **RadioButton** when:

- there are only 2–4 options and showing them inline improves clarity

---

## Related widgets

- **SelectBox** — dropdown picker with search and filtering
- **DropdownButton** — button that opens an action menu (not a persistent selection)
- **RadioButton** — small enumerations displayed inline
- **MenuButton** — the base widget for custom menu-triggered buttons