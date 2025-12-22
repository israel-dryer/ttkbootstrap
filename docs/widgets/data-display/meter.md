---
title: Meter
---

# Meter

`Meter` displays a **single numeric value within a range**, often as a circular or arc-style gauge.

It’s ideal for dashboards, summaries, and status panels where visual emphasis matters more than precision.

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

## Value model

Meters display:

- `amountused` relative to `amounttotal`
- optional text/label overlays

---

## Common options

- `amountused`
- `amounttotal`
- `subtext`
- `stripethickness`
- `interactive=False` (if supported)

---

## Styling

Meters are highly visual and often color-coded:

```python
ttk.Meter(app, bootstyle="success")
ttk.Meter(app, bootstyle="danger")
```

---

## When should I use Meter?

Use Meter when:

- showing a snapshot or status
- visual emphasis is important

Prefer **Progressbar** when:

- tracking task progress over time

---

## Related widgets

- **Progressbar**
- **FloodGauge**

---

## Reference

- **API Reference:** `ttkbootstrap.Meter`
