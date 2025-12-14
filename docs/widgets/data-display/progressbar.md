---
title: Progressbar
icon: fontawesome/solid/bars-progress
---

# Progressbar

`Progressbar` shows the progress of a task.

In ttkbootstrap v2, `Progressbar` is a wrapper around Tkinter's `ttk.Progressbar` that keeps the familiar API but adds a few "app-ready" conveniences:

- **Bootstyle tokens** (`bootstyle="success"`, `bootstyle="danger-striped"`, etc.)
- **Striped variant** via `bootstyle="striped"` or `bootstyle="success-striped"`
- Optional **reactive binding** with `signal=...`
- **Surface-aware** styling via `surface_color=...` (or inherit from the parent surface)

> _Image placeholder:_
> `![Progressbar variants](../_img/widgets/progressbar/overview.png)`
> Suggested shot: determinate + indeterminate + striped variants.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

progress = ttk.Progressbar(
    app,
    orient="horizontal",
    length=300,
    mode="determinate",
    maximum=100,
    value=50,
    bootstyle="success",
)
progress.pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

### `value` and `maximum`

For determinate mode, set the current value and maximum.

```python
import ttkbootstrap as ttk

app = ttk.App()

progress = ttk.Progressbar(app, mode="determinate", maximum=100, value=75)
progress.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

Update the value at runtime:

```python
progress["value"] = 90
# or
progress.configure(value=90)
```

### `orient` and `length`

```python
# Horizontal (default)
ttk.Progressbar(app, orient="horizontal", length=300).pack(pady=10)

# Vertical
ttk.Progressbar(app, orient="vertical", length=200).pack(pady=10)
```

### Using a variable

Sync the progressbar with a Tk variable.

```python
import ttkbootstrap as ttk

app = ttk.App()

progress_var = ttk.IntVar(value=0)

bar = ttk.Progressbar(app, variable=progress_var, maximum=100)
bar.pack(fill="x", padx=20, pady=20)

def increment():
    current = progress_var.get()
    if current < 100:
        progress_var.set(current + 10)

ttk.Button(app, text="+ 10%", command=increment).pack(pady=10)

app.mainloop()
```

---

## Determinate vs Indeterminate

### Determinate mode

Shows a specific percentage complete. Update `value` as the task progresses.

```python
import ttkbootstrap as ttk

app = ttk.App()

progress = ttk.Progressbar(
    app,
    mode="determinate",
    maximum=100,
    value=0,
    bootstyle="primary",
)
progress.pack(fill="x", padx=20, pady=20)

def simulate_work():
    for i in range(101):
        progress["value"] = i
        app.update_idletasks()
        app.after(50)

ttk.Button(app, text="Start", command=simulate_work).pack(pady=10)

app.mainloop()
```

### Indeterminate mode

Shows an animated loop when progress can't be determined.

```python
import ttkbootstrap as ttk

app = ttk.App()

progress = ttk.Progressbar(app, mode="indeterminate", bootstyle="info")
progress.pack(fill="x", padx=20, pady=20)

def toggle():
    if progress.cget("mode") == "indeterminate":
        progress.start()
    else:
        progress.stop()

ttk.Button(app, text="Start/Stop", command=toggle).pack(pady=10)

app.mainloop()
```

Use `.start()` and `.stop()` to control the animation:

```python
progress.start()   # Start animation
progress.stop()    # Stop animation
```

---

## Bootstyle variants

### Color tokens

Use color tokens to indicate task status or intent.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Progressbar(app, value=40, bootstyle="primary").pack(fill="x", padx=20, pady=4)
ttk.Progressbar(app, value=50, bootstyle="secondary").pack(fill="x", padx=20, pady=4)
ttk.Progressbar(app, value=60, bootstyle="success").pack(fill="x", padx=20, pady=4)
ttk.Progressbar(app, value=70, bootstyle="info").pack(fill="x", padx=20, pady=4)
ttk.Progressbar(app, value=80, bootstyle="warning").pack(fill="x", padx=20, pady=4)
ttk.Progressbar(app, value=90, bootstyle="danger").pack(fill="x", padx=20, pady=4)

app.mainloop()
```

> _Image placeholder:_
> `![Progressbar bootstyles](../_img/widgets/progressbar/bootstyles.png)`
> (Show progressbars in all color variants.)

### Striped variant

Add `-striped` to any bootstyle for a striped appearance.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Progressbar(app, value=50, bootstyle="primary-striped").pack(fill="x", padx=20, pady=4)
ttk.Progressbar(app, value=60, bootstyle="success-striped").pack(fill="x", padx=20, pady=4)
ttk.Progressbar(app, value=70, bootstyle="danger-striped").pack(fill="x", padx=20, pady=4)

app.mainloop()
```

Or use `striped` alone for the default color:

```python
ttk.Progressbar(app, value=75, bootstyle="striped").pack(fill="x", padx=20, pady=4)
```

> _Image placeholder:_
> `![Striped progressbars](../_img/widgets/progressbar/striped.png)`

---

## Signals

If your v2 app uses signals, you can bind the progressbar value to a `signal=` so changes flow through your app state.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
progress = ttk.Signal(0)  # pseudo-code

bar = ttk.Progressbar(
    app,
    signal=progress,
    maximum=100,
    bootstyle="success",
)
bar.pack(fill="x", padx=20, pady=20)

def advance():
    current = progress.get()
    if current < 100:
        progress.set(current + 10)

ttk.Button(app, text="+ 10%", command=advance).pack(pady=10)

app.mainloop()
```

---

## When should I use Progressbar?

Use `Progressbar` when:

- showing download, upload, or file operation progress
- displaying the progress of a long-running task
- indicating that work is being done (indeterminate mode)
- you need a linear status indicator

Prefer other widgets when:

- **Meter** — for gauges or circular progress displays
- **Label** — for simple text status updates
- **Toast** — for completion notifications

---

## Related widgets

- **Meter** — circular/gauge-style progress
- **Label** — text status display
- **FloodGauge** — label with integrated progress bar