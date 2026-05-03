---
title: ToolTip
---

# ToolTip

`ToolTip` is a **non-blocking hover overlay** that attaches to any
`tkinter` widget and shows a small text popup after a configurable
delay. It's the lightest overlay in the framework — read-only, no
focus, no buttons — used to surface contextual help for icon-only
controls or dense toolbars without permanent labels.

`ToolTip` is **not a widget**. It's a controller object that owns a
chromeless `Toplevel` created on first hover and destroyed when the
pointer leaves. There is no `configure()`/`cget()` surface and no
parent–child relationship to the widget being tooltipped — the
controller installs `<Enter>`/`<Leave>`/`<Motion>`/`<ButtonPress>`
bindings on the target widget and manages the popup from those hooks.

---

## Basic usage

Attach a tooltip to any widget by passing the widget and the text:

```python
import ttkbootstrap as ttk

app = ttk.App()

btn = ttk.Button(app, icon="arrow-clockwise")
btn.pack(padx=20, pady=20)

ttk.ToolTip(btn, text="Reload the current view")

app.mainloop()
```

The instance can be discarded — the constructor's side effect is
the bindings on `btn`. Keep a reference only if you want to call
`destroy()` later.

---

## Lifecycle

A tooltip's life is one hover cycle:

- **Trigger** — `<Enter>` on the target widget schedules `_show_tip`
  via `widget.after(delay, ...)`. The default `delay` is 250 ms.
- **Visibility** — once the timer fires, a `Toplevel` is created
  with `overrideredirect=True`, `windowtype="tooltip"`, and
  `alpha=0.95` (overridable via `**kwargs`). The popup follows the
  mouse via `<Motion>` unless an `anchor_point` was provided.
- **Dismissal** — `<Leave>` or `<ButtonPress>` on the target widget
  cancels the pending show (if any) and destroys the toplevel. The
  controller object survives across cycles; the *toplevel* is
  freshly created each time.
- **Teardown** — `tip.destroy()` cancels any pending show, hides the
  popup, and unbinds the four event handlers from the target widget.
  The target widget itself is left intact.

There's no `show()` / `hide()` method on `ToolTip` — visibility is
fully driven by the pointer. To change text or any other option,
call `tip.destroy()` and construct a new instance:

```python
import ttkbootstrap as ttk

app = ttk.App()
btn = ttk.Button(app, text="Server")
btn.pack(padx=20, pady=20)

tip = ttk.ToolTip(btn, text="connecting…")

def on_connected():
    tip.destroy()
    ttk.ToolTip(btn, text="connected")

app.after(2000, on_connected)
app.mainloop()
```

---

## Common options

| Option | Default | Effect |
|---|---|---|
| `text` | `"widget info"` | Tooltip body. Multi-line strings render as separate lines and wrap at `wraplength`. |
| `delay` | `250` | Milliseconds between `<Enter>` and tooltip appearance. |
| `padding` | `10` | Internal padding (pixels) between text and the tooltip border. |
| `justify` | `"left"` | Multi-line text alignment: `"left"`, `"center"`, `"right"`. |
| `wraplength` | `scale_size(widget, 300)` | Max line width (pixels) before wrapping. DPI-scaled relative to the widget's display. |
| `image` | `None` | A `PhotoImage` (or compatible) shown below the text via `compound="bottom"`. |
| `accent` | `None` (resolves to `"background[+1]"`) | Theme token for the tooltip frame. Pass `"primary"`, `"danger"`, etc. for tinted tooltips. |
| `bootstyle` | `None` | DEPRECATED — use `accent`. |
| `anchor_point` | `None` | If set, anchors the tooltip to a point on the target widget instead of following the mouse. One of `n s e w nw ne sw se center`. |
| `window_point` | `None` (auto-opposite of `anchor_point`) | Which corner of the tooltip aligns with `anchor_point`. Same nine values. |
| `auto_flip` | `True` | Re-anchors offscreen tooltips. `True` / `False` / `"vertical"` / `"horizontal"`. Only relevant when `anchor_point` is set. |
| `**kwargs` | — | Forwarded to the `Toplevel` constructor. `overrideredirect`, `master`, and `windowtype` are set unconditionally. `alpha` defaults to `0.95`. |

The default `accent="background[+1]"` is a "slightly elevated"
surface token that contrasts against the page background by one
step. To match a category (warning hint, error tip), pass a regular
accent:

```python
import ttkbootstrap as ttk

app = ttk.App()

ok = ttk.Button(app, icon="check-lg")
ok.pack(side="left", padx=10, pady=20)
ttk.ToolTip(ok, text="Ready", accent="success")

err = ttk.Button(app, icon="x-lg")
err.pack(side="left", padx=10, pady=20)
ttk.ToolTip(err, text="Connection refused", accent="danger")

app.mainloop()
```

The frame internally uses `variant="tooltip"` (registered in
`style/builders/tooltip.py`), which draws a flat 1-pixel border in
`b.border(accent)`. The variant is not configurable from the
constructor.

---

## Behavior

### Positioning

`ToolTip` has two positioning modes:

