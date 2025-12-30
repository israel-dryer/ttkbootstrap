---
title: Spinbox
---

# Spinbox

`Spinbox` is a **primitive input** that wraps `ttk.Spinbox` with ttkbootstrap styling and reactive text support.

It provides low-level spin behavior (range or list stepping) while still allowing direct typing. Use `Spinbox` when you want
native ttk options like `format` and `command`. For a form-ready field with labels/messages/validation and standardized events,
prefer [SpinnerEntry](/widgets/inputs/spinnerentry.md).

---

## Quick start

### Numeric range

```python
import ttkbootstrap as ttk

app = ttk.App()

spin = ttk.Spinbox(app, from_=0, to=10, increment=1, width=8)
spin.pack(padx=20, pady=20)

app.mainloop()
```

### Fixed list of values

```python
import ttkbootstrap as ttk

app = ttk.App()

spin = ttk.Spinbox(app, values=("XS", "S", "M", "L", "XL"), wrap=True, width=8)
spin.pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `Spinbox` when:

- you want low-level ttk spinbox behavior and options

- the range/list is small and predictable

- you're building your own composite control

### Consider a different control when...

- **you want a form-ready field (labels/messages/validation/events)** - prefer [SpinnerEntry](/widgets/inputs/spinnerentry.md)

- **the choices are better expressed as a dropdown list** - prefer [SelectBox](/widgets/selection/selectbox.md)

---

## Appearance

### `color`

Applies ttkbootstrap theme styling.

```python
ttk.Spinbox(app, from_=0, to=10, color="primary")
```

!!! link "Design System"
    See the [Design System](../../design-system/index.md) for available color tokens.

---

## Examples and patterns

### Value model

Spinbox stores and returns **text** (even in numeric mode).

```python
value = spin.get()
```

Bind with:

- `textvariable=` (Tk variable), or

- `textsignal=` (reactive signal)

### Common options

#### Range mode: `from_`, `to`, `increment`

```python
ttk.Spinbox(app, from_=1, to=31, increment=1)
```

#### Values mode: `values`

```python
ttk.Spinbox(app, values=("Low", "Medium", "High"))
```

If `values` is provided, it takes precedence over the numeric range.

#### `wrap`

```python
ttk.Spinbox(app, from_=0, to=5, wrap=True)
ttk.Spinbox(app, values=("A", "B", "C"), wrap=True)
```

#### `state="readonly"`

Use readonly mode when you want pick-only interaction.

```python
ttk.Spinbox(app, values=("A", "B", "C"), state="readonly")
```

#### `format` (range mode)

```python
ttk.Spinbox(app, from_=0, to=1, increment=0.05, format="%.2f")
```

### Events

#### `command`

```python
def on_change():
    print(spin.get())

spin = ttk.Spinbox(app, from_=0, to=10, command=on_change)
```

If you need to respond to typing, bind key events:

```python
spin.bind("<KeyRelease>", lambda e: print(spin.get()))
```

---

## Behavior

- Users can type or use arrows to step.

- In many Tk builds, `command` is primarily invoked by arrow interactions (not typing).

- Wrapping cycles max->min (range) or last->first (values).

### Validation and constraints

Spinbox does not provide control-level parsing/validation by default. It is a primitive widget.

For validated, commit-based workflows, prefer [SpinnerEntry](/widgets/inputs/spinnerentry.md) or [NumericEntry](/widgets/inputs/numericentry.md).

---

## Additional resources

### Related widgets

- [SpinnerEntry](/widgets/inputs/spinnerentry.md) - form-ready stepper control

- [NumericEntry](/widgets/inputs/numericentry.md) - validated numeric input

- [Scale](/widgets/inputs/scale.md) - continuous adjustment

- [Combobox](/widgets/primitives/combobox.md) - selection + optional typing

### Framework concepts

- [Events and Signals](../../capabilities/signals/signals.md)

### API reference

- [`ttkbootstrap.Spinbox`](../../reference/widgets/Spinbox.md)