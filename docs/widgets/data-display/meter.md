---
title: Meter
icon: fontawesome/solid/gauge
---

# Meter

`Meter` displays progress or value using a circular gauge.
It is ideal for dashboards and summaries.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

meter = ttk.Meter(app, amountused=65, amounttotal=100)
meter.pack(padx=20, pady=20)

app.mainloop()
```

---

## What problem it solves

Meters communicate progress or utilization at a glance.

---

## UX guidance

- Use meters for summaries, not precise tracking
- Pair with labels for clarity

---

## Related widgets

- **Progressbar**
- **FloodGauge**
