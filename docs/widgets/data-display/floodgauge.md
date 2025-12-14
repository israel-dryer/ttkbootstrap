---
title: FloodGauge
icon: fontawesome/solid/water
---

# FloodGauge

`FloodGauge` displays progress as a filling area.
It is visually expressive and best for high-level status indicators.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

gauge = ttk.FloodGauge(app, value=70)
gauge.pack(padx=20, pady=20)

app.mainloop()
```

---

## What problem it solves

Flood gauges emphasize *direction* and *completion* rather than exact values.

---

## UX guidance

- Use sparingly for emphasis
- Avoid for precise measurements

---

## Related widgets

- **Progressbar**
- **Meter**
