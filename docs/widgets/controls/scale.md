---
title: Scale
icon: fontawesome/solid/sliders
---

# Scale

`Scale` lets users choose a numeric value by dragging a thumb along a track.

In ttkbootstrap, `Scale` is still the familiar ttk widget, but it’s designed to *fit the rest of the v2 ecosystem*:

- Works with a Tk variable (`variable=...`) **and/or** a reactive signal (`signal=...`)
- Uses **Bootstyle tokens** via `bootstyle="primary"`, `bootstyle="success"`, etc.
- Respects surface colors (`surface_color=...`) so it blends into elevated / inherited backgrounds

> **Screenshot placeholder:**  
> `![Scale examples](../_img/widgets/scale/overview.png)`  
> (Show horizontal + vertical scales, plus a labeled value readout.)

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

value = ttk.DoubleVar(value=50)

scale = ttk.Scale(
    app,
    from_=0,
    to=100,
    variable=value,
    bootstyle="primary",
)
scale.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## Common options

### Range and initial value
- `from_`: start of the range (float)
- `to`: end of the range (float)
- `variable`: a `DoubleVar` or `IntVar` to store the value
- `value`: (when supported in your wrapper) an initial value you want reflected in the widget

```python
value = ttk.DoubleVar(value=0)

ttk.Scale(app, from_=-1, to=1, variable=value).pack(fill="x")
```

### Orientation

```python
ttk.Scale(app, from_=0, to=10, orient="horizontal").pack(fill="x")
ttk.Scale(app, from_=0, to=10, orient="vertical").pack(fill="y")
```

> **Screenshot placeholder:**  
> `![Vertical scale](../_img/widgets/scale/vertical.png)`

### Length

`length` controls the pixel length of the control (especially useful for vertical scales).

```python
ttk.Scale(app, from_=0, to=100, orient="vertical", length=240).pack(padx=20, pady=20)
```

### Command callback

`command=` is called as the thumb moves. Ttk passes the value as a **string**, so convert it if you need a number.

```python
def on_change(raw: str) -> None:
    v = float(raw)
    print("value:", v)

ttk.Scale(app, from_=0, to=1, command=on_change).pack(fill="x", padx=20, pady=10)
```

If you already use `variable=...`, a common pattern is to read from the variable inside the callback.

---

## Styling with Bootstyle

A `Scale` accepts `bootstyle` like other widgets.

```python
ttk.Scale(app, from_=0, to=100, bootstyle="primary").pack(fill="x", pady=6)
ttk.Scale(app, from_=0, to=100, bootstyle="success").pack(fill="x", pady=6)
ttk.Scale(app, from_=0, to=100, bootstyle="danger").pack(fill="x", pady=6)
```

> **Screenshot placeholder:**  
> `![Scale bootstyles](../_img/widgets/scale/bootstyles.png)`  
> (Show the same scale in several colors.)

### Surface-aware backgrounds

If your UI uses elevated surfaces (frames with inherited surface tokens), you can pin the scale to a surface token:

```python
ttk.Scale(
    app,
    from_=0,
    to=100,
    bootstyle="primary",
    surface_color="background[+1]",
).pack(fill="x", padx=20, pady=20)
```

---

## Showing the value next to the Scale

A common desktop pattern is “slider + live value readout”.

```python
import ttkbootstrap as ttk

app = ttk.App()

value = ttk.DoubleVar(value=25)

row = ttk.Frame(app, padding=20)
row.pack(fill="x")

scale = ttk.Scale(row, from_=0, to=100, variable=value, bootstyle="primary")
scale.pack(side="left", fill="x", expand=True)

label = ttk.Label(row, textvariable=value, width=6, anchor="e")
label.pack(side="left", padx=(10, 0))

app.mainloop()
```


!!! tip "Formatting percent, currency, etc..." 
    Render the label yourself in a callback instead of using `textvariable` directly.

---

## Signals

If you use the v2 reactive layer, `Scale` can be bound to a `signal=` so changes flow through your app state.

```python
import ttkbootstrap as ttk

app = ttk.App()

# Example only — use your real signal creation API
volume = ttk.Signal(50)  # pseudo-code

ttk.Scale(app, from_=0, to=100, signal=volume, bootstyle="info").pack(fill="x", padx=20, pady=20)

volume.subscribe(lambda v: print("volume changed:", v))

app.mainloop()
```

!!! note "Keep `variable=` and `signal=` consistent." 
    In most apps you pick one source of truth (signals for reactive apps, variables for simple forms).

---

## When should I use Scale?

Use `Scale` when:

- the value is naturally continuous (volume, brightness, thresholds)
- users benefit from *relative* adjustment instead of typing exact numbers

Prefer a numeric input (like `NumericEntry` / `SpinnerEntry`) when:

- users must enter precise values
- you need formatting, units, or validation messages

---

## Related widgets

- **SpinnerEntry** — precise numeric adjustment with step controls
- **NumericEntry** — formatted numeric input with validation
- **LabeledScale** — scale with a built-in label/value presentation (if you prefer the composite widget)