- **Mouse-following** (default, when `anchor_point=None`) — the
  popup tracks the cursor with a fixed offset of `+25 px` right
  and `+10 px` down. `WindowPositioning.ensure_on_screen` clamps
  the geometry so the tooltip stays inside the screen with a 5 px
  padding.

- **Anchored** (when `anchor_point` is set) — the popup is pinned
  to the named point on the *target widget* and does not move while
  visible. The nine-point anchor model is the same on both ends:

    ```
    nw  n  ne
     w cen e
    sw  s  se
    ```

    `anchor_point` picks the point on the widget; `window_point`
    picks the matching point on the tooltip. If `window_point` is
    omitted, it defaults to the geometric opposite (`s` ↔ `n`,
    `e` ↔ `w`, etc.) for natural placement.

```python
import ttkbootstrap as ttk

app = ttk.App()

btn = ttk.Button(app, icon="info-circle", variant="text")
btn.pack(padx=80, pady=80)

# Anchored tooltip on the right side of the button, opening rightward.
ttk.ToolTip(btn, text="Click for details", anchor_point="e")

app.mainloop()
```

### Auto-flip

When `anchor_point` is set, `auto_flip` (default `True`) re-anchors
the tooltip across the relevant axis if it would render off-screen.
For a button near the right edge with `anchor_point="e"`, auto-flip
re-anchors to `"w"` so the tooltip opens to the left instead.
Pass `auto_flip="vertical"` (or `"horizontal"`) to constrain the
flip to a single axis; pass `False` to disable flipping entirely.

Auto-flip is meaningful only in anchored mode. In mouse-following
mode the tooltip is always positioned relative to the cursor and
clamped on-screen by translation, not flipping.

### No reconfiguration surface

`ToolTip` does not expose `configure()` / `cget()`, and its public
surface is essentially `__init__` and `destroy`. Mutable state lives
on private attributes (`_text`, `_delay`, etc.) that are read each
time `_show_tip` runs, but there's no supported path to change
them. To swap text, destroy and recreate.

### Pre-existing widget bindings are clobbered

The constructor calls `widget.bind("<Enter>", self._on_enter)`
without `add="+"`, which silently *replaces* any existing
`<Enter>` / `<Leave>` / `<Motion>` / `<ButtonPress>` binding on
the target widget. If your code already binds those events for a
hover effect or click handler, attach the tooltip first and bind
your handlers afterward — or use `bind(..., add="+")` for the
tooltip's own bindings (not currently supported by `ToolTip`).

Attaching a second `ToolTip` to a widget automatically destroys the
first — the new instance replaces the old one cleanly.

### Window flags

Each show creates a `Toplevel` with:

- `overrideredirect=True` — chromeless on Win/Linux. On macOS
  (Aqua), `overrideredirect` is silently skipped per the framework's
  `BaseWindow` guard, so `windowtype="tooltip"` is what produces
  the chromeless effect (Aqua applies `MacWindowStyle "help none"`
  for that windowtype).
- `master=widget` — the toplevel is parented to the target widget,
  so destroying the widget destroys any visible tooltip.
- `alpha=0.95` (default; override via `**kwargs`).

Additional `Toplevel` options can be passed through `**kwargs`
(e.g. `topmost=True`).

---

## Events

ToolTip has *no* virtual events and *no* `on_*` callbacks. It
neither emits nor accepts hooks for show / hide / dismiss.

If you need to know when a tooltip becomes visible — for analytics,
or to cancel a side effect tied to hover — bind to the target
widget's `<Enter>` / `<Leave>` directly *before* attaching the
tooltip (so your handler isn't clobbered):

```python
import ttkbootstrap as ttk

app = ttk.App()
btn = ttk.Button(app, text="Server")
btn.pack(padx=20, pady=20)

# Bind first, then attach the tooltip.
btn.bind("<Enter>", lambda e: print("hovered"))
btn.bind("<Leave>", lambda e: print("left"))
ttk.ToolTip(btn, text="Reload")

app.mainloop()
```

The order matters: the tooltip's bindings would otherwise replace
yours.

---

## When should I use ToolTip?

Use ToolTip when:

- you need a hover-only label for an icon-only control (toolbar
  buttons, badge chips, status indicators)
- the hint text is brief and supplemental — losing it shouldn't
  break the workflow
- the affordance is for sighted users only; screen readers should
  pick up an `aria-label` equivalent (the framework doesn't model
  this directly — set the widget's accessible name on the
  underlying ttk widget if accessibility is in scope)

Prefer Toast when:

- the message is feedback ("Saved", "Copied"), not a hint about
  what a control does
- you need timed dismissal or programmatic display rather than a
  hover trigger

Prefer a Dialog (e.g. `MessageBox.show_info`) when:

- the message demands acknowledgement before the user continues
- the content is more than one short paragraph

Prefer inline help text (a Label below or beside the control) when:

- the hint is essential for completing the task — sighted users
  who skip hovering would be blocked

---

## Related widgets

- **Toast** — non-blocking, programmatically-shown notifications
- **MessageBox** — modal alerts and confirmations
- **Label** — inline help text that's always visible

---

## Reference

- **API reference:** `ttkbootstrap.ToolTip`
- **Related guides:** Feedback, Design System
