---
title: FloodGauge
---

# FloodGauge

`FloodGauge` is a **filled-level indicator** that visualizes how full a value is within a range.

It’s especially useful for capacity, utilization, or threshold-based indicators.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

fg = ttk.FloodGauge(app, value=75)
fg.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## Value model

- `value` represents fill level (commonly 0–100)
- optional thresholds can alter styling

---

## Common options

- `value`
- `maximum`
- `text`
- `orient`

---

## Styling

Flood gauges often change color as thresholds are crossed:

```python
ttk.FloodGauge(app, bootstyle="warning")
```

---

## When should I use FloodGauge?

Use FloodGauge when:

- capacity or fullness matters
- thresholds are more important than exact numbers

---

## Related widgets

- **Progressbar**
- **Meter**

---

## Reference

- **API Reference:** `ttkbootstrap.FloodGauge`
