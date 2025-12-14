---
title: Scale
icon: fontawesome/solid/sliders
---

# Scale

`Scale` is a **direct-manipulation control** for selecting a numeric value from a continuous or stepped range.

Unlike `NumericEntry`, which is optimized for precise values, `Scale` is designed for **gesture-based adjustment** —
making it ideal for volume, zoom, thresholds, or any value where users benefit from immediate visual feedback.

> _Image placeholder:_  
> `![Scale overview](../_img/widgets/scale/overview.png)`  
> Suggested shot: horizontal scale + value label + live update.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

scale = ttk.Scale(
    app,
    from_=0,
    to=100,
    value=50,
)
scale.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## What problem does Scale solve?

Numeric values are not always best entered by typing:

- users may not know the exact value
- relative adjustment matters more than precision
- live feedback improves usability

`Scale` allows users to **drag to explore values**, while still producing a usable numeric result.

---

## Range and orientation

```python
scale = ttk.Scale(
    app,
    from_=10,
    to=200,
    orient="horizontal",  # or "vertical"
)
```

!!! note "Orientation"
    Horizontal scales are preferred for most desktop layouts.  
    Vertical scales work best for audio levels or side panels.

---

## Step resolution

If your implementation supports stepping, use it to constrain values.

```python
scale = ttk.Scale(
    app,
    from_=0,
    to=10,
    step=1,    # example option
)
```

!!! note "Continuous vs stepped"
    Continuous scales are best for perception-based adjustment.  
    Stepped scales are best when values must align to discrete states.

---

## Displaying the current value

It’s common to show the selected value alongside a scale.

```python
value_label = ttk.Label(app, text="50")

def update_value(event):
    value_label.config(text=str(int(event.data)))

scale.on_input(update_value)
```

!!! tip "Live feedback"
    Use `on_input(...)` to update previews or labels while dragging.  
    Use `on_changed(...)` when the value is committed.

---

## Text vs value

`Scale` always represents a numeric value, but the distinction between
**live changes** and **committed changes** still matters.

| Event | When it fires |
|------|---------------|
| `on_input` | while the thumb is moving |
| `on_changed` | when the user releases the thumb |

---

## Validation and constraints

Scales inherently constrain values to their range, so validation is usually minimal.

Use validation when:

- the scale is conditionally enabled
- the range changes dynamically
- the value must satisfy cross-field rules

---

## Events

`Scale` emits standard change events:

- `<<Input>>` — value changing while dragging
- `<<Changed>>` — final value committed

Attach handlers using the convenience helpers:

```python
def handle_changed(event):
    print("final value:", event.data)

scale.on_changed(handle_changed)
```

---

## When should I use Scale?

Use `Scale` when:

- users benefit from visual, continuous adjustment
- live previews matter
- exact precision is not critical

Prefer `NumericEntry` when:

- users need to type exact values
- values must be validated strictly
- accessibility via keyboard input is primary

---

## Related widgets

- **NumericEntry** — precise numeric input
- **Progressbar** — display progress, not input
- **Meter** — display proportional values
