---
title: FloodGauge
icon: fontawesome/solid/wave-square
---


# FloodGauge

`FloodGauge` is a canvas-based progress indicator that blends determinate/indeterminate modes, text overlays, and flexible orientation without relying on native ttk styling.

It delivers animated pulses, theming via bootstyle/surface tokens, and format masks so you can build modern dashboards, loaders, or status chips.

---

## Overview

Key FloodGauge capabilities:

- Canvas rendering allows full control over orientation (`horizontal` or `vertical`), length/thickness, and colors driven by `bootstyle`.
- Supports `mode="determinate"` with masked text overlays (`mask='{:.0f}%'`) or `mode="indeterminate"` with bouncing pulse animation.
- Text displays are powered by `mask`, `text`, and underlying `textvariable` (defaults to `StringVar`), while numeric progress ties to `value`, `maximum`, and `variable` (`IntVar` by default).
- Methods such as `start()`, `stop()`, and `step()` animate or drive progress, and configuration delegates let you mutate `mask`, `orient`, `font`, etc., at runtime.
- Color updates happen automatically on `<<ThemeChanged>>`, so the gauge stays in sync with your active theme.

Use FloodGauge whenever you need a visually distinct progress meter that feels more expressive than a linear bar.

---

## Quick example

```python
import ttkbootstrap as ttk
from tkinter import IntVar

app = ttk.App(title="FloodGauge Demo", theme="cosmo")

progress_var = IntVar(value=45)

gauge = ttk.FloodGauge(
    app,
    bootstyle="warning",
    value=progress_var.get(),
    variable=progress_var,
    mask="Updating: {}%",
    length=300,
    thickness=40,
    orient="horizontal",
)
gauge.pack(padx=16, pady=16, fill="x")

ttk.Button(app, text="Advance", command=lambda: progress_var.set(min(progress_var.get() + 10, 100))).pack(padx=16)

app.mainloop()
```

---

## Modes, masking, and animation

- `mode="determinate"` fills the track based on `value / maximum` and optionally renders `mask` text (e.g., `'Progress: {}%'`); falling back to the `text`/`textvariable` if no mask is supplied.
- `mode="indeterminate"` draws a bouncing pulse instead of a filled region—call `gauge.start()` to begin the animation and `gauge.stop()` to cancel it.
- Use `step(amount)` to increment programmatically (wraps at `maximum`), or let `start()` auto-advance the `value` on a timer.
- `orient="vertical"` flips the bar, and you can alter `length`, `thickness`, `font`, and `mask` on the fly via the widget’s configure delegates.

---

## Bindings & customization

- Pass `variable` and `textvariable` (Tk `IntVar`/`StringVar`) for reactive updates and to observe the gauge via `trace`.
- Replace `bootstyle` mid-flight to change colors; FloodGauge listens to `<<ThemeChanged>>` to redraw surfaces automatically.
- Provide custom `mask` strings, fonts, or even external `StringVar`/`IntVar` objects to keep the control connected to your application state.

---

## When to use FloodGauge

Choose FloodGauge for expressive, animated meters—loaders, resource usage, or time-to-complete indicators—especially when you want more personality than a plain progress bar.

If you just need a straightforward determinate progress indicator, use `Progressbar`; for circular gauges, look at `Meter`.

---

## Related widgets

- `Progressbar` (linear progress)
- `Meter` (circular gauge)
- `Label` (masked text or subtitles)
