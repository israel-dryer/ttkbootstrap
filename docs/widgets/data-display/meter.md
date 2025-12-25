---
title: Meter
---

# Meter

`Meter` displays a **single numeric value within a range**, often as a circular or arc-style gauge.

It's ideal for dashboards, summaries, and status panels where visual emphasis matters more than precision.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

meter = ttk.Meter(app, amountused=65, amounttotal=100)
meter.pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use Meter when:

- showing a snapshot or status value

- visual emphasis is important

- you need a dashboard-style indicator

### Consider a different control when...

- **Tracking task progress over time** — use [Progressbar](progressbar.md) instead

- **Showing capacity or fullness levels** — use [FloodGauge](floodgauge.md) instead

- **You need a compact text-based indicator** — use [Badge](badge.md) instead

---

## Appearance

### Styling with `bootstyle`

Meters are highly visual and often color-coded:

```python
ttk.Meter(app, bootstyle="success")
ttk.Meter(app, bootstyle="danger")
ttk.Meter(app, bootstyle="info")
```

!!! link "Design System"
    See [Design System](../../design-system/index.md) for color tokens and theming guidelines.

---

## Examples & patterns

### Value model

Meters display:

- `amountused` relative to `amounttotal`

- optional text/label overlays

```python
meter = ttk.Meter(
    app,
    amountused=75,
    amounttotal=100,
    subtext="CPU Usage"
)
meter.pack()
```

### Common options

- `amountused` — current value

- `amounttotal` — maximum value

- `subtext` — label displayed below the value

- `stripethickness` — thickness of the gauge stripe

- `interactive=False` — whether the meter can be adjusted by the user (if supported)

### With subtext

```python
ttk.Meter(
    app,
    amountused=42,
    amounttotal=100,
    subtext="Progress"
).pack()
```

---

## Behavior

- The meter arc fills proportionally based on `amountused / amounttotal`

- Visual updates occur when values are changed programmatically

- Some implementations support interactive mode where users can drag to adjust

---

## Reactivity

Meter can be updated dynamically by binding to signals:

```python
usage = ttk.Signal(50)
meter = ttk.Meter(app, amountused=usage, amounttotal=100)

# Update value
usage.set(75)  # Meter updates automatically
```

!!! link "Signals"
    See [Signals](../../capabilities/signals/signals.md) for reactive programming patterns.

---

## Additional resources

### Related widgets

- [Progressbar](progressbar.md) — linear progress indicators

- [FloodGauge](floodgauge.md) — capacity/level indicators

- [Badge](badge.md) — compact status indicators

### Framework concepts

- [Design System](../../design-system/index.md) — colors, typography, and theming

- [Signals](../../capabilities/signals/signals.md) — reactive data binding

### API reference

- [`ttkbootstrap.Meter`](../../reference/widgets/Meter.md)