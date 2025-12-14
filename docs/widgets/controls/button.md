---
title: Button
icon: fontawesome/solid/hand-pointer
---

# Button

`Button` triggers an action when clicked.

In ttkbootstrap v2, `Button` is a wrapper around Tkinter’s `ttk.Button` that keeps the familiar API but adds a few
“app-ready” conveniences:

- **Bootstyle tokens** (`bootstyle="primary-outline"`, `bootstyle="danger"`, etc.)
- **Theme-aware icons** via `icon=...` (preferred over raw `image=...`)
- Optional **reactive text binding** with `textsignal=...`
- **Surface-aware** styling via `surface_color=...` (or inherit from the parent surface)

---
<figure markdown>
![Button variants](../../assets/dark/widgets-button.png#only-dark)  
![Button variants](../../assets/light/widgets-button.png#only-light)
</figure>
!!! note "Ghost and Link are displayed above in _active_ state. Normal state appears same as text."

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()


def on_save():
    print("Saved!")


ttk.Button(app, text="Save", bootstyle="primary", command=on_save).pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

### `text` and `command`

```python
ttk.Button(app, text="Run", command=lambda: print("run")).pack()
```

### `state`

Disable a button until the user has completed a step.

```python
btn = ttk.Button(app, text="Continue", bootstyle="primary", state="disabled")
btn.pack()

# later…
btn.configure(state="normal")
```

### `padding`, `width`, and `underline`

```python
ttk.Button(app, text="Wide", width=18, padding=(12, 6)).pack(pady=6)
ttk.Button(app, text="E_xit", underline=1).pack(pady=6)  # Alt+X mnemonic on some platforms
```

---

## Bootstyle variants

Buttons are typically styled with a **color token** and an optional **variant**.

```python
ttk.Button(app, text="Primary", bootstyle="primary").pack(pady=4)
ttk.Button(app, text="Outline", bootstyle="primary-outline").pack(pady=4)
ttk.Button(app, text="Ghost", bootstyle="primary-ghost").pack(pady=4)
ttk.Button(app, text="Link", bootstyle="primary-link").pack(pady=4)
ttk.Button(app, text="Text", bootstyle="text").pack(pady=4)
```

---

## Icons

### Theme-aware icon (recommended)

Use `icon=...` so the icon can respond to hover/disabled state and theme changes.

```python
ttk.Button(
    app,
    text="Download",
    bootstyle="primary",
    icon="download",  # placeholder: your icon spec / provider name
).pack(pady=6)
```

> _Image placeholder:_  
> `![Button with icon](../_img/widgets/button/icon-text.png)`

### Icon-only buttons

Use `icon_only=True` for compact toolbar buttons.

```python
ttk.Button(
    app,
    bootstyle="secondary",
    icon="gear",  # placeholder
    icon_only=True,
).pack(pady=6)
```

> _Image placeholder:_  
> `![Icon-only toolbar buttons](../_img/widgets/button/icon-only.png)`

!!! warning "Using `image=...`"
You can still pass a Tk `PhotoImage` via `image=...`, but it won’t automatically recolor for theme changes.

---

## Surface-aware backgrounds

If your app uses inherited surfaces (elevated frames), you can pin the button to a specific surface token.

```python
panel = ttk.Frame(app, padding=20, bootstyle="background")  # example surface
panel.pack(fill="both", expand=True)

ttk.Button(
    panel,
    text="Action",
    bootstyle="primary-outline",
    surface_color="background[+1]",
).pack()
```

---

## Reactive text with `textsignal`

If your v2 app uses signals, you can bind the label text to a signal (so the button text updates automatically).

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
label = ttk.Signal("Start")  # pseudo-code

btn = ttk.Button(app, bootstyle="primary", textsignal=label)
btn.pack(padx=20, pady=20)

# later…
label.set("Stop")

app.mainloop()
```

---

## Localization

If you use message catalogs, `localize="auto"` (or `True`) allows a label to be treated as a localization key.

```python
ttk.Button(app, text="button.ok", localize="auto", bootstyle="primary").pack()
```

---

## Patterns

### Primary + secondary actions

```python
row = ttk.Frame(app, padding=20)
row.pack(fill="x")

ttk.Button(row, text="Cancel", bootstyle="secondary").pack(side="right", padx=(8, 0))
ttk.Button(row, text="Save", bootstyle="primary").pack(side="right")
```

### Destructive actions

```python
ttk.Button(app, text="Delete", bootstyle="danger").pack(pady=6)
ttk.Button(app, text="Delete", bootstyle="danger-outline").pack(pady=6)
```

---

## Related widgets

- **CheckButton** — boolean toggle (on/off)
- **RadioButton** — single selection in a group
- **MenuButton** / **DropdownButton** — button that opens a menu
- **Dialog** / **MessageDialog** — action buttons inside modal flows
