---
title: Scrollbar
---

# Scrollbar

`Scrollbar` is the themed scrollbar primitive for any widget that
exposes the `xview` / `yview` view-protocol — `Text`, `Canvas`,
`Listbox`, `Treeview`, and the ttkbootstrap composites built on top
of them. It's a thin wrapper over `ttk.Scrollbar` that participates
in the design system: the thumb picks up `accent`, the trough picks
up `surface`, and a `variant` switch toggles between an image-based
*rounded* thumb and a flat *square* thumb.

`Scrollbar` is the building block, not the convenience. For a
scrollable container of arbitrary widgets, reach for
[ScrollView](scrollview.md). For a multi-line text widget that comes
pre-wired, reach for [ScrolledText](../inputs/scrolledtext.md).
Construct `Scrollbar` directly when you're assembling a custom
composite around `Text` or `Canvas` and need explicit control over
which sides scroll and how.

<figure markdown>
![scrollbar](../../assets/dark/widgets-scrollbar.png#only-dark)
![scrollbar](../../assets/light/widgets-scrollbar.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

frame = ttk.Frame(app, padding=12)
frame.pack(fill="both", expand=True)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

text = ttk.Text(frame, wrap="none", width=40, height=10)
text.grid(row=0, column=0, sticky="nsew")

ys = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
ys.grid(row=0, column=1, sticky="ns")

xs = ttk.Scrollbar(frame, orient="horizontal", command=text.xview)
xs.grid(row=1, column=0, sticky="ew")

text.configure(xscrollcommand=xs.set, yscrollcommand=ys.set)

app.mainloop()
```

The wiring is **two-way and symmetric**:

- `command=text.yview` lets the scrollbar drive the target. When the
  user drags the thumb or clicks an arrow, ttk calls
  `text.yview(...)` with the new view fraction.
- `text.configure(yscrollcommand=ys.set)` lets the target drive the
  scrollbar. Whenever the text's view changes — by typing, programmatic
  insert, mouse wheel, keyboard navigation — Tk calls `ys.set(first,
  last)` to update the thumb size and position.

Both halves are required. Wire only `command=` and the user can drag
the thumb but the thumb position never reflects programmatic edits.
Wire only `yscrollcommand=` and the thumb tracks the content but
clicks and drags don't scroll.

---

## Common options

| Option           | Type            | Default            | Notes                                                                  |
| ---------------- | --------------- | ------------------ | ---------------------------------------------------------------------- |
| `orient`         | str             | `"vertical"`       | `"vertical"` or `"horizontal"`; sets the axis and arrow shapes         |
| `command`        | callable        | —                  | Invoked when the user interacts with the bar; pass `target.xview` / `yview` |
| `accent`         | str             | — (border tint)    | Color token for the **thumb**; defaults to the surface's border color  |
| `surface`        | str             | `"content"`        | Surface token for the trough fill                                      |
| `variant`        | str             | `"default"`        | One of `default`, `round`, `rounded`, `square` (see *Variants*)        |
| `style_options`  | dict            | `{}`               | Builder options. The relevant key is `show_arrows: bool` (default `True`) |
| `style`          | str             | resolved at build  | Explicit ttk style; overrides accent/variant/surface                   |
| `takefocus`      | bool            | `0`                | Whether the scrollbar participates in keyboard focus traversal         |
| `cursor`         | str             | platform default   | Cursor shown over the bar                                              |
| `bootstyle`      | str             | —                  | **Deprecated** — use `accent` and `variant`                            |

### Thumb color

```python
ttk.Scrollbar(frame, orient="vertical", accent="primary")
ttk.Scrollbar(frame, orient="vertical", accent="info")
```

`accent` colors the **thumb**, not the trough. Unlike `Frame`,
`LabelFrame`, and `Card` — where `accent` is rerouted to a `surface`
override — `Scrollbar` is not a container, so the accent flows
straight through to the style builder and tints the thumb. The
default thumb color is the surface's border color, which keeps the
bar visible but unobtrusive when no accent is set.

`active` (hover) and `pressed` shades are derived automatically from
the chosen color, so there's nothing to configure for the
interaction states.

### Variants

```python
ttk.Scrollbar(frame, orient="vertical", variant="round")    # default
ttk.Scrollbar(frame, orient="vertical", variant="square")
```

Two visual families are registered:

- `default` (alias `round` / `rounded`) — image-based thumb with
  rounded ends. The trough is drawn flat behind it.
- `square` — flat solid-color thumb that fills the full bar width,
  with theme-aware border drawing.

Any other variant value raises `BootstyleBuilderError` at
construction.

### Hiding arrows

```python
ttk.Scrollbar(frame, orient="vertical", style_options={"show_arrows": False})
```

`show_arrows` is a builder option, not a constructor parameter, so
it goes through `style_options`. Setting it to `False` removes the
two end-arrow elements from the layout, leaving just the trough and
thumb. Useful for compact toolbars or when the surrounding UI
already provides scroll affordances.

### Trough surface

```python
ttk.Scrollbar(frame, orient="vertical", surface="card")
```

`surface` colors the trough background. Set it to match the
container the scrollbar sits inside — by default the trough uses
`content`, which is correct on the app background but stands out
against a `card` or `chrome` parent.

---

## Behavior

**The view protocol.** A scrollbar communicates with its target
through Tk's standard view protocol. The target supports `xview` /
`yview` methods, which accept three command forms (`moveto fraction`,
`scroll N units`, `scroll N pages`). The scrollbar invokes the
appropriate form when the user interacts with it. In the other
direction, the target reports its current view as a `(first, last)`
fraction tuple to whatever callback is registered as
`xscrollcommand` / `yscrollcommand`. `Scrollbar.set(first, last)`
matches that signature exactly, so passing the bound method directly
is the conventional wiring.

**Inherited ttk methods.** All methods on `ttk.Scrollbar` are
available on `Scrollbar`:

- `set(first, last)` — update the thumb position and size; called by
  the target widget, not by your code.
- `get()` — return the current `(first, last)` fraction tuple.
- `delta(deltax, deltay)` — convert a pixel delta to a view fraction
  delta along the scrollbar's axis.
- `fraction(x, y)` — return the view fraction corresponding to a
  point in widget coordinates.
- `identify(x, y)` — return the name of the element under the
  coordinate (`"Scrollbar.thumb"`, `"Scrollbar.trough"`,
  `"Scrollbar.uparrow"`, etc., or `""`).
- `activate(element)` / `state(...)` / `instate(...)` — standard
  ttk state and element-activation hooks.

**Disabled state.**

```python
sb.state(["disabled"])    # greyed out, ignores clicks
sb.state(["!disabled"])   # re-enabled
```

The thumb and arrows render in a muted color when disabled. Targets
keep calling `sb.set(...)` either way — `state` only affects
interaction.

**`orient` is construction-only in practice.** Reconfiguring
`orient` after the widget is built updates the Tk option but does
**not** rebuild the resolved ttk style: a scrollbar created
vertical and then reconfigured to `orient="horizontal"` keeps its
*Vertical* style, with up/down arrows in a horizontal layout. To
change orientation, destroy the scrollbar and create a new one with
the desired orient.

**Don't double-up.** Many widgets auto-show their own scrollbars
when needed (`Text` does this opt-in via `wrap=`, `Treeview` and
`Listbox` need explicit wiring), and the ttkbootstrap composites
[ScrollView](scrollview.md) and [ScrolledText](../inputs/scrolledtext.md)
ship a `Scrollbar` already wired up. Reach for the primitive only
when those don't fit.

---

## Events

`Scrollbar` exposes no `on_*` event helpers and emits no virtual
events. The data flow is one-directional through `command` (user →
target) and `set` (target → scrollbar); both are plain callbacks,
not Tk events. To react to scroll position changes, wrap the
`command` callback or hook the target widget's view protocol
directly.

```python
def on_scroll(*args):
    text.yview(*args)               # delegate first
    print("scrolled to", ys.get())  # then react

ys.configure(command=on_scroll)
```

The standard Tk events are still bound on the widget — `<Configure>`
on resize, `<ButtonPress-1>` / `<ButtonRelease-1>` for raw click
detection, `<Enter>` / `<Leave>` for hover — but they fire on the
scrollbar, not on the target, and they don't carry view-fraction
data. Read `ys.get()` from inside a handler if you need it.

---

## When should I use Scrollbar?

Use `Scrollbar` when:

- you're building a custom composite around `Text`, `Canvas`,
  `Listbox`, or `Treeview` and need explicit control over which
  axes scroll, where the bars sit in the layout, or how they're
  styled
- you have a non-standard scroll target — a custom widget that
  implements the `xview` / `yview` protocol — and need to wire it
  up by hand
- you want a vertical bar without a horizontal one (or vice versa),
  which the auto-scrolling composites don't currently expose

Prefer **ScrollView** when you want a generic scrollable container
for arbitrary widgets — it owns its own scrollbars, the viewport
sizing, and the mouse-wheel wiring. Prefer **ScrolledText** when
the content is a `Text` widget — it ships with a vertical scrollbar
configured by `scrollbar_visibility`. Reach for the bare `Scrollbar`
only when neither composite fits.

---

## Related widgets

- **ScrollView** — scrollable viewport for arbitrary widget content;
  manages its own scrollbars
- **ScrolledText** — `Text` widget bundled with a configurable
  scrollbar
- **Text**, **Canvas**, **Listbox**, **Treeview** — common scroll
  targets that implement the `xview` / `yview` view protocol
- **PanedWindow** — when the goal is *resizing* regions rather than
  *scrolling* within them

---

## Reference

- **API reference:** [`ttkbootstrap.Scrollbar`](../../reference/widgets/Scrollbar.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
