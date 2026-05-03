---
title: Meter
---

# Meter

`Meter` is a **PIL-rendered radial gauge** that shows a single numeric
value as an arc — full circle by default, semicircle on demand — with
a large value readout, optional prefix/suffix labels, and an optional
subtitle drawn at the center. Unlike [Progressbar](progressbar.md)
and [FloodGauge](floodgauge.md), which fill a linear track, Meter
is dashboard-shaped: it draws attention to one number.

The arc itself can render four ways — solid sweep (default), a thin
indicator wedge that floats at the current value, a segmented sweep
of evenly spaced ticks, or a wedge over a segmented trough — and the
widget supports an `interactive` mode where the user clicks or drags
across the arc to set the value.

<figure markdown>
![meter](../../assets/dark/widgets-meter.png#only-dark)
![meter](../../assets/light/widgets-meter.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Meter(
    app,
    value=65,
    maxvalue=100,
    subtitle="CPU Usage",
    value_suffix="%",
).pack(padx=20, pady=20)

app.mainloop()
```

For a semicircular gauge:

```python
ttk.Meter(app, value=42, meter_type="semi", value_suffix="°C").pack()
```

---

## Common options

| Option            | Purpose                                                                            |
| ----------------- | ---------------------------------------------------------------------------------- |
| `value`           | Current meter value. Default `0`.                                                  |
| `minvalue`        | Lower bound of the value range. Default `0`.                                       |
| `maxvalue`        | Upper bound of the value range. Default `100`.                                     |
| `dtype`           | `int` (default) or `float`. Sets the variable type and step rounding.              |
| `value_format`    | Format string for the readout. Default `"{:.0f}"`.                                 |
| `value_prefix`    | Small label rendered to the left of the value (`"$"`, `"@"`).                      |
| `value_suffix`    | Small label rendered to the right of the value (`"%"`, `"°C"`).                    |
| `value_font`      | Font for the value text. Default `"-size 36 -weight bold"`.                        |
| `subtitle`        | Caption rendered below the value (or centered when `show_text=False`).             |
| `secondary_font`  | Font for prefix, suffix, and subtitle. Default `"-size 9"`.                        |
| `secondary_style` | Color token for prefix, suffix, and subtitle. Default `"background[muted]"`.       |
| `accent`          | Color token for the indicator and value text. Default `"primary"`.                 |
| `meter_type`      | `"full"` (360°, default) or `"semi"` (270°).                                       |
| `arc_range`       | Total sweep in degrees. Default `360` for full, `270` for semi.                    |
| `arc_offset`      | Starting angle. Default `-90` for full, `135` for semi.                            |
| `size`            | Width and height of the canvas in pixels. Default `200`.                           |
| `thickness`       | Arc stroke width in pixels. Default `10`.                                          |
| `indicator_width` | Width of a wedge-style indicator in degrees. `0` (default) draws a full sweep.     |
| `segment_width`   | Segment size in degrees for a ticked arc. `0` (default) draws a solid arc.         |
| `show_text`       | Whether to render the value readout. Default `True`.                               |
| `interactive`     | Whether mouse clicks/drags on the arc change `value`. Default `False`.             |
| `step_size`       | Rounding increment used in interactive mode. Default `1`.                          |

**Accent and secondary color.** `accent` drives **two** things — the
arc indicator color and the value-readout color. Prefix, suffix, and
subtitle pick up `secondary_style`, which defaults to a muted
background tone so the central number remains the focal point:

```python
ttk.Meter(app, value=72, accent="success", subtitle="Healthy")
ttk.Meter(app, value=12, accent="warning", subtitle="Low")
ttk.Meter(app, value=98, accent="danger", subtitle="Critical")
```

There is no built-in threshold mapping. To re-tint as a value crosses
a level, reconfigure `accent` from your own code (or from an
`on_changed` handler — see Events).

**Indicator shape.** Combine `segment_width` and `indicator_width`
to switch between four visual modes:

| `segment_width` | `indicator_width` | Result                                                       |
| --------------- | ----------------- | ------------------------------------------------------------ |
| `0`             | `0`               | Solid sweep filling from start to current value (default).   |
| `0`             | `> 0`             | A floating wedge of `indicator_width` degrees at the value.  |
| `> 0`           | `0`               | Segmented sweep — evenly spaced ticks up to the value.       |
| `> 0`           | `> 0`             | Wedge over a segmented trough.                               |

```python
ttk.Meter(app, value=60, indicator_width=10)              # floating wedge
ttk.Meter(app, value=60, segment_width=8)                  # segmented sweep
ttk.Meter(app, value=60, segment_width=8, indicator_width=12)  # wedge + ticks
```

**Layout: full vs semi.** `meter_type="semi"` opens the bottom of
the arc. If you need a different sweep, override `arc_range` and
`arc_offset` directly — both accept any integer degree value:

```python
# Quarter gauge starting at 9 o'clock and sweeping up
ttk.Meter(app, arc_offset=180, arc_range=90, value=30)
```

**Static caption only.** Set `show_text=False` to hide the value
readout entirely — Meter then renders just the arc, with the
`subtitle` (if any) drawn dead-center as a label-only dial:

```python
ttk.Meter(app, value=50, show_text=False, subtitle="Load")
```

**Reactive value.** Meter does **not** accept a `signal=` or
`variable=` argument — it owns its internal `IntVar`/`DoubleVar`. To
update the gauge from outside, write through any of the four
equivalent paths:

```python
meter.value = 75              # property
meter.set(75)                 # method
meter.configure(value=75)     # configure
meter.step(5)                 # increment with bounce at limits
```

All four paths fan in to the same variable trace and trigger a
redraw. To observe changes, subscribe to `<<Change>>` (see Events) —
that's the framework's reactive surface for Meter, not a `Signal`
binding.

---

## Behavior

**Value range and dtype.** `dtype=int` (default) routes through an
`IntVar`; `dtype=float` routes through a `DoubleVar`. The default
`value_format="{:.0f}"` shows whole numbers regardless — set
`value_format="{:.2f}"` (or similar) when working with floats:

```python
ttk.Meter(app, value=3.14, dtype=float, value_format="{:.2f}")
```

`dtype` is **construction-only**. Reconfiguring it later emits a
`ConfigurationWarning` and is silently ignored.

**Stepping with bounce.** `step(delta=1)` advances `value` by
`delta`, but unlike a one-way counter, it **bounces** at the
`minvalue` / `maxvalue` boundaries: the internal direction flag flips
and subsequent calls reverse. This is convenient for back-and-forth
demos and oscillating animations, less so for monotonic progress —
for that, write to `value` directly.

```python
meter = ttk.Meter(app, value=0, maxvalue=10)
for _ in range(15):
    meter.step()             # 1, 2, …, 10, then 9, 8, … (bounce)
```

**Interactive mode.** With `interactive=True`, `<Button-1>` and
`<B1-Motion>` on the canvas convert the click position to an angle,
then map that angle through `arc_range` / `arc_offset` and
`step_size` to a new value. Values are clamped to `[minvalue,
maxvalue]`. Useful for input dials; pair with an `on_changed`
listener if you need to react to the drag:

```python
meter = ttk.Meter(app, value=50, interactive=True, step_size=5)
meter.on_changed(lambda e: print("now", e.data["value"]))
```

**Repaint triggers.** The canvas redraws on `<<ThemeChanged>>` and
on `<Configure>` (the widget rebuilds its base trough image and
re-resolves accent/surface colors), and on every write to the
internal value variable. Reconfiguring `size`, `thickness`,
`segment_width`, `arc_range`, `arc_offset`, or `meter_type` rebuilds
the base image as well.

---

## Events

Meter emits a single virtual event:

- `<<Change>>` — fired when `value` changes. `event.data` is
  `{"value": new, "prev_value": old}`.

Use the `on_changed()` / `off_changed()` helpers, or bind directly:

```python
meter = ttk.Meter(app, value=0, maxvalue=100)

def on_change(event):
    v = event.data["value"]
    if v >= 90:
        meter.configure(accent="danger")
    elif v >= 70:
        meter.configure(accent="warning")
    else:
        meter.configure(accent="success")

bind_id = meter.on_changed(on_change)
# meter.off_changed(bind_id)  # to remove later
```

The event fires once per write to the internal variable when the new
value differs from the previous one — duplicate writes (same value
twice) do not re-fire.

---

## When should I use Meter?

Use `Meter` when:

- the value is a **single number** and visual emphasis matters
  (dashboards, status panels, summary cards)
- you want a radial readout — full circle, semicircle, or a custom
  arc — with a large central number
- the user should be able to **drag** to set the value (input dial
  with `interactive=True`)

Prefer:

- [Progressbar](progressbar.md) — when the message is task progress
  along a linear track
- [FloodGauge](floodgauge.md) — when the message is "how full" and
  you want a thicker bar with a label rendered inside the fill
- [Badge](badge.md) — when the status is categorical (`"OK"`,
  `"Failed"`) rather than continuous
- [Scale](../inputs/scale.md) — when you need a standard linear
  slider input rather than a radial dial

---

## Related widgets

- **[Progressbar](progressbar.md)** — slim ttk-based linear progress
  indicator
- **[FloodGauge](floodgauge.md)** — canvas-drawn linear fill with an
  inline label
- **[Badge](badge.md)** — compact, categorical status chip
- **[Scale](../inputs/scale.md)** — linear interactive value input

---

## Reference

- **API reference:** `ttkbootstrap.Meter`
- **Related guides:** [Design System](../../design-system/index.md)
