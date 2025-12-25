---
title: Progressbar
---

# Progressbar

`Progressbar` displays **task progress over time**.

It communicates how much work has completed (determinate) or that work is ongoing (indeterminate), without requiring user interaction.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

pb = ttk.Progressbar(app, maximum=100, value=40)
pb.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use Progressbar when:

- progress is linear and measurable

- users benefit from seeing completion percentage

- tracking task progress over time

### Consider a different control when...

- **You want a more expressive, dashboard-style indicator** — use [Meter](meter.md) instead

- **You need to show capacity or fullness** — use [FloodGauge](floodgauge.md) instead

- **You need a compact status indicator** — use [Badge](badge.md) for text-based status

---

## Appearance

### Styling with `bootstyle`

Use `bootstyle` to indicate intent or severity:

```python
ttk.Progressbar(app, bootstyle="success")
ttk.Progressbar(app, bootstyle="warning")
ttk.Progressbar(app, bootstyle="danger")
```

!!! link "Design System"
    See [Design System](../../design-system/index.md) for color tokens and theming guidelines.

---

## Examples & patterns

### Value model

- **Determinate**: shows progress between `0` and `maximum`

- **Indeterminate**: animates continuously to indicate ongoing work

```python
pb.configure(mode="indeterminate")
pb.start()
```

### Common options

- `value` — current progress value

- `maximum` — maximum value (default 100)

- `mode="determinate" | "indeterminate"` — progress mode

- `length` — length of the progressbar in pixels

- `orient="horizontal" | "vertical"` — orientation

### Updating progress

```python
pb = ttk.Progressbar(app, maximum=100)
pb.pack()

# Update progress programmatically
pb.configure(value=50)

# Or step by a value
pb.step(10)
```

---

## Behavior

- Determinate mode updates visually as `value` changes

- Indeterminate mode runs an animation until stopped

- Use `start()` to begin indeterminate animation

- Use `stop()` to halt indeterminate animation

```python
# Start indeterminate animation
pb.configure(mode="indeterminate")
pb.start(interval=10)  # interval in milliseconds

# Stop animation
pb.stop()
```

---

## Reactivity

Progressbar can be updated dynamically by binding to signals:

```python
progress = ttk.Signal(0)
pb = ttk.Progressbar(app, value=progress)

# Update progress
progress.set(50)  # Progressbar updates automatically
```

!!! link "Signals"
    See [Signals](../../concepts/signals.md) for reactive programming patterns.

---

## Additional resources

### Related widgets

- [Meter](meter.md) — dashboard-style gauge indicators

- [FloodGauge](floodgauge.md) — capacity/level indicators

- [Badge](badge.md) — compact status indicators

### Framework concepts

- [Design System](../../design-system/index.md) — colors, typography, and theming

- [Signals](../../concepts/signals.md) — reactive data binding

### API reference

- [ttkbootstrap.Progressbar](../../api/widgets/progressbar.md)