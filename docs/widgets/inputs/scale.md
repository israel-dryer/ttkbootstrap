---
title: Scale
---

# Scale

`Scale` is a primitive themed wrapper around `ttk.Scale`: a draggable thumb
that selects a numeric value from a continuous range. It carries no label,
message, or validation chrome — it is a single value-bearing control built
for gestural adjustment.

The committed value is a `float` between `from_` and `to`, updated live as
the user drags. Reach for `Scale` when relative motion and immediate visual
feedback matter more than typing precision; reach for
[`NumericEntry`](numericentry.md) when the user needs to type exact values
or the field requires form-style validation.

<figure markdown>
![scale](../../assets/dark/widgets-scale.png#only-dark)
![scale](../../assets/light/widgets-scale.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

scale = ttk.Scale(app, from_=0, to=100, value=50)
scale.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

`Scale` exposes a single `float` in `[from_, to]`. The value updates
continuously while the user drags the thumb — there is no separate commit
step. Read or write it through the `value` property:

```python
scale.value = 25
current = scale.value     # always a float
```

Tk clamps assignments to the configured range, so `scale.value = 999` on a
0–100 scale silently becomes `100`. If you need an integer, cast on read
(`int(scale.value)`).

### Signals and variables

`Scale` has the standard ttkbootstrap value bindings:

- `scale.signal` — `Signal[float]` for reactive subscriptions.
- `scale.variable` — Tk variable (`DoubleVar` by default).

Pass your own with `signal=` or `variable=` to share the value across
widgets — this is how [`LabeledScale`](labeledscale.md) keeps its label
text in sync with the thumb.

```python
volume = ttk.Signal(0.5)
ttk.Scale(app, from_=0, to=1, signal=volume).pack(fill="x")
```

---

## Common options

| Option | Purpose |
|---|---|
| `from_` | Minimum value. |
| `to` | Maximum value. |
| `value` | Initial value (default `0`). |
| `orient` | `'horizontal'` (default) or `'vertical'`. |
| `length` | Track length in pixels. |
| `command` | Callback fired with the new value on every change. |
| `signal` / `variable` | External binding for the value. |
| `state` | `'normal'` or `'disabled'`. |
| `accent` | Semantic color token (`primary`, `success`, `danger`, …). |
| `surface` | Optional surface token; otherwise inherited. |
| `takefocus` | Whether the widget participates in focus traversal. |

```python
ttk.Scale(app, from_=0, to=100)                    # primary (default)
ttk.Scale(app, from_=0, to=100, accent="success")
ttk.Scale(app, from_=0, to=1, orient="vertical")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent tokens."

---

## Behavior

### Orientation

Horizontal scales are the default and suit most desktop layouts. Vertical
scales (`orient="vertical"`) read better for level meters, side panels, or
narrow tool areas.

### Range clamping

Tk clamps both user drags and programmatic writes to `[from_, to]`. The
widget never produces a value outside the configured range, so app code
can trust `scale.value` without re-checking bounds.

### Disable and enable

```python
scale.config(state="disabled")
scale.config(state="normal")
```

A disabled scale ignores both pointer drags and `scale.value = ...`-style
writes through the variable.

### Adjusting the range at runtime

```python
scale.config(from_=0, to=10)
```

The current value is re-clamped against the new range on the next update.

---

## Events

Unlike form-style inputs, `Scale` does not expose `on_input` / `on_changed`
helpers. The way to listen for value changes is one of:

**`command` callback** — fires on every change (drag, keyboard, or
`scale.value = ...`). The new value is passed as a string and almost always
wants to be coerced:

```python
def on_change(value):
    print("value:", float(value))

scale = ttk.Scale(app, from_=0, to=100, command=on_change)
```

**`signal.subscribe(...)`** — same firing semantics, but the callback
receives the typed value and the subscription is easy to dispose:

```python
unsub = scale.signal.subscribe(lambda v: print("v:", v))
```

**`<ButtonRelease-1>`** — for "the user has settled on a value," distinct
from "the user is still dragging":

```python
def on_release(event):
    print("final value:", scale.value)

scale.bind("<ButtonRelease-1>", on_release)
```

A common pattern is to use `command` (or `signal.subscribe`) for live
preview and `<ButtonRelease-1>` for a single committed action — for
example, applying an expensive filter only once the drag ends.

---

## Validation and constraints

`Scale`'s `from_` / `to` range is enforced by Tk, so explicit validation
is rarely needed. When it is — for cross-field rules, conditional
enabling, or "the valid range depends on another field" — validate at
the point you read the value (form submit, action handler), or filter
through the `command` callback or signal subscription. To restrict
movement to discrete steps, snap the value yourself:

```python
def snap(value):
    rounded = round(float(value))
    if rounded != int(scale.value):
        scale.value = rounded

scale = ttk.Scale(app, from_=0, to=10, command=snap)
```

---

## When should I use Scale?

Use `Scale` when:

- the input is gestural — volume, zoom, opacity, threshold.
- relative change matters more than typing an exact number.
- live feedback (preview, immediate update) is part of the UX.
- you want a primitive, chrome-free control to compose into a larger layout.

Prefer a different control when:

- the user must type exact values → use [NumericEntry](numericentry.md).
- the field needs form-style validation (required, custom rules) →
  use [NumericEntry](numericentry.md).
- you also want a live label that tracks the thumb → use
  [LabeledScale](labeledscale.md).
- the widget displays progress rather than collects input → use
  [Progressbar](../data-display/progressbar.md) or
  [Meter](../data-display/meter.md).

---

## Related widgets

- [LabeledScale](labeledscale.md) — `Scale` with an integrated value label.
- [NumericEntry](numericentry.md) — keyed numeric input with bounds, stepping, and validation.
- [SpinnerEntry](spinnerentry.md) — entry that steps through values via buttons.
- [Progressbar](../data-display/progressbar.md) — displays progress, not user input.
- [Meter](../data-display/meter.md) — displays proportional values.
- [Entry](../primitives/entry.md) — low-level text input primitive.

---

## Reference

- **API reference:** [`ttkbootstrap.Scale`](../../reference/widgets/Scale.md)
- **Related guides:**
    - [Signals](../../capabilities/signals/signals.md)
    - [Forms](../../guides/forms.md)
