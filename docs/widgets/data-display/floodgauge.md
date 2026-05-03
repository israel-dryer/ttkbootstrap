---
title: FloodGauge
---

# FloodGauge

`FloodGauge` is a **canvas-drawn progress widget** that renders a fill
from `0` to `maximum` (determinate) or a bouncing pulse animation
(indeterminate). Unlike [Progressbar](progressbar.md), which wraps
`tkinter.ttk.Progressbar`, FloodGauge is a `tkinter.Canvas` subclass
with full control over color, thickness, orientation, and a built-in
text overlay rendered inside the fill.

The text overlay is what makes FloodGauge distinct: a static `text`
label, or a `mask` format string like `"Disk: {}%"` that interpolates
the current value as the bar advances. The widget is non-interactive —
it doesn't take focus, fire `command`, or emit virtual events. Update
it by writing to its bound `variable` (or via `set()` / `configure()`).

<figure markdown>
![floodgauge](../../assets/dark/widgets-floodgauge.png#only-dark)
![floodgauge](../../assets/light/widgets-floodgauge.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

fg = ttk.FloodGauge(app, value=65, mask="Disk: {}%")
fg.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

For an indeterminate pulse, switch modes and call `start()`:

```python
fg = ttk.FloodGauge(app, mode="indeterminate", text="Working…")
fg.pack(fill="x", padx=20, pady=20)
fg.start()
```

Call `fg.stop()` when the work finishes.

---

## Common options

FloodGauge accepts the canvas-drawn progress options below. Unlike
[Progressbar](progressbar.md), it is **not** a ttk widget — there is
no `style`, no `state`, and no `signal=` parameter; reactivity is
through the standard Tk `variable` / `textvariable` bindings.

| Option          | Purpose                                                                  |
| --------------- | ------------------------------------------------------------------------ |
| `value`         | Current progress as an integer (`0` to `maximum`). Default `0`.          |
| `maximum`       | Upper bound of the determinate range. Default `100`.                     |
| `mode`          | `"determinate"` (default) or `"indeterminate"`.                          |
| `mask`          | Format string with `"{}"` for the value, e.g. `"Loaded {}%"`.            |
| `text`          | Static label shown when `mask` is not set.                               |
| `font`          | Font for the text overlay. Default `("Helvetica", 12)`.                  |
| `accent`        | Fill color token. Default `"primary"`. Trough is the subtle border tint. |
| `orient`        | `"horizontal"` (default) or `"vertical"`.                                |
| `length`        | Main-axis size in pixels. Default `200`.                                 |
| `thickness`     | Cross-axis size in pixels. Default `50`.                                 |
| `increment`     | Step size used by `step()` and the auto-advance in `start()`.            |
| `variable`      | `tkinter.IntVar` bound to `value`.                                       |
| `textvariable`  | `tkinter.StringVar` bound to `text`. Overwritten when `mask` is active.  |

**Accent.** `accent` drives the fill color; the trough is the
matching subtle/border tint, and the text overlay automatically picks
the readable contrast color (`b.on_color(accent)` from the active
theme). You don't set foreground manually:

```python
ttk.FloodGauge(app, value=80, accent="success", mask="{}%")
ttk.FloodGauge(app, value=20, accent="warning", mask="{}%")
ttk.FloodGauge(app, value=10, accent="danger", mask="{}%")
```

To re-tint as thresholds are crossed, reconfigure `accent` from your
own code — there is no built-in threshold mapping:

```python
def update(level):
    accent = "success" if level < 70 else "warning" if level < 90 else "danger"
    fg.configure(value=level, accent=accent)
```

**Mask vs text.** When `mask` is set, the text overlay is
`mask.format(int(value))` and the underlying `textvariable` is
re-written on every redraw. When `mask` is `None`, the overlay is the
static `text` (or whatever string is in `textvariable`). Use `mask`
when the label should track the value; use `text` for a fixed caption
like `"Working…"` during indeterminate animation.

```python
ttk.FloodGauge(app, value=42, mask="{} of 100")          # tracks value
ttk.FloodGauge(app, value=0, text="Loading…")             # static label
ttk.FloodGauge(app, mode="indeterminate", text="Working…")
```

**Orientation and size.** `orient="vertical"` rotates the bar; the
fill rises from the bottom edge. `length` is the requested size along
the orientation axis (height when vertical), `thickness` is the
cross-axis size. Both are honored on construction; the widget then
tracks geometry-manager dimensions on `<Configure>`.

```python
ttk.FloodGauge(app, orient="vertical", length=200, thickness=40, value=60).pack()
```

**Reactive value.** Pass an `IntVar` (or hand the widget's own
`fg.variable`) and write to it; the canvas redraws on every variable
trace:

```python
import tkinter as tk

level = tk.IntVar(value=25)
fg = ttk.FloodGauge(app, variable=level, mask="{}%")
fg.pack(fill="x", padx=20, pady=10)

level.set(90)  # gauge updates automatically
```

The same applies to `textvariable` for bound captions. Note that
`mask` writes back into `textvariable` on each redraw, so don't pair
the two on a single value-tracking gauge.

---

## Behavior

**Determinate mode.** The fill reflects `value / maximum`. Update
`value` directly, via the `value` property, via `configure(value=...)`,
or by writing to the bound `IntVar`; all four routes converge through
the same variable trace:

```python
fg.value = 50          # property
fg.set(75)             # method
fg.configure(value=90) # configure
fg.variable.set(100)   # bound IntVar
```

`step(amount=1)` advances the value by `amount`, wrapping back to `0`
when it would exceed `maximum` (the wrap is `(value + amount) %
(maximum + 1)`). This is convenient for tick loops where the absolute
count is uninteresting.

**Indeterminate mode.** A pulse roughly 20% of the bar's main-axis
size bounces back and forth across the trough. `start(step_size=8,
interval=20)` schedules the animation; `stop()` cancels it. Defaults
are 8 px / 20 ms in indeterminate mode. The text overlay (static
`text` only — `mask` interpolation isn't meaningful here) stays
centered.

```python
fg.configure(mode="indeterminate")
fg.start()             # default 20 ms tick, step 8 px
fg.stop()
```

**`start()` in determinate mode.** Calling `start()` while in
determinate mode auto-advances `value` by `increment` every tick
(default 1 / 50 ms). The bar fills, wraps via `step()`, and continues
indefinitely until `stop()` is called. This is a demo/animation
convenience — for real progress, write to `value` from your own
update loop.

**Repaint triggers.** The canvas redraws on `<Configure>` (resize),
on `<<ThemeChanged>>` (theme switch — the bar refreshes its colors
through the active theme's accent/border palette), and on every
write to `variable` / `textvariable`. There is no manual `redraw()`
call to make.

---

## Events

FloodGauge does **not** emit virtual events and does **not** expose
any `on_*` helpers — it's a pure status indicator. To observe value
changes, trace the bound variable yourself:

```python
import tkinter as tk

level = tk.IntVar(value=0)
fg = ttk.FloodGauge(app, variable=level, mask="{}%")

def on_change(*_):
    if level.get() >= 100:
        print("done")
        fg.stop()

level.trace_add("write", on_change)
```

If you need to know when an indeterminate animation ends, drive
`stop()` from your own code path — there's no completion event.

---

## When should I use FloodGauge?

Use `FloodGauge` when:

- the message is **"how full"** (capacity, utilization, threshold)
- you want a label rendered **inside** the fill (`"Disk: 78%"`,
  `"42 of 100"`)
- you want a thicker, more prominent indicator than the slim
  `Progressbar` track
- you need fine control over orientation, thickness, and font

Prefer:

- [Progressbar](progressbar.md) — when the message is task progress
  and you want the standard ttk-themed bar with a `striped` /
  `thin` variant
- [Meter](meter.md) — when you want a dashboard-style radial gauge
  with a central numeric readout
- [Badge](badge.md) — when the status is categorical (`"Saved"`,
  `"Failed"`) rather than continuous

---

## Related widgets

- **[Progressbar](progressbar.md)** — slim ttk-based linear progress
  indicator
- **[Meter](meter.md)** — radial gauge with a numeric readout
- **[Badge](badge.md)** — compact, categorical status chip
- **[Label](label.md)** — pair with a FloodGauge for an external
  caption when you don't want the value text rendered inside the fill

---

## Reference

- **API reference:** `ttkbootstrap.FloodGauge`
- **Related guides:** [Design System](../../design-system/index.md)
