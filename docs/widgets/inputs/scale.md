---
title: Scale
---

# Scale

`Scale` is a **direct-manipulation input control** for selecting a numeric value from a continuous or stepped range.

Unlike `NumericEntry`, which is optimized for precise typing, `Scale` is designed for **gesture-based adjustment** —
ideal for volume, zoom, thresholds, and any setting where users benefit from immediate visual feedback.

> _Image placeholder:_  
> `![Scale overview](../_img/widgets/scale/overview.png)`  
> Suggested shot: horizontal scale + value label + live update.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

scale = ttk.Scale(app, from_=0, to=100, value=50)
scale.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

A `Scale` always produces a numeric value within its configured range.

- The displayed value updates while the user drags the thumb.
- A **committed** value is produced when the user releases the thumb.

If your app treats “live preview” differently from “final commit”, use the appropriate event hook
(see **Events**).

---

## Common options

### `from_` and `to`

Defines the numeric range.

```python
ttk.Scale(app, from_=10, to=200)
```

### `orient`

Controls orientation.

```python
ttk.Scale(app, from_=0, to=100, orient="horizontal")  # or "vertical"
```

!!! note "Orientation"
    Horizontal scales are preferred for most desktop layouts.  
    Vertical scales work well for audio levels, side panels, or compact tool areas.

### `value`

Sets the initial value.

```python
ttk.Scale(app, from_=0, to=100, value=25)
```

### `step`

If supported by your implementation, constrains values to discrete increments.

```python
ttk.Scale(app, from_=0, to=10, step=1)
```

!!! note "Continuous vs stepped"
    - **Continuous scales** are best for perception-based adjustment  
    - **Stepped scales** are best when values must align to discrete states

---

## Behavior

Scales are commonly paired with a label or preview to reflect the current value.

```python
value_label = ttk.Label(app, text="50")

def update_value(event):
    value_label.config(text=str(int(event.data)))

scale.on_input(update_value)
```

---

## Events

`Scale` distinguishes between **live input** and **committed change**.

| Event | When it fires |
|------|---------------|
| `on_input` | while the thumb is moving |
| `on_changed` | when the user releases the thumb |

```python
def handle_changed(event):
    print("final value:", event.data)

scale.on_changed(handle_changed)
```

!!! tip "Live feedback"
    Use `on_input(...)` to update previews or labels while dragging.  
    Use `on_changed(...)` when the value is committed.

---

## Validation and constraints

Because a `Scale` inherently constrains values to a known range, explicit validation is usually minimal.

Validation is most useful when:

- the scale is conditionally enabled/required
- the valid range changes dynamically
- the value must satisfy cross-field rules

---

## When should I use Scale?

Use `Scale` when:

- users benefit from visual, continuous adjustment
- relative changes matter more than precision
- live feedback improves usability

Prefer `NumericEntry` when:

- users must type exact values
- values require strict validation
- keyboard-first accessibility is primary

---

## Related widgets

- **NumericEntry** — precise numeric input
- **Spinbox / SpinnerEntry** — numeric stepping with typing
- **Progressbar** — displays progress, not user input
- **Meter** — displays proportional values

---

## Reference

- **API Reference:** `ttkbootstrap.Scale`
