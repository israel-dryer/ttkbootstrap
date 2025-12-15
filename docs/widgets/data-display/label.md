---
title: Label
icon: fontawesome/solid/tag
---

# Label

`Label` displays text or images.

In ttkbootstrap v2, `Label` is a wrapper around Tkinter's `ttk.Label` that keeps the familiar API but adds a few "app-ready" conveniences:

- **Bootstyle tokens** (`bootstyle="secondary"`, `bootstyle="info"`, etc.)
- **Theme-aware icons** via `icon=...` (preferred over raw `image=...`)
- Optional **reactive text binding** with `textsignal=...`
- **Surface-aware** styling via `surface_color=...` (or inherit from the parent surface)
- **Localization** support with `localize=...`

> _Image placeholder:_
> `![Label variants](../_img/widgets/label/overview.png)`
> Suggested shot: labels with different bootstyles, icons, and text variations.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Welcome to ttkbootstrap!").pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

### `text` and `textvariable`

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Status: Ready").pack(pady=4)

status = ttk.StringVar(value="Connected")
ttk.Label(app, textvariable=status).pack(pady=4)

app.mainloop()
```

### `anchor` and `justify`

Control how text is positioned within the label.

```python
ttk.Label(app, text="Left aligned", anchor="w", width=20).pack(fill="x", pady=4)
ttk.Label(app, text="Center aligned", anchor="center", width=20).pack(fill="x", pady=4)
ttk.Label(app, text="Right aligned", anchor="e", width=20).pack(fill="x", pady=4)
```

For multi-line text, use `justify`:

```python
ttk.Label(
    app,
    text="This is a long\nmulti-line label\nwith centered text",
    justify="center",
).pack(pady=10)
```

### `wraplength`

Automatically wrap text to fit within a specific width (in pixels).

```python
ttk.Label(
    app,
    text="This is a very long label that will wrap automatically when it exceeds the specified width.",
    wraplength=200,
).pack(padx=20, pady=10)
```

### `padding`

Add space around the label content.

```python
ttk.Label(app, text="Padded label", padding=(20, 10)).pack()
```

### `font`

Specify a custom font.

```python
ttk.Label(app, text="Large Text", font=("Helvetica", 18, "bold")).pack(pady=10)
```

---

## Bootstyle variants

Use bootstyle color tokens to change the label's text color for semantic meaning.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Default label").pack(anchor="w", padx=20, pady=2)
ttk.Label(app, text="Primary", bootstyle="primary").pack(anchor="w", padx=20, pady=2)
ttk.Label(app, text="Secondary", bootstyle="secondary").pack(anchor="w", padx=20, pady=2)
ttk.Label(app, text="Success", bootstyle="success").pack(anchor="w", padx=20, pady=2)
ttk.Label(app, text="Info", bootstyle="info").pack(anchor="w", padx=20, pady=2)
ttk.Label(app, text="Warning", bootstyle="warning").pack(anchor="w", padx=20, pady=2)
ttk.Label(app, text="Danger", bootstyle="danger").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

> _Image placeholder:_
> `![Label bootstyles](../_img/widgets/label/bootstyles.png)`
> (Show labels in all color variants.)

---

## Icons

### Theme-aware icon (recommended)

Use `icon=...` so the icon can respond to the current theme and widget state.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(
    app,
    text="Success!",
    icon="check-circle",  # placeholder: your icon spec / provider name
    compound="left",
    bootstyle="success",
).pack(padx=20, pady=10)

app.mainloop()
```

### Icon positioning with `compound`

Control where the icon appears relative to text.

```python
ttk.Label(app, text="Left", icon="star", compound="left").pack(pady=4)
ttk.Label(app, text="Right", icon="star", compound="right").pack(pady=4)
ttk.Label(app, text="Top", icon="star", compound="top").pack(pady=4)
ttk.Label(app, text="Bottom", icon="star", compound="bottom").pack(pady=4)
```

> _Image placeholder:_
> `![Label with icon](../_img/widgets/label/icon.png)`

### Icon-only labels

Use `icon_only=True` for compact icon-only labels (like status indicators or badges).

```python
ttk.Label(
    app,
    icon="circle-fill",  # placeholder
    icon_only=True,
    bootstyle="success",
).pack(pady=6)
```

!!! warning "Using `image=...`"
    You can still pass a Tk `PhotoImage` via `image=...`, but it won't automatically recolor for theme changes.

---

## Reactive text with `textsignal`

If your app uses signals, you can bind the label text to a signal so it updates automatically.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
status = ttk.Signal("Ready")  # pseudo-code

label = ttk.Label(app, textsignal=status, bootstyle="info")
label.pack(padx=20, pady=20)

def start():
    status.set("Running...")

ttk.Button(app, text="Start", command=start).pack(pady=10)

app.mainloop()
```

---

## Localization

If you use message catalogs, `localize="auto"` (or `True`) allows the label text to be treated as a localization key.

```python
ttk.Label(app, text="label.welcome", localize="auto").pack()
```

---

## When should I use Label?

Use `Label` when:

- displaying static or dynamic text
- showing status messages or indicators
- creating section headers or field labels
- displaying icons with or without text

Prefer **TextEntry** when:

- users need to edit the text

Prefer **Button** when:

- the text should trigger an action when clicked

---

## Related widgets

- **TextEntry** — editable text input
- **Tooltip** — contextual help text
- **LabelFrame** — frame with a labeled border