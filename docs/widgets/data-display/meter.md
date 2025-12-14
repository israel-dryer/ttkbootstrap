---
title: Meter
icon: fontawesome/solid/gauge-high
---

# Meter

`Meter` displays a value as a circular gauge or arc.

In ttkbootstrap v2, `Meter` is a composite widget built on a `Canvas` that provides:

- **Circular progress display** with full circle or semi-circle (gauge) styles
- **Bootstyle tokens** (`bootstyle="success"`, `bootstyle="danger"`, etc.)
- **Customizable appearance** (size, thickness, segments, wedge indicators)
- **Value text display** with prefix/suffix and subtitle
- **Interactive mode** for user input via click, drag, or keyboard
- **<<Changed>> events** when the value changes

Use `Meter` for dashboard indicators, resource monitors, or any circular progress display.

> _Image placeholder:_
> `![Meter variants](../_img/widgets/meter/overview.png)`
> Suggested shot: full circle + semi-circle + segmented variants.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

meter = ttk.Meter(
    app,
    bootstyle="success",
    value=65,
    maxvalue=100,
    size=200,
)
meter.pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

### `value`, `minvalue`, and `maxvalue`

Set the current value and range.

```python
import ttkbootstrap as ttk

app = ttk.App()

meter = ttk.Meter(
    app,
    value=75,
    minvalue=0,
    maxvalue=100,
    bootstyle="primary",
)
meter.pack(padx=20, pady=20)

app.mainloop()
```

Update the value at runtime:

```python
meter.value = 85
# or
meter.configure(value=85)
```

### `size` and `thickness`

Control the overall size and arc thickness.

```python
# Large meter with thick arc
ttk.Meter(app, size=250, thickness=20, value=60).pack(pady=10)

# Small meter with thin arc
ttk.Meter(app, size=120, thickness=8, value=60).pack(pady=10)
```

### Value formatting

Display the value with custom formatting, prefix, and suffix.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Percentage
ttk.Meter(
    app,
    value=75,
    value_suffix="%",
    value_format="{:.0f}",
).pack(padx=20, pady=10)

# Currency
ttk.Meter(
    app,
    value=1234.56,
    minvalue=0,
    maxvalue=2000,
    value_prefix="$",
    value_format="{:.2f}",
).pack(padx=20, pady=10)

app.mainloop()
```

### Subtitle

Add descriptive text below the value.

```python
ttk.Meter(
    app,
    value=65,
    subtitle="CPU Usage",
    bootstyle="info",
).pack(padx=20, pady=20)
```

---

## Meter types

### Full circle (default)

Displays a complete 360-degree circle.

```python
ttk.Meter(
    app,
    meter_type="full",
    value=70,
    bootstyle="success",
).pack(pady=10)
```

### Semi-circle (gauge)

Displays a 270-degree gauge/speedometer style.

```python
ttk.Meter(
    app,
    meter_type="semi",
    value=70,
    bootstyle="danger",
).pack(pady=10)
```

> _Image placeholder:_
> `![Full vs Semi meter](../_img/widgets/meter/types.png)`

---

## Appearance variants

### Segmented meter

Use `segment_width` to create a segmented appearance.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Meter(
    app,
    value=75,
    segment_width=10,
    bootstyle="warning",
).pack(padx=20, pady=20)

app.mainloop()
```

### Wedge indicator

Use `indicator_width` to show only a wedge/pointer instead of filling the arc.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Meter(
    app,
    value=75,
    indicator_width=20,
    bootstyle="info",
).pack(padx=20, pady=20)

app.mainloop()
```

> _Image placeholder:_
> `![Segmented and wedge meters](../_img/widgets/meter/variants.png)`

---

## Bootstyle variants

Use bootstyle color tokens to change the meter's arc color.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Meter(app, value=50, bootstyle="primary").pack(pady=4)
ttk.Meter(app, value=60, bootstyle="secondary").pack(pady=4)
ttk.Meter(app, value=70, bootstyle="success").pack(pady=4)
ttk.Meter(app, value=80, bootstyle="info").pack(pady=4)
ttk.Meter(app, value=90, bootstyle="warning").pack(pady=4)
ttk.Meter(app, value=95, bootstyle="danger").pack(pady=4)

app.mainloop()
```

> _Image placeholder:_
> `![Meter bootstyles](../_img/widgets/meter/bootstyles.png)`
> (Show meters in all color variants.)

---

## Interactive mode

Enable `interactive=True` to allow users to change the value by clicking, dragging, or using keyboard/mouse wheel.

```python
import ttkbootstrap as ttk

app = ttk.App()

meter = ttk.Meter(
    app,
    value=50,
    interactive=True,
    step_size=5,
    bootstyle="success",
)
meter.pack(padx=20, pady=20)

def on_change(event):
    print(f"Value changed from {event.data['prev_value']} to {event.data['value']}")

meter.on_changed(on_change)

app.mainloop()
```

### `step_size`

Control the increment when using keyboard or mouse wheel in interactive mode.

```python
meter = ttk.Meter(app, interactive=True, step_size=10)  # Changes by 10
```

---

## Custom arc range and offset

Use `arc_range` and `arc_offset` to customize the arc's angular coverage.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Custom 180-degree arc starting at 0 degrees
ttk.Meter(
    app,
    value=50,
    arc_range=180,
    arc_offset=0,
).pack(padx=20, pady=20)

app.mainloop()
```

- `arc_range`: Total arc range in degrees (default: 360 for full, 270 for semi)
- `arc_offset`: Starting angle in degrees (default: -90 for full, 135 for semi)

---

## Hide text

Set `show_text=False` to hide the value display.

```python
ttk.Meter(app, value=75, show_text=False).pack(pady=20)
```

---

## Events

### `on_changed(...)` and `off_changed(...)`

The meter emits a `<<Changed>>` event whenever the value changes. Use `on_changed(...)` to bind a callback.

```python
import ttkbootstrap as ttk

app = ttk.App()

meter = ttk.Meter(app, value=50, interactive=True)
meter.pack(padx=20, pady=20)

def handle_change(event):
    data = event.data
    print(f"Changed from {data['prev_value']} to {data['value']}")

meter.on_changed(handle_change)

app.mainloop()
```

To unbind:

```python
bind_id = meter.on_changed(handle_change)
meter.off_changed(bind_id)
```

The event data includes:
- `value`: New value
- `prev_value`: Previous value

---

## When should I use Meter?

Use `Meter` when:

- displaying circular progress or completion percentage
- creating dashboard gauges (CPU, memory, disk usage)
- showing speedometer-style indicators
- a circular display better communicates the information than a linear bar

Prefer other widgets when:

- **Progressbar** — for linear progress indicators
- **FloodGauge** — for label with integrated progress bar
- **Label** — for simple numeric displays without visual progress

---

## Related widgets

- **Progressbar** — linear progress bar
- **FloodGauge** — label with progress bar
- **Label** — text display