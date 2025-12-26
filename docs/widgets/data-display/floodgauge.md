---
title: FloodGauge
---

# FloodGauge

`FloodGauge` is a **filled-level indicator** that visualizes how full a value is within a range.

It's especially useful for capacity, utilization, or threshold-based indicators.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

fg = ttk.FloodGauge(app, value=75)
fg.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use FloodGauge when:

- capacity or fullness matters

- thresholds are more important than exact numbers

- visualizing resource utilization

### Consider a different control when...

- **Tracking task progress over time** — use [Progressbar](progressbar.md) instead

- **You need a dashboard-style circular gauge** — use [Meter](meter.md) instead

- **You need a compact text-based indicator** — use [Badge](badge.md) instead

---

## Appearance

### Styling with `bootstyle`

Flood gauges often change color as thresholds are crossed:

```python
ttk.FloodGauge(app, bootstyle="warning")
ttk.FloodGauge(app, bootstyle="danger")
ttk.FloodGauge(app, bootstyle="success")
```

!!! link "Design System"
    See [Design System](../../design-system/index.md) for color tokens and theming guidelines.

---

## Examples & patterns

### Value model

- `value` represents fill level (commonly 0-100)

- optional thresholds can alter styling

```python
fg = ttk.FloodGauge(app, value=80, maximum=100)
fg.pack()
```

### Common options

- `value` — current fill level

- `maximum` — maximum value (default 100)

- `text` — label displayed on the gauge

- `orient` — orientation (`"horizontal"` or `"vertical"`)

### With text label

```python
ttk.FloodGauge(
    app,
    value=65,
    text="Storage"
).pack(fill="x", padx=20)
```

### Vertical orientation

```python
ttk.FloodGauge(
    app,
    value=50,
    orient="vertical"
).pack(pady=20)
```

---

## Behavior

- The gauge fill level updates proportionally based on `value / maximum`

- Visual updates occur when values are changed programmatically

- Color/style can change based on threshold values

---

## Reactivity

FloodGauge can be updated dynamically by binding to signals:

```python
level = ttk.Signal(25)
fg = ttk.FloodGauge(app, value=level)

# Update value
level.set(90)  # FloodGauge updates automatically
```

!!! link "Signals"
    See [Signals](../../capabilities/signals/signals.md) for reactive programming patterns.

---

## Additional resources

### Related widgets

- [Progressbar](progressbar.md) — linear progress indicators

- [Meter](meter.md) — dashboard-style gauge indicators

- [Badge](badge.md) — compact status indicators

### Framework concepts

- [Design System](../../design-system/index.md) — colors, typography, and theming

- [Signals](../../capabilities/signals/signals.md) — reactive data binding

### API reference

- [`ttkbootstrap.FloodGauge`](../../reference/widgets/FloodGauge.md)