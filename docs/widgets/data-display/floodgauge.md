---
title: FloodGauge
icon: fontawesome/solid/water
---

# FloodGauge

`FloodGauge` displays progress with an animated text overlay.

In ttkbootstrap v2, `FloodGauge` is a composite widget built on a `Canvas` that provides:

- **Determinate and indeterminate modes** with smooth animations
- **Text overlay** with customizable format masks
- **Bootstyle tokens** (`bootstyle="success"`, `bootstyle="danger"`, etc.)
- **Horizontal or vertical orientation**
- **Theme-aware colors** that update automatically
- **Variable bindings** for reactive updates

Use `FloodGauge` for visually distinctive progress indicators with text overlays, like upload/download status or loading screens.

> _Image placeholder:_
> `![FloodGauge variants](../_img/widgets/floodgauge/overview.png)`
> Suggested shot: horizontal + vertical + indeterminate variants.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

gauge = ttk.FloodGauge(
    app,
    bootstyle="success",
    value=65,
    mask="{}% Complete",
    length=300,
    thickness=40,
)
gauge.pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

### `value` and `maximum`

Set the current value and maximum for determinate mode.

```python
import ttkbootstrap as ttk

app = ttk.App()

gauge = ttk.FloodGauge(
    app,
    value=75,
    maximum=100,
    bootstyle="primary",
)
gauge.pack(padx=20, pady=20)

app.mainloop()
```

Update the value at runtime:

```python
gauge.configure(value=90)
```

### `orient`, `length`, and `thickness`

Control the orientation and dimensions.

```python
# Horizontal (default)
ttk.FloodGauge(app, orient="horizontal", length=300, thickness=40).pack(pady=10)

# Vertical
ttk.FloodGauge(app, orient="vertical", length=200, thickness=40).pack(pady=10)
```

### Text overlay with `mask`

Use `mask` to format the value as text overlay. Use `{}` as a placeholder for the value.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Percentage
ttk.FloodGauge(
    app,
    value=75,
    mask="{}%",
).pack(fill="x", padx=20, pady=10)

# Custom format
ttk.FloodGauge(
    app,
    value=45,
    maximum=100,
    mask="Progress: {}/100",
).pack(fill="x", padx=20, pady=10)

app.mainloop()
```

### Static `text`

Use `text` for static text that doesn't change with the value.

```python
ttk.FloodGauge(
    app,
    value=50,
    text="Loading...",
).pack(fill="x", padx=20, pady=10)
```

### `font`

Customize the text font.

```python
ttk.FloodGauge(
    app,
    value=60,
    mask="{}%",
    font=("Helvetica", 16, "bold"),
).pack(fill="x", padx=20, pady=10)
```

---

## Determinate vs Indeterminate

### Determinate mode (default)

Shows a filled bar based on the current value.

```python
import ttkbootstrap as ttk

app = ttk.App()

gauge = ttk.FloodGauge(
    app,
    mode="determinate",
    value=0,
    maximum=100,
    mask="{}%",
    bootstyle="info",
)
gauge.pack(fill="x", padx=20, pady=20)

def simulate_work():
    for i in range(101):
        gauge.configure(value=i)
        app.update_idletasks()
        app.after(50)

ttk.Button(app, text="Start", command=simulate_work).pack(pady=10)

app.mainloop()
```

### Indeterminate mode

Shows a bouncing animation for unknown duration tasks.

```python
import ttkbootstrap as ttk

app = ttk.App()

gauge = ttk.FloodGauge(
    app,
    mode="indeterminate",
    text="Processing...",
    bootstyle="warning",
)
gauge.pack(fill="x", padx=20, pady=20)

def toggle():
    gauge.start()

def stop_gauge():
    gauge.stop()

ttk.Button(app, text="Start", command=toggle).pack(side="left", padx=5, pady=10)
ttk.Button(app, text="Stop", command=stop_gauge).pack(side="left", padx=5, pady=10)

app.mainloop()
```

Use `.start()` and `.stop()` to control the animation:

```python
gauge.start()   # Start animation
gauge.stop()    # Stop animation
```

---

## Bootstyle variants

Use bootstyle color tokens to change the gauge's fill color.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.FloodGauge(app, value=40, mask="{}%", bootstyle="primary").pack(fill="x", padx=20, pady=4)
ttk.FloodGauge(app, value=50, mask="{}%", bootstyle="secondary").pack(fill="x", padx=20, pady=4)
ttk.FloodGauge(app, value=60, mask="{}%", bootstyle="success").pack(fill="x", padx=20, pady=4)
ttk.FloodGauge(app, value=70, mask="{}%", bootstyle="info").pack(fill="x", padx=20, pady=4)
ttk.FloodGauge(app, value=80, mask="{}%", bootstyle="warning").pack(fill="x", padx=20, pady=4)
ttk.FloodGauge(app, value=90, mask="{}%", bootstyle="danger").pack(fill="x", padx=20, pady=4)

app.mainloop()
```

> _Image placeholder:_
> `![FloodGauge bootstyles](../_img/widgets/floodgauge/bootstyles.png)`
> (Show floodgauges in all color variants.)

---

## Using variables

Bind the gauge to Tk variables for reactive updates.

```python
import ttkbootstrap as ttk

app = ttk.App()

progress_var = ttk.IntVar(value=0)
text_var = ttk.StringVar(value="Ready")

gauge = ttk.FloodGauge(
    app,
    variable=progress_var,
    textvariable=text_var,
    bootstyle="success",
)
gauge.pack(fill="x", padx=20, pady=20)

def advance():
    current = progress_var.get()
    if current < 100:
        progress_var.set(current + 10)
        text_var.set(f"{current + 10}% Complete")

ttk.Button(app, text="+ 10%", command=advance).pack(pady=10)

app.mainloop()
```

---

## Animation methods

### `start(step_size=None, interval=None)`

Start automatic animation. Behavior depends on mode:

- **Determinate mode**: Auto-increments value at regular intervals
- **Indeterminate mode**: Bouncing pulse animation

```python
# Determinate mode - increment by 2 every 100ms
gauge.configure(mode="determinate")
gauge.start(step_size=2, interval=100)

# Indeterminate mode - bounce animation
gauge.configure(mode="indeterminate")
gauge.start()
```

### `stop()`

Stop the animation.

```python
gauge.stop()
```

### `step(amount=1)`

Manually increment the value by a specific amount.

```python
gauge.step(5)  # Increment by 5
gauge.step()   # Increment by 1 (default)
```

---

## When should I use FloodGauge?

Use `FloodGauge` when:

- you need a progress indicator with text overlay
- you want more visual impact than a standard progress bar
- you need determinate or indeterminate progress with animation
- you're building loading screens or status displays

Prefer other widgets when:

- **Progressbar** — for simple linear progress without text overlay
- **Meter** — for circular/gauge-style progress displays
- **Label** — for static text without progress indication

---

## Related widgets

- **Progressbar** — linear progress bar
- **Meter** — circular gauge
- **Label** — text display