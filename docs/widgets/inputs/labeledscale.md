---
title: LabeledScale
---

# LabeledScale

`LabeledScale` is a [`Scale`](scale.md) paired with a label that sits
directly above (or below) the thumb and continuously displays the current
value. It is a `Frame` composite — `widget.scale` is the inner
[`Scale`](scale.md), `widget.label` is the value label — and the label's
position tracks the thumb as the user drags.

The committed value is an `int` or a `float` depending on the `dtype`
constructor argument. Reach for `LabeledScale` when users benefit from
seeing the exact value while dragging (volume, opacity, threshold);
prefer plain [`Scale`](scale.md) when no live readout is needed, or
[`NumericEntry`](numericentry.md) when typing precision matters.

<figure markdown>
![labeledscale](../../assets/dark/widgets-labeledscale.png#only-dark)
![labeledscale](../../assets/light/widgets-labeledscale.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

scale = ttk.LabeledScale(app, value=50, minvalue=0, maxvalue=100)
scale.pack(padx=20, pady=20, fill="x")

app.mainloop()
```

---

## Value model

`LabeledScale` exposes a single value within `[minvalue, maxvalue]`. Read
or write it via the `value` property:

```python
scale.value = 75       # programmatic set
current = scale.value  # int or float, matching `dtype`
```

The value updates live as the user drags the thumb (there is no separate
commit step). The label text re-renders on every update.

### Value type — `dtype`

`dtype=int` (the default) coerces values to `int` on every read; the
slider effectively snaps to integer steps. `dtype=float` keeps the value
continuous and is the right choice for ranges like `0.0 – 1.0`. `dtype`
is a construction-time choice — reconfiguring it later raises
`ConfigurationWarning`.

### Range clamping

If a write lands outside `[minvalue, maxvalue]`, the widget restores the
previous value rather than clamping silently — this differs from primitive
[`Scale`](scale.md), where Tk clamps to range. So if your code might
push out-of-range values, call `widget.scale.configure(from_=...,
to=...)` to widen the range first.

### Variables and signals

Pass a `tk.IntVar` or `tk.DoubleVar` via `variable=` to share the value
with another widget. `LabeledScale` does **not** accept a `signal=`
keyword; for reactive subscriptions, reach through to the inner scale:

```python
scale = ttk.LabeledScale(app, value=0, minvalue=0, maxvalue=100)
scale.scale.signal.subscribe(lambda v: print("v:", v))
```

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial value (default `0`). |
| `minvalue` / `maxvalue` | Range. Aliases: `from_` / `to`. Defaults `0` / `100`. |
| `dtype` | `int` (default) or `float`. Construction-time only. |
| `variable` | Tk variable to share the value with other widgets. |
| `compound` | Label position relative to the scale: `'before'` (default, label above) or `'after'` (label below). |
| `accent` | Semantic color token for the inner scale (`primary`, `success`, `danger`, …). |
| Frame kwargs | Any other kwargs (e.g. `padding`, `width`) are forwarded to the underlying `Frame`. Padding is forced to `2`. |

```python
ttk.LabeledScale(app, value=0, minvalue=0, maxvalue=255)             # RGB range
ttk.LabeledScale(app, dtype=float, minvalue=0.0, maxvalue=1.0)       # opacity
ttk.LabeledScale(app, compound="after", accent="success")            # label below, success accent
```

!!! note "Accent applies only to the slider"
    `accent` is forwarded to the inner [`Scale`](scale.md). The label
    inherits default text styling and is not recolored.

!!! link "See [Design System](../../design-system/index.md) for the full set of accent tokens."

---

## Behavior

### Horizontal only

Only horizontal orientation is supported. Passing `orient="vertical"`
raises a `TclError`.

### Label tracking

The label is positioned with `place` so it sits directly over the thumb.
It re-positions on every variable write and on `<Configure>` / `<Map>`
events, which keeps it aligned through window resizes.

### Disable and enable

```python
scale.scale.configure(state="disabled")
scale.scale.configure(state="normal")
```

State is set on the inner scale. The label is a passive readout and is
not state-aware.

### Adjusting the range at runtime

```python
scale.scale.configure(from_=0, to=200)
```

Reconfigure through the inner scale rather than `LabeledScale.configure`
itself.

---

## Events

`LabeledScale` does not expose `on_input` / `on_changed` helpers. To
react to value changes, attach to the inner scale or trace the variable:

```python
# Reactive subscription via the inner scale's signal
scale = ttk.LabeledScale(app, value=0, minvalue=0, maxvalue=100)
scale.scale.signal.subscribe(lambda v: print("live:", v))

# Final value on thumb release
def on_release(event):
    print("final:", scale.value)
scale.scale.bind("<ButtonRelease-1>", on_release)

# Or trace your own variable
import tkinter as tk
var = tk.IntVar(value=50)
scale = ttk.LabeledScale(app, variable=var, minvalue=0, maxvalue=100)
var.trace_add("write", lambda *_: print("var:", var.get()))
```

A common pattern is to use `signal.subscribe` for live preview and
`<ButtonRelease-1>` for a single committed action — for example,
applying an expensive filter only once the drag ends.

---

## Validation and constraints

`LabeledScale`'s range is enforced by the widget itself: writes outside
`[minvalue, maxvalue]` are rejected (the previous value is restored). The
`dtype` choice provides additional implicit validation — `dtype=int`
coerces every value to an integer.

Beyond range and dtype, validation is rarely needed for a slider. When
it is — cross-field rules, conditional enabling — read `widget.value` at
the point of use (form submit, action handler), or filter through the
inner scale's `signal` subscription.

For dynamic ranges, reconfigure the inner scale:

```python
scale.scale.configure(from_=new_min, to=new_max)
```

---

## When should I use LabeledScale?

Use `LabeledScale` when:

- the user benefits from seeing the exact value while dragging.
- a compact slider with built-in readout fits the layout better than a
  separate `Scale` + `Label` pair.
- the value is naturally bounded and gestural (volume, opacity, threshold).

Prefer a different control when:

- a tracking label isn't needed → use [Scale](scale.md).
- the user must type exact values → use [NumericEntry](numericentry.md).
- discrete stepping with up/down buttons fits the UX better → use
  [SpinnerEntry](spinnerentry.md).
- the widget displays progress rather than collects input → use
  [Progressbar](../data-display/progressbar.md) or
  [Meter](../data-display/meter.md).

---

## Related widgets

- [Scale](scale.md) — primitive slider without an integrated label.
- [NumericEntry](numericentry.md) — keyed numeric input with bounds and validation.
- [SpinnerEntry](spinnerentry.md) — entry that steps through values via buttons.
- [Progressbar](../data-display/progressbar.md) — displays progress, not user input.
- [Meter](../data-display/meter.md) — displays proportional values.

---

## Reference

- **API reference:** [`ttkbootstrap.LabeledScale`](../../reference/widgets/LabeledScale.md)
- **Related guides:**
    - [Signals](../../capabilities/signals/signals.md)
    - [Forms](../../guides/forms.md)
