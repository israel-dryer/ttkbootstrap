---
title: Spinbox
icon: fontawesome/solid/sort
---

# Spinbox

`Spinbox` is a themed wrapper around `ttk.Spinbox` that integrates ttkbootstrap styling and reactive text support. It’s a **primitive input** that lets users adjust a value via up/down arrows, while still allowing direct typing in the entry field.

<!--
IMAGE: Spinbox basic states
Suggested: Spinbox showing numeric value with arrows; include readonly and disabled variants
Theme variants: light / dark
-->

---

## Basic usage

Use a numeric range spinbox:

```python
import ttkbootstrap as ttk

app = ttk.App()

spin = ttk.Spinbox(app, from_=0, to=10, increment=1, width=8)
spin.pack(padx=20, pady=20)

app.mainloop()
```

Use a fixed list of values:

```python
import ttkbootstrap as ttk

app = ttk.App()

spin = ttk.Spinbox(app, values=("XS", "S", "M", "L", "XL"), wrap=True, width=8)
spin.pack(padx=20, pady=20)

app.mainloop()
```

<!--
IMAGE: Spinbox range vs values
Suggested: Two spinboxes side-by-side (range-based and values-based)
-->

---

## What problem it solves

A spinbox provides a compact way to nudge a value up or down without requiring a separate slider or multiple buttons. It’s especially useful for:

- Small numeric adjustments (quantity, steps, levels)
- Cycling through a short list of options
- Power-user workflows where typing + incrementing both matter

ttkbootstrap’s `Spinbox` adds consistent theme styling and reactive binding via `textsignal`.

---

## Core concepts

### Range mode vs values mode

You can configure a spinbox in one of two ways:

**Range mode**: provide `from_`, `to`, and optional `increment`.

```python
ttk.Spinbox(app, from_=1, to=31, increment=1)
```

**Values mode**: provide an explicit `values` sequence.

```python
ttk.Spinbox(app, values=("Low", "Medium", "High"))
```

If you provide `values`, it takes precedence over the numeric range.

---

### Wrapping

With `wrap=True`, the spinbox cycles:

- from max → min (range mode)
- last → first (values mode)

```python
ttk.Spinbox(app, from_=0, to=5, wrap=True)
```

---

### Typing vs arrows

Spinboxes allow both:

- typing into the entry portion
- using the arrows to step

If you want to restrict to “selection only,” use `state="readonly"`.

```python
ttk.Spinbox(app, values=("A", "B", "C"), state="readonly")
```

---

### Reactive text with `textsignal`

Like other ttkbootstrap primitives, `Spinbox` supports `textsignal` for reactive synchronization with application state:

```python
spin = ttk.Spinbox(app, from_=0, to=100, textsignal=my_signal)
```

<!--
IMAGE: Reactive spinbox text
Suggested: Diagram-style image showing signal <-> spinbox text synchronization
-->

---

## Common options & patterns

### Format strings

`format` can be used to control how values are displayed (range mode):

```python
ttk.Spinbox(app, from_=0, to=1, increment=0.1, format="%.1f")
```

---

### Handling changes (command)

`command` runs when the value changes via the spinbox controls:

```python
def on_change():
    print(spin.get())

spin = ttk.Spinbox(app, from_=0, to=10, command=on_change)
```

!!! note "Typing vs command"
    `command` is typically triggered by arrow interactions. If you need to react to typing, bind events on the entry portion (e.g., `<KeyRelease>`), or use a higher-level control with standardized events.

---

### Styling with bootstyle

```python
ttk.Spinbox(app, from_=0, to=10, bootstyle="primary")
ttk.Spinbox(app, values=("A", "B"), bootstyle="secondary")
```

You can also provide a concrete ttk style name via `style=...` which overrides bootstyle.

---

## Events

Spinbox is a primitive widget, so you typically use standard Tk/ttk events:

- `<<Increment>>` / `<<Decrement>>` (when supported by Tk build)
- `<KeyRelease>` for typing
- `<FocusOut>` for commit-style workflows

```python
spin.bind("<KeyRelease>", lambda e: print(spin.get()))
```

!!! tip "Form-friendly spin input"
    If you want labels, validation messages, and consistent `on_input(...)` / `on_changed(...)` semantics, use `SpinnerEntry` (the control) instead of `Spinbox` (the primitive).

---

## UX guidance

- Use spinboxes for small increments where the user benefits from “nudging”
- Avoid spinboxes for large ranges (use `Scale` or a numeric entry + validation)
- Prefer readonly when free-form typing would cause invalid values

---

## When to use / when not to

**Use Spinbox when:**

- You need a small “stepper” control
- The range is small and predictable
- You want both typing and increment/decrement affordances

**Avoid Spinbox when:**

- You need robust validation and messaging (use `SpinnerEntry` / `NumericEntry`)
- The range is large or needs precision controls (use `NumericEntry`)
- Options are long or need search (use `Combobox` / `SelectBox`)

---

## Related widgets

- **SpinnerEntry** — form-ready stepper control (labels/messages/events)
- **NumericEntry** — validated numeric input
- **Scale** — slider for continuous adjustment
- **Combobox** — selection + optional typing
