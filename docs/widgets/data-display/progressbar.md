---
title: Progressbar
icon: fontawesome/solid/bars-progress
---

# Progressbar

`Progressbar` displays progress toward completion of a task.
It supports determinate and indeterminate modes.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

pb = ttk.Progressbar(app, maximum=100, value=40)
pb.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## What problem it solves

Progress indicators communicate that work is happening and how much remains.

---

## Core concepts

### Determinate vs indeterminate

- **Determinate**: known progress
- **Indeterminate**: unknown duration

---

## UX guidance

- Always show progress for tasks > ~300ms
- Prefer determinate when possible

---

## Related widgets

- **Meter**
- **FloodGauge**
