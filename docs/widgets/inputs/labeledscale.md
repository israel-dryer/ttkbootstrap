---
title: LabeledScale
---

# LabeledScale

`LabeledScale` is a **horizontal scale widget** with a label that displays and follows the current value.

Use `LabeledScale` when users need visual feedback of the exact value as they drag the slider - common for volume controls, opacity settings, or any numeric range where precision matters.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

scale = ttk.LabeledScale(
    app,
    value=50,
    minvalue=0,
    maxvalue=100,
)
scale.pack(padx=20, pady=20, fill="x")

app.mainloop()
```

---

## When to use

Use `LabeledScale` when:

- users need to see the exact value while dragging
- you want a compact slider with built-in value display
- the value label should track the slider position

### Consider a different control when...

- you don't need a tracking label -> use [Scale](scale.md)
- you need a numeric entry with increment buttons -> use [SpinnerEntry](spinnerentry.md)
- you need fine-grained numeric input -> use [NumericEntry](numericentry.md)

---

## Appearance

### `compound`

Label position relative to the scale:

- `"before"` (default) - label above the scale
- `"after"` - label below the scale

```python
ttk.LabeledScale(app, compound="after")
```

### `bootstyle`

Style applied to both the scale and label.

```python
ttk.LabeledScale(app, bootstyle="success")
```

!!! link "Design System"
    LabeledScale styling follows the theme's color palette. See [Design System](../../design-system/index.md) for customization options.

---

## Examples and patterns

### `value`

Initial value for the scale. Defaults to 0.

### `minvalue` / `maxvalue`

Range of the scale. Defaults to 0-100.

```python
ttk.LabeledScale(app, minvalue=0, maxvalue=255)  # RGB range
ttk.LabeledScale(app, minvalue=-50, maxvalue=50)  # Centered range
```

### `dtype`

Data type for the value: `int` (default) or `float`.

```python
ttk.LabeledScale(app, dtype=float, minvalue=0.0, maxvalue=1.0)
```

### `variable`

A tkinter variable to associate with the scale. If None, creates an IntVar or DoubleVar based on dtype.

### Value access

```python
# Get current value
current = scale.value

# Set value programmatically
scale.value = 75
```

---

## Behavior

- The label automatically updates to display the current value.
- The label position follows the slider handle as it moves.
- Only horizontal orientation is supported.
- Values outside the range are clamped to the last valid value.

---

## Additional resources

### Related widgets

- [Scale](scale.md) - basic scale without tracking label
- [SpinnerEntry](spinnerentry.md) - numeric input with increment/decrement buttons
- [NumericEntry](numericentry.md) - numeric input field with validation

### API reference

- [`ttkbootstrap.LabeledScale`](../../reference/widgets/LabeledScale.md)