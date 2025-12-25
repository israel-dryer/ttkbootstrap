---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: Spinbox
---

# Spinbox

`Spinbox` is a **primitive input** that wraps `ttk.Spinbox` with ttkbootstrap styling and reactive text support.

It provides low-level spin behavior (range or list stepping) while still allowing direct typing. Use `Spinbox` when you want
native ttk options like `format` and `command`. For a form-ready field with labels/messages/validation and standardized events,
prefer **SpinnerEntry**. fileciteturn14file4

---

## Basic usage

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

## Value model

Spinbox stores and returns **text** (even in numeric mode).

```python
value = spin.get()
```

Bind with:

- `textvariable=` (Tk variable), or

- `textsignal=` (reactive signal)

---

## Common options

### Range mode: `from_`, `to`, `increment`

```python
ttk.Spinbox(app, from_=1, to=31, increment=1)
```

### Values mode: `values`

```python
ttk.Spinbox(app, values=("Low", "Medium", "High"))
```

If `values` is provided, it takes precedence over the numeric range.

### `wrap`

```python
ttk.Spinbox(app, from_=0, to=5, wrap=True)
ttk.Spinbox(app, values=("A", "B", "C"), wrap=True)
```

### `state="readonly"`

Use readonly mode when you want pick-only interaction.

```python
ttk.Spinbox(app, values=("A", "B", "C"), state="readonly")
```

### `format` (range mode)

```python
ttk.Spinbox(app, from_=0, to=1, increment=0.05, format="%.2f")
```

---

## Behavior

- Users can type or use arrows to step.

- In many Tk builds, `command` is primarily invoked by arrow interactions (not typing).

- Wrapping cycles max→min (range) or last→first (values).

---

## Events

### `command`

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

## Validation and constraints

Spinbox does not provide control-level parsing/validation by default. It is a primitive widget.

For validated, commit-based workflows, prefer **SpinnerEntry** or **NumericEntry**.

---

## When should I use Spinbox?

Use `Spinbox` when:

- you want low-level ttk spinbox behavior and options

- the range/list is small and predictable

- you’re building your own composite control

Prefer **SpinnerEntry** when:

- you want a form-ready field (labels/messages/validation/events)

Prefer **SelectBox** when:

- the choices are better expressed as a dropdown list

---

## Related widgets

- **SpinnerEntry** — form-ready stepper control

- **NumericEntry** — validated numeric input

- **Scale** — continuous adjustment

- **Combobox** — selection + optional typing

---

## Reference

- **API Reference:** `ttkbootstrap.Spinbox`

---

## Additional resources

### Related widgets

- [Canvas](canvas.md)

- [Combobox](combobox.md)

- [Entry](entry.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Spinbox`](../../reference/widgets/Spinbox.md)
