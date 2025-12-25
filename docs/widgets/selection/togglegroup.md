---
title: ToggleGroup
---

# ToggleGroup

`ToggleGroup` is a **composite selection control** that groups toggle buttons with **single** or **multi-selection** support.

Use `ToggleGroup` for segmented controls, mode switches, toolbar filters, and compact selection patterns where buttons should read as a connected unit.

---

## Overview

`ToggleGroup` provides:

- **single selection** (`mode="single"`) - radio button behavior, one active at a time
- **multi-selection** (`mode="multi"`) - checkbox behavior, multiple selections allowed
- **horizontal** or **vertical** orientation
- automatic visual grouping with buttongroup styling

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

group = ttk.ToggleGroup(app, mode="single", value="grid")
group.add("Grid", value="grid")
group.add("List", value="list")
group.add("Cards", value="cards")
group.pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `ToggleGroup` when:

- you want a segmented control for mode switching
- you need a compact multi-selection pattern (tags, filters)
- buttons should appear visually connected

### Consider a different control when...

- options should look like classic radio buttons -> use [RadioGroup](radiogroup.md)
- you have unrelated actions that shouldn't look connected -> use separate [Button](../actions/button.md) widgets
- you need grouped action buttons (not selection) -> use [ButtonGroup](../actions/buttongroup.md)

---

## Variants

### Single selection mode

Only one option can be selected at a time (radio button behavior).

```python
group = ttk.ToggleGroup(app, mode="single", value="day")
group.add("Day", value="day")
group.add("Week", value="week")
group.add("Month", value="month")
```

### Multi-selection mode

Multiple options can be selected simultaneously (checkbox behavior).

```python
group = ttk.ToggleGroup(app, mode="multi", value={"bold"})
group.add("Bold", value="bold")
group.add("Italic", value="italic")
group.add("Underline", value="underline")
```

### Orientation

```python
ttk.ToggleGroup(app, orient="horizontal")  # default
ttk.ToggleGroup(app, orient="vertical")
```

---

## How the value works

The value type depends on the mode:

- **single mode**: `str` - the value of the selected option
- **multi mode**: `set[str]` - set of selected option values

```python
# Get current value
current = group.get()

# Set value
group.set("week")           # single mode
group.set({"bold", "italic"})  # multi mode
```

---

## Binding to signals or variables

You can control the group selection with either:

- `signal=...` (preferred)
- `variable=...` (Tk variable - `StringVar` for single, `SetVar` for multi)

If neither is provided, `ToggleGroup` creates an internal variable.

```python
import ttkbootstrap as ttk

app = ttk.App()

view = ttk.Signal("grid")

group = ttk.ToggleGroup(app, mode="single", signal=view)
group.add("Grid", value="grid")
group.add("List", value="list")
group.pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

### `mode`

Selection mode: `"single"` (default) or `"multi"`.

### `orient`

Layout orientation: `"horizontal"` (default) or `"vertical"`.

### `bootstyle`

Applies to all child buttons (defaults to `"primary"`).

```python
group = ttk.ToggleGroup(app, bootstyle="secondary")
```

### `add(text, value, key=None, **kwargs)`

Add an option. `value` is required. `key` defaults to `value`.

```python
group.add("Low", value="low")
group.add("High", value="high", key="hi")
```

---

## Behavior

- In single mode, selecting a new option deselects the previous one.
- In multi mode, clicking toggles the option on/off.
- Buttons are packed based on orientation (horizontal: left-to-right, vertical: top-to-bottom).
- Visual styling uses buttongroup variants with automatic position detection.

---

## Events

Subscribe to value changes using `on_changed`.

```python
def on_change(value):
    print("Selected:", value)

sub_id = group.on_changed(on_change)

# Later:
group.off_changed(sub_id)
```

Callbacks receive the new value directly (string in single mode, set in multi mode).

---

## Colors and styling

`ToggleGroup` forwards `bootstyle` to its child buttons with buttongroup styling.

```python
ttk.ToggleGroup(app, bootstyle="primary")
ttk.ToggleGroup(app, bootstyle="secondary")
ttk.ToggleGroup(app, bootstyle="success")
```

---

## When should I use ToggleGroup?

Use `ToggleGroup` when:

- you want connected button-style selection
- the control appears in toolbars, headers, or compact UI areas
- you need either single or multi-selection in a segmented layout

Prefer **RadioGroup** when:

- classic radio button indicators are expected

Prefer **ButtonGroup** when:

- buttons trigger actions rather than represent selection state

---

## Additional resources

### Related widgets

- [ButtonGroup](../actions/buttongroup.md) - grouped action buttons (no selection state)
- [RadioGroup](radiogroup.md) - grouped radio buttons with classic indicators
- [RadioToggle](radiotoggle.md) - individual toggle-style radio buttons
- [CheckToggle](checktoggle.md) - individual toggle-style checkboxes

### API reference

- [`ttkbootstrap.ToggleGroup`](../../reference/widgets/ToggleGroup.md)