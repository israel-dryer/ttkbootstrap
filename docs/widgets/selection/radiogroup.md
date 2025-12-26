---
title: RadioGroup
---

# RadioGroup

`RadioGroup` is a **composite selection control** that manages a set of `RadioButton` widgets as a single unit.

Use `RadioGroup` when you want a convenient way to build a mutually exclusive choice list without manually wiring
multiple `RadioButton` instances to the same signal or variable.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

group = ttk.RadioGroup(app, text="Choose a plan", orient="vertical", value="basic")
group.add("Basic", "basic")
group.add("Pro", "pro")
group.add("Enterprise", "enterprise")
group.pack(padx=20, pady=20, fill="x")

app.mainloop()
```

---

## When to use

Use `RadioGroup` when:

- you want a single widget that manages a set of radio options

- you want consistent layout and labeling for the group

- you want a simple subscribe/unsubscribe change API

### Consider a different control when...

- you need custom per-option layout (different rows/columns, mixed widgets) — use individual **RadioButton** widgets

- you want complete control over spacing and structure — use individual **RadioButton** widgets

---

## Appearance

### Variants

`RadioGroup` primarily varies by **orientation** and **label placement**.

#### Orientation

```python
ttk.RadioGroup(app, orient="horizontal")
ttk.RadioGroup(app, orient="vertical")
```

#### Label placement

`labelanchor` controls where the label appears relative to the buttons:

- `'n'` (top, default), `'s'` (bottom), `'w'` (left), `'e'` (right)

- compound anchors like `'nw'`, `'se'` are accepted and normalized

```python
ttk.RadioGroup(app, text="Pick one", labelanchor="w", orient="horizontal")
```

### Colors and styling

`RadioGroup` forwards `bootstyle` to its child radio buttons.

For more control, pass per-button options via `add(..., **kwargs)` or `style_options`.

!!! link "Design System"
    For available colors and styling options, see the [Design System](/design-system/) documentation.

---

## Examples and patterns

### How the value works

`RadioGroup` exposes a single selected value.

- `value=` sets the initial selection (stored in the underlying variable)

- `get()` returns the current selection

- `set(value)` selects an option by value (or `""` to deselect)

```python
group.set("pro")
print(group.get())
```

### Common options

#### `bootstyle`

Applies to the child `RadioButton` widgets (defaults to `"primary"`).

```python
group = ttk.RadioGroup(app, bootstyle="success")
```

#### `state`

Sets the state for all buttons (`"normal"` or `"disabled"`).

```python
group = ttk.RadioGroup(app, state="disabled")
```

#### `add(text, value, key=None, **kwargs)`

Add an option. `value` is required. `key` defaults to `value`.

```python
group.add("Low", "low")
group.add("High", "high", key="hi")
```

### Events

Subscribe to changes using `on_changed`.

```python
def on_change(value):
    print("Selected:", value)

sub_id = group.on_changed(on_change)
# Later: group.off_changed(sub_id)
```

This subscribes to the underlying signal, so callbacks receive the **new value**.

### Validation and constraints

`RadioGroup` enforces that selected values correspond to existing options:

- `set(value)` raises if `value` does not exist (except `""` which clears selection)

Validation is most useful when selection is required before submission.

---

## Behavior

- In horizontal orientation, buttons are packed left-to-right.

- In vertical orientation, buttons are stacked top-to-bottom.

- Changing `orient`, `bootstyle`, `state`, `text`, `labelanchor`, or `value` via `configure(...)`
  updates the group and its children.

---

## Localization

If you use a group label (`text=`) or per-option labels, they follow your normal localization rules
for `Label` and `RadioButton` text.

!!! link "Localization"
    For more information on localizing your application, see the [Localization](/capabilities/localization/) documentation.

---

## Reactivity

You can control the group selection with either:

- `signal=...` (preferred)

- `variable=...` (Tk `StringVar`)

If neither is provided, `RadioGroup` creates an internal variable.

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.Signal("opt2")

group = ttk.RadioGroup(app, text="Select:", signal=choice, orient="vertical")
group.add("Option 1", "opt1")
group.add("Option 2", "opt2")
group.pack(padx=20, pady=20)

app.mainloop()
```

!!! link "Signals"
    For more information on reactive programming with signals, see the [Signals](/capabilities/signals/) documentation.

---

## Additional resources

### Related widgets

- [RadioButton](radiobutton.md) — individual radio option

- [RadioToggle](radiotoggle.md) — button-like radio option

- [SelectBox](selectbox.md) — single selection from a list (dropdown)

- [CheckButton](checkbutton.md) — independent multi-selection

### Framework concepts

- [Design System](/design-system/) — colors, themes, and styling

- [Signals](/capabilities/signals/) — reactive state management

- [Localization](/capabilities/localization/) — internationalization support

### API reference

- [`ttkbootstrap.RadioGroup`](../../reference/widgets/RadioGroup.md)