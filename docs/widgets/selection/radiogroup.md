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

title: RadioGroup
---

# RadioGroup

`RadioGroup` is a **composite selection control** that manages a set of `RadioButton` widgets as a single unit.

Use `RadioGroup` when you want a convenient way to build a mutually exclusive choice list without manually wiring
multiple `RadioButton` instances to the same signal or variable.

---

## Overview

A `RadioGroup`:

- manages a shared selection value (via `signal` or `variable`)

- provides `add()` to create options

- supports **horizontal** or **vertical** layout

- can display an optional **group label** positioned with `labelanchor`

---

## Basic usage

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

## Variants

`RadioGroup` primarily varies by **orientation** and **label placement**.

### Orientation

```python
ttk.RadioGroup(app, orient="horizontal")
ttk.RadioGroup(app, orient="vertical")
```

### Label placement

`labelanchor` controls where the label appears relative to the buttons:

- `'n'` (top, default), `'s'` (bottom), `'w'` (left), `'e'` (right)

- compound anchors like `'nw'`, `'se'` are accepted and normalized

```python
ttk.RadioGroup(app, text="Pick one", labelanchor="w", orient="horizontal")
```

---

## How the value works

`RadioGroup` exposes a single selected value.

- `value=` sets the initial selection (stored in the underlying variable)

- `get()` returns the current selection

- `set(value)` selects an option by value (or `""` to deselect)

```python
group.set("pro")
print(group.get())
```

---

## Binding to signals or variables

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

---

## Common options

### `bootstyle`

Applies to the child `RadioButton` widgets (defaults to `"primary"`).

```python
group = ttk.RadioGroup(app, bootstyle="success")
```

### `state`

Sets the state for all buttons (`"normal"` or `"disabled"`).

```python
group = ttk.RadioGroup(app, state="disabled")
```

### `add(text, value, key=None, **kwargs)`

Add an option. `value` is required. `key` defaults to `value`.

```python
group.add("Low", "low")
group.add("High", "high", key="hi")
```

---

## Behavior

- In horizontal orientation, buttons are packed left-to-right.

- In vertical orientation, buttons are stacked top-to-bottom.

- Changing `orient`, `bootstyle`, `state`, `text`, `labelanchor`, or `value` via `configure(...)`
  updates the group and its children.

---

## Events

Subscribe to changes using `on_changed`.

```python
def on_change(value):
    print("Selected:", value)

sub_id = group.on_changed(on_change)
# Later: group.off_changed(sub_id)
```

This subscribes to the underlying signal, so callbacks receive the **new value**.

---

## Validation and constraints

`RadioGroup` enforces that selected values correspond to existing options:

- `set(value)` raises if `value` does not exist (except `""` which clears selection)

Validation is most useful when selection is required before submission.

---

## Colors and styling

`RadioGroup` forwards `bootstyle` to its child radio buttons.

For more control, pass per-button options via `add(..., **kwargs)` or `style_options`.

---

## Localization

If you use a group label (`text=`) or per-option labels, they follow your normal localization rules
for `Label` and `RadioButton` text.

---

## When should I use RadioGroup?

Use `RadioGroup` when:

- you want a single widget that manages a set of radio options

- you want consistent layout and labeling for the group

- you want a simple subscribe/unsubscribe change API

Prefer individual **RadioButton** widgets when:

- you need custom per-option layout (different rows/columns, mixed widgets)

- you want complete control over spacing and structure

---

## Related widgets

- **RadioButton** — individual radio option

- **RadioToggle** — button-like radio option

- **SelectBox** — single selection from a list (dropdown)

- **CheckButton** — independent multi-selection

---

## Reference

- **API Reference:** `ttkbootstrap.RadioGroup`

---

## Additional resources

### Related widgets

- [Calendar](calendar.md)

- [CheckButton](checkbutton.md)

- [CheckToggle](checktoggle.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.RadioGroup`](../../reference/widgets/RadioGroup.md)
