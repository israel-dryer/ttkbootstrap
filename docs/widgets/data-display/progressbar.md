---
title: Progressbar
---

# Progressbar

`Progressbar` displays **task progress over time**.

It communicates how much work has completed (determinate) or that work is ongoing (indeterminate), without requiring user interaction.

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

## Value model

- **Determinate**: shows progress between `0` and `maximum`
- **Indeterminate**: animates continuously to indicate ongoing work

```python
pb.configure(mode="indeterminate")
pb.start()
```

---

## Common options

- `value`
- `maximum`
- `mode="determinate" | "indeterminate"`
- `length`
- `orient="horizontal" | "vertical"`

---

## Behavior

- Determinate mode updates visually as `value` changes
- Indeterminate mode runs an animation until stopped

---

## Styling

Use `bootstyle` to indicate intent or severity:

```python
ttk.Progressbar(app, bootstyle="success")
ttk.Progressbar(app, bootstyle="warning")
```

---

## When should I use Progressbar?

Use Progressbar when:

- progress is linear and measurable
- users benefit from seeing completion percentage

Prefer **Meter** when:

- you want a more expressive, dashboard-style indicator

---

## Related widgets

- **Meter**
- **FloodGauge**
- **Spinner / BusyIndicator** (if available)

---

## Reference

- **API Reference:** `ttkbootstrap.Progressbar`
