---
title: PanedWindow
---

# PanedWindow

`PanedWindow` is an **interactive split container** that arranges
children in side-by-side or top-and-bottom panes separated by
draggable sashes. The user resizes regions by dragging a sash; the
program controls how extra space is distributed (via per-pane
`weight`) and what initial sizes the panes take (via the children's
own `width` / `height` and propagation flags).

It's a thin themed wrapper over `ttk.Panedwindow`. Unlike `Frame`,
`LabelFrame`, and `Card` — which are purely structural — `PanedWindow`
is interactive: dragging a sash repositions adjacent panes, and the
sash itself takes the `accent` color so it's visible against the
panes' surfaces.

<figure markdown>
![panedwindow](../../assets/dark/widgets-panedwindow.png#only-dark)
![panedwindow](../../assets/light/widgets-panedwindow.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

pw = ttk.PanedWindow(app, orient="horizontal")
pw.pack(fill="both", expand=True)

sidebar = ttk.Frame(pw, padding=12, width=220)
sidebar.pack_propagate(False)
content = ttk.Frame(pw, padding=12)

pw.add(sidebar, weight=0)
pw.add(content, weight=1)

ttk.Label(sidebar, text="Sidebar").pack(anchor="w")
ttk.Label(content, text="Content").pack(anchor="w")

app.mainloop()
```

The two patterns to internalize:

- **Initial sash position** comes from the children's own requested
  size. Set `width=` / `height=` on the child *and* call
  `pack_propagate(False)` (or `grid_propagate(False)`) on it, or the
  child collapses to its content size and the sash sits where the
  content ends.
- **Resize behavior** comes from `weight`. Panes with higher weight
  absorb more of any extra space when the panedwindow itself is
  resized.

---

## Layout model

`PanedWindow` arranges children along one axis: left-to-right when
`orient="horizontal"`, top-to-bottom when `orient="vertical"`. Each
child becomes a *pane*; adjacent panes are separated by a draggable
*sash*. The framework places the sashes; the user moves them.

**Adding panes.** Use `add(child, weight=N)` to append, or
`insert(pos, child, weight=N)` to place at a specific index. The
`pos` argument can be an integer index, the string `"end"`, or the
name of a child already managed by the panedwindow (the existing
child is then displaced and the new one slots in before it).

```python
pw.add(left, weight=0)              # append
pw.add(right, weight=1)
pw.insert(0, header, weight=0)      # prepend
pw.insert("end", footer, weight=0)  # explicit end
```

If `insert` is called with a child that's already a pane, the call
moves the pane to the new position rather than adding a duplicate.

**Removing panes.** `pw.forget(child)` removes the pane and its
sash; the remaining panes redistribute according to their weights.
`pw.panes()` returns the ordered tuple of pane child paths.

**Per-pane options.** ttk.Panedwindow supports exactly one pane
option: `weight`. The `tk.PanedWindow` options `sticky`, `minsize`,
`padx`, `pady`, `height`, and `width` are **not** accepted — passing
them raises `TclError: unknown option`. Sizing constraints have to
go on the pane child itself:

```python
sidebar = ttk.Frame(pw, width=220)
sidebar.pack_propagate(False)       # honor width
pw.add(sidebar, weight=0)
```

**Querying and adjusting.** Read or set a pane's weight after the
fact with `pane(child, "weight")` / `pane(child, weight=N)`. Read or
set sash positions with `sashpos(index)` / `sashpos(index, newpos)`.
Sash indices are zero-based: sash 0 sits between panes 0 and 1.

```python
pw.pane(sidebar, weight=2)          # change weight
print(pw.sashpos(0))                # current sash position
pw.sashpos(0, 280)                  # move sash 0 to x=280 (or y=280)
```

---

## Common options

| Option            | Type           | Default                | Notes                                                        |
| ----------------- | -------------- | ---------------------- | ------------------------------------------------------------ |
| `orient`          | str            | `"horizontal"`         | `"horizontal"` or `"vertical"` — sets the split axis         |
| `padding`         | int \| tuple   | `0`                    | Inner spacing around the panes                               |
| `width`           | int            | natural                | Requested overall width in pixels                            |
| `height`          | int            | natural                | Requested overall height in pixels                           |
| `accent`          | str            | `"border"` (in builder)| Color token for the **sash** (not the surface)               |
| `surface`         | str            | `"content"`            | Background visible behind the sashes                         |
| `style`           | str            | `"TPanedwindow"`       | Explicit ttk style name; overrides accent/surface            |
| `style_options`   | dict           | `{}`                   | Builder options. `sash_thickness` (int, scaled px) is global |
| `bootstyle`       | str            | —                      | **Deprecated** — use `accent` and `variant`                  |

### Sash color

```python
ttk.PanedWindow(app, accent="primary")   # primary-tinted sash
ttk.PanedWindow(app, accent="info")      # info-tinted sash
```

`accent` on `PanedWindow` colors the **sash background**, not the
container's surface. This diverges from `Frame` / `LabelFrame` /
`Card`, where `accent` is rerouted to a `surface` override; for
`PanedWindow`, the accent passes straight through to the style
builder and becomes the sash fill. The default is `"border"`, which
resolves to a theme-appropriate stroke color so the sash is visible
but unobtrusive.

### Sash thickness

```python
ttk.PanedWindow(app, style_options={"sash_thickness": 12})
```

`sash_thickness` is a builder option, not a constructor parameter,
so it goes through `style_options`. It's measured in scaled pixels
and defaults to `6`. Note that ttk's `Sash` element is **global** —
configuring `sash_thickness` on one panedwindow updates the sash
thickness for all panedwindows in the app.

### Surface

```python
ttk.PanedWindow(app, surface="card")
```

`surface` colors the panedwindow's own background. This is mostly
visible inside the `padding` strip and at the edges of the sash; the
panes themselves cover the rest. Set it to match the surrounding
region when the panedwindow is nested inside a tinted container.

---

## Behavior

**Sash drag.** Clicking and dragging a sash repositions it,
constrained between the boundaries of the adjacent panes. The drag
is interactive — pane contents reflow in real time. The sash
respects the `cursor` option, which defaults to a resize cursor
shape on most platforms.

**Weight-based resizing.** When the panedwindow itself is resized,
extra space (or lost space) is distributed across panes in
proportion to their `weight`. A pane with `weight=0` keeps its
current size and absorbs no resize delta; a pane with `weight=2`
absorbs twice as much delta as a pane with `weight=1`.

**No built-in collapse.** ttk.Panedwindow has no expand / collapse
mechanism for panes. To build a collapsible sidebar pattern,
remember the sash position before hiding (`sashpos(0)`), `forget`
the pane, and on re-show `add` (or `insert`) it back and restore
the sash. Or — if hide is rare — set the pane's weight to `0` and
shrink the sash position to the pane's left edge.

**Geometry propagation.** A `PanedWindow` sizes itself to its panes
unless propagation is disabled. Inside a fixed-size parent, set
`width=` and `height=` on the panedwindow and call
`pack_propagate(False)` on the parent (or `grid_propagate(False)` if
you use grid).

**Children are panes, not free widgets.** A child added to a
`PanedWindow` must not be `pack`ed or `grid`ded directly — `add` /
`insert` are the only correct entry points. Mixing `add` with a
direct geometry call on the same child results in undefined
behavior.

---

## Events

`PanedWindow` exposes no `on_*` event helpers and emits no virtual
events. Two raw Tk events are useful in practice:

- `<Configure>` fires on the panedwindow itself when it's resized,
  and on each pane child when its allocation changes (drag or
  parent resize).
- `<ButtonRelease-1>` on the panedwindow fires at the end of a sash
  drag, which is when you'd typically want to persist sash positions
  to a settings store.

```python
def on_sash_release(event):
    if pw.identify(event.x, event.y).startswith("sash"):
        positions = [pw.sashpos(i) for i in range(len(pw.panes()) - 1)]
        save_layout(positions)

pw.bind("<ButtonRelease-1>", on_sash_release)
```

`identify(x, y)` returns the name of the element under a coordinate
(`"sash"`, `""` for an empty area, or the empty string if the point
is outside the widget). It's the way to distinguish a click on a
sash from a click that happened to land in the panedwindow's
padding.

---

## When should I use PanedWindow?

Use `PanedWindow` when:

- the layout has two or three regions whose ideal sizes vary by
  user, by content, or by window size, and you want the user to
  adjust the split without wiring up a custom drag handle
- you're building a workbench-style layout — sidebar + editor,
  navigator + editor + inspector, results pane below an input
- different users will want different proportions and you don't
  want to make the choice for them

Prefer **PackFrame** or **GridFrame** when the proportions should be
program-controlled and not user-adjustable. Prefer **Notebook** when
the regions are *alternative* views rather than *adjacent* ones.
Prefer a fixed `Frame` layout when adjustability would be
distracting (e.g. dialog body, settings page).

Don't reach for `PanedWindow` for collapsible regions —
**Accordion** or **Expander** are the right tools when the binary
"open vs closed" state matters more than continuous resizing.

---

## Related widgets

- **Frame** — non-interactive container; the typical pane content
- **PackFrame**, **GridFrame** — non-interactive layout containers
  for program-controlled splits
- **Notebook** — alternative views (tabbed) instead of adjacent
  panes
- **Accordion**, **Expander** — collapsible sections when "open vs
  closed" is the salient state
- **ScrollView** — pair with a pane when the content overflows
- **Separator** — a static visual divider when no resize behavior
  is wanted

---

## Reference

- **API reference:** [`ttkbootstrap.PanedWindow`](../../reference/widgets/PanedWindow.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
