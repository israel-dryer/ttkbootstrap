---
title: Progressbar
icon: fontawesome/solid/ellipsis-h
---


# Progressbar

`Progressbar` wraps `ttk.Progressbar` with bootstyle tokens, surface colors, and `Signal` integration so you can render determinate or indeterminate progress bars that stay styled with your theme.

---

## Overview

Key `Progressbar` features:

- `mode` supports `determinate` (value between 0 and `maximum`) and `indeterminate` (animated looping).
- `bootstyle`/`surface_color` let the bar match your intent (e.g., `success`, `danger`, `striped`).
- `SignalMixin`/`Signal` support keeps the value reactive and can sync with other widgets.
- `length`, `orient`, `maximum`, `value`, and `phase` remain compatible with the native `ttk` widget.
- `style_options` passes extra tokens like `{"thickness": 12}` to surface customizations.

Use progress bars to communicate task status (downloads, saves, installations, etc.) while keeping the UI cohesive.

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap import Signal

app = ttk.App(title="Progress Demo", theme="cosmo")
progress = Signal(0)

bar = ttk.Progressbar(
    app,
    orient="horizontal",
    length=400,
    value=0,
    maximum=100,
    bootstyle="success",
    signal=progress,
)
bar.pack(padx=16, pady=16, fill="x")

ttk.Button(
    app,
    text="Advance",
    command=lambda: progress.set(min(progress.get() + 10, 100))
).pack(padx=16)

app.mainloop()
```

---

## Determinate vs. indeterminate

- `mode="determinate"` (default) fills the bar proportionally to `value / maximum`; update `value` manually or through a signal when your task reports progress.
- `mode="indeterminate"` disables manual values and runs a looping animation; call `bar.start()`/`bar.stop()` or adjust `phase` for custom pacing.
- `phase` exposes the animation phase for striping or themed motion tracking.
- Bootstyles such as `striped` or `danger` apply to both modes so you can signal intent visually.

---

## Signals & events

- Provide a `Signal` (import from `ttkbootstrap import Signal`) for reactive updates; the signal stays synced with the backing Tk variable via `SignalMixin`.
- Access `bar.variable` if you prefer to rely on Tk variables or `trace`/`subscribe` to react to changes from other controls.
- `Progressbar` respects states like `disabled` and connects seamlessly with your app's event loop.

---

## When to use Progressbar

Choose `Progressbar` for any linear status indicator: downloads, saves, installs, or long-running computations. Pair it with `Label` or `ToolTip` for more context or wrap it in a `Frame` when composing dashboards.

For spinner-like motion, look at `SpinnerEntry` or animated `Toast` notifications instead.

---

## Related widgets

- `Label` (status text)
- `Button` (drive progress)
- `Toast` (completion feedback)
