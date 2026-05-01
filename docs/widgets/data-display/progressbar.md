---
title: Progressbar
---

# Progressbar

`Progressbar` is a themed wrapper over `tkinter.ttk.Progressbar` that
shows **how much of a task has completed** (determinate) or **that work
is ongoing** (indeterminate). It's a static, non-interactive indicator
— it doesn't take focus, fire `command`, or emit virtual events, and
it's the right control whenever the message is "how far along".

Determinate mode renders a fill from `0` to `maximum` driven by `value`.
Indeterminate mode runs an animation until `stop()` is called, with no
meaningful value. The widget supports three visual variants
(`default`, `striped`, `thin`) and the standard accent palette, so it
fits in toolbars and dialogs as well as full-width status rows.

<figure markdown>
![progressbar](../../assets/dark/widgets-progressbar.png#only-dark)
![progressbar](../../assets/light/widgets-progressbar.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

pb = ttk.Progressbar(app, maximum=100, value=40)
pb.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

For indeterminate work, switch modes and call `start()`:

```python
pb = ttk.Progressbar(app, mode="indeterminate")
pb.pack(fill="x", padx=20, pady=20)
pb.start()
```

Call `pb.stop()` when the work finishes.

---

## Common options

Progressbar accepts the standard `ttk.Progressbar` options plus the
framework's theming and signal extensions:

| Option          | Purpose                                                                  |
| --------------- | ------------------------------------------------------------------------ |
| `value`         | Current progress as a float (0 to `maximum`).                            |
| `maximum`       | Upper bound of the determinate range. Default `100`.                     |
| `mode`          | `"determinate"` (default) or `"indeterminate"`.                          |
| `orient`        | `"horizontal"` (default) or `"vertical"`.                                |
| `length`        | Requested length along the orientation axis, in pixels.                  |
| `accent`        | Theme color token applied to the fill (`"primary"` by default).          |
| `variant`       | Visual style: `"default"`, `"striped"`, or `"thin"`.                     |
| `surface`       | Surface token used for the trough background (`"content"` by default).   |
| `signal`        | Reactive `Signal` bound to `value`.                                      |
| `variable`      | Tk `DoubleVar` (or compatible) bound to `value`.                         |
| `phase`         | Animation phase for indeterminate mode (rarely set by hand).             |
| `state`         | `"normal"` or `"disabled"` (see Behavior).                               |

**Variant.** `variant` controls the bar silhouette. `default` is a
solid fill, `striped` adds a diagonal hatch (useful for indeterminate
mode), and `thin` collapses both bar and trough to a slim track:

```python
ttk.Progressbar(app, value=40, variant="default")
ttk.Progressbar(app, value=40, variant="striped", accent="info")
ttk.Progressbar(app, value=40, variant="thin")
```

**Accent.** `accent` drives the fill color. Pair it with `variant`
to express both severity and density:

```python
ttk.Progressbar(app, value=80, accent="success")
ttk.Progressbar(app, value=20, accent="warning")
ttk.Progressbar(app, value=10, accent="danger", variant="striped")
```

**Orientation and size.** `orient="vertical"` rotates the bar; `length`
is the requested size along the orientation axis (height for vertical
bars). The cross-axis size is determined by the variant.

```python
ttk.Progressbar(app, orient="vertical", length=200, value=60).pack()
```

**Reactive value.** Bind a `Signal` (or `Variable`) via `signal=` —
**not** `value=` — to keep the bar live without manual `configure()`
calls. The signal's value drives `value` directly:

```python
progress = ttk.Signal(0.0)
pb = ttk.Progressbar(app, signal=progress, maximum=100)
pb.pack(fill="x", padx=20, pady=10)

progress.set(45)  # bar updates automatically
```

After construction, the widget exposes `pb.signal` and `pb.variable`
for the same purpose. Passing `value=signal` does **not** create a
binding — it sets `value` once to the signal's stringified repr.

---

## Behavior

**Determinate mode.** The fill reflects `value / maximum`. Update
`value` directly, via the `value` property, via `configure(value=...)`,
or via the bound signal/variable; all four routes converge on the same
underlying option:

```python
pb.value = 50          # property
pb.set(75)             # method
pb.configure(value=90) # configure
progress.set(100)      # bound signal
```

`step(amount=1.0)` advances `value` by `amount`, wrapping back to `0`
when it would exceed `maximum`. It's convenient for "tick" loops that
don't track an absolute count.

**Indeterminate mode.** `start(interval=50)` schedules a periodic
`step(1.0)` every `interval` milliseconds (default 50 ms). `stop()`
cancels the schedule. The bar's `value` still advances numerically
underneath, but the visual is an animated loop rather than a fill
proportion.

```python
pb.configure(mode="indeterminate")
pb.start()        # default 50 ms tick
pb.stop()
```

The `striped` variant is a common pairing for indeterminate work —
the moving stripes reinforce the "ongoing" feel.

**State.** Through `TtkStateMixin`, Progressbar honors the standard
ttk states. `"disabled"` dims both the bar fill and the trough via
the `disabled` state map. `"active"` and `"readonly"` are accepted
but rarely have a distinct visual.

```python
pb.state(["disabled"])
pb.state(["!disabled"])
```

---

## Events

Progressbar does **not** emit virtual events and does **not** expose
any `on_*` helpers — it's a pure status indicator. To observe value
changes, subscribe to the bound signal:

```python
progress = ttk.Signal(0.0)
pb = ttk.Progressbar(app, signal=progress, maximum=100)

def on_progress(value):
    if value >= 100:
        print("done")

progress.subscribe(on_progress)
```

If you need to know when an indeterminate animation ends, drive
`stop()` from your own code path — there's no completion event.

---

## When should I use Progressbar?

Use `Progressbar` when:

- progress is **linear and quantifiable** (bytes downloaded, files
  processed, tests run)
- you want a compact, neutral indicator that doesn't demand attention
- the work runs in the background and the user just needs a heartbeat

Prefer:

- [Meter](meter.md) — when you want a dashboard-style gauge with a
  central numeric readout
- [Floodgauge](floodgauge.md) — when the message is "how full" and
  you want a label rendered inside the fill
- [Badge](badge.md) — when the status is categorical
  (`"Saved"`, `"Failed"`) rather than continuous

---

## Related widgets

- **[Meter](meter.md)** — radial gauge with a numeric readout
- **[Floodgauge](floodgauge.md)** — capacity indicator with a built-in
  label
- **[Badge](badge.md)** — compact, categorical status chip
- **[Label](label.md)** — pair with a Progressbar for a "Downloading…"
  caption above or beside the bar

---

## Reference

- **API reference:** `ttkbootstrap.Progressbar`
- **Related guides:** [Design System](../../design-system/index.md),
  [Signals](../../capabilities/signals/signals.md)
