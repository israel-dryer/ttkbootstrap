---
title: Meter
icon: fontawesome/solid/gauge-high
---


# Meter

`Meter` displays a value as a circular arc, pairing `bootstyle` colors with optional text, prefix/suffix labels, and subtitle decorations. It is great for dashboards, resource monitors, or any place you want a compact, animated progress indicator instead of a linear bar.

---

## Overview

Key capabilities:

- Handles both `meter_type="full"` (complete circle) and `"semi"` (gauge) layouts with automatic arc sizing.
- Supports solid arcs, segmented strips (`segment_width`), or wedge-style indicators (`indicator_width`), plus custom `thickness` and `size`.
- Formats value text with `value_format`, optional `value_prefix`/`value_suffix`, and separate fonts/styles for secondary text.
- Optional `interactive=True` turns the meter into a draggable control that emits `<<Changed>>` on value updates (tap/drag/keyboard stepping via `step_size`).
- Bootstyle colors, `surface_color`, and `value` range (`minvalue`, `maxvalue`) stay synced through the canvas-based renderer.

Use `Meter` whenever a circular visual better expresses progress, capacity, or completion than a straight bar.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(title="Meter Demo", theme="cosmo")

meter = ttk.Meter(
    app,
    bootstyle="success",
    value=65,
    maxvalue=100,
    size=220,
    thickness=16,
    meter_type="semi",
    subtitle="Completion",
    value_suffix="%",
)
meter.pack(padx=24, pady=24)

app.mainloop()
```

---

## Appearance & interaction

- Use `meter_type` plus `arc_range`/`arc_offset` to switch between full circles, gauges, or custom arcs.
- Adjust `segment_width` to render striping, and `indicator_width` to show a wedge pointer instead of a filled arc.
- `value_format`, `value_prefix`, and `value_suffix` control how the numeric label renders, while `value_font` and `secondary_font` customize typography.
- Enable `interactive=True` to let users tap or drag inside the meter to adjust the value; use `step_size` to control keyboard and mouse wheel increments.
- Bind to `<<Changed>>` on the widget to react to both user and programmatic updates (event data includes `value` and `prev_value`).

---

## When to use Meter

Choose `Meter` for circular dashboard indicators, speedometer-style widgets, or status chips that benefit from a round motion cue. Pair it with labels, icons, or `Toast` notifications when you need more context.

For linear progress or determinate tracking without a gauge, fall back to `Progressbar`.

---

## Related widgets

- `Progressbar` (linear progress)
- `Label` (value/subtitle text)
- `Toast` (completion feedback)
