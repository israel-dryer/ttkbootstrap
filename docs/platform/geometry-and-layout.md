# Geometry & Layout

Tk decides where widgets go through **geometry managers**. There are
three: `pack`, `grid`, and `place`. Each one negotiates with the parent
container to allocate space for the children that have been registered
with it. This page covers the three managers, the propagation rules
that govern parent sizing, the timing model (why `winfo_width()` is
zero in a constructor), and what ttkbootstrap adds on top.

For "what container should I reach for in this app?" recipes, see
[Guides → Layout](../guides/layout.md).

---

## The three managers

| Manager | Mental model | When to use |
|---|---|---|
| `pack` | Flow children along an axis (top, bottom, left, right) | Linear strips: toolbars, status bars, single-column stacks |
| `grid` | Place children in a 2-D row/column matrix | Forms, tables, anything where rows and columns must align |
| `place` | Pixel- or fraction-positioned absolute placement | Overlays, badges, drag-drop targets, custom rendering |

Each manager is a separate negotiation protocol. **You may use only
one manager per parent.** Mixing them inside the same container is not
just discouraged; Tk will deadlock the negotiation, leaving widgets at
size zero or in indeterminate positions. (You can use *different*
managers in *sibling* containers — that's fine and common.)

```python
import ttkbootstrap as ttk

app = ttk.App()
toolbar = ttk.Frame(app)
toolbar.pack(side="top", fill="x")          # toolbar uses pack
form = ttk.Frame(app)
form.pack(side="top", fill="both", expand=True)
ttk.Label(form, text="Name").grid(row=0, column=0)   # form uses grid
ttk.Entry(form).grid(row=0, column=1)
```

---

## `pack` mechanics

`pack` fills a parent by laying children along a side. Each call
*allocates* a strip from the remaining cavity and places the child
inside it.

```python
btn.pack(
    side="top",        # "top" | "bottom" | "left" | "right" (default "top")
    fill="x",          # "x" | "y" | "both" | "none" (default "none")
    expand=True,       # share leftover cavity space proportionally
    padx=4, pady=2,    # external padding (around the strip)
    ipadx=0, ipady=0,  # internal padding (inside the widget)
    anchor="w",        # alignment within the strip if it's larger than the child
)
```

Key facts:

- `side` decides *which edge* the strip is taken from — and the
  remaining cavity is what subsequent children see. Children added
  later to `side="top"` end up *below* earlier ones, not above.
- `fill="x"` makes the widget stretch across its strip on the
  cross-axis; `expand=True` makes the strip itself grow into leftover
  cavity space. They're independent — you usually want both for the
  "main content" widget.
- `padx`, `pady` accept either an `int` (symmetric) or a `(left,
  right)` / `(top, bottom)` tuple (asymmetric). ttkbootstrap's
  `PackFrame` injects asymmetric pads to implement `gap=`.

---

## `grid` mechanics

`grid` places children in row/column cells. Cells are created
implicitly when you reference them.

```python
widget.grid(
    row=0, column=0,         # cell coordinates
    rowspan=1, columnspan=2, # span multiple cells
    sticky="nsew",           # which edges the widget hugs (any of n, s, e, w)
    padx=4, pady=2, ipadx=0, ipady=0,
)
```

| `sticky` value | Effect |
|---|---|
| `""` (default) | Widget centered in cell, takes its requested size |
| `"w"` | Glued to west edge; cross-axis still requested size |
| `"ew"` | Stretched horizontally |
| `"ns"` | Stretched vertically |
| `"nsew"` | Stretched both axes (fills the cell) |

For rows and columns to actually expand when the parent grows, you
must give them `weight`:

```python
form.grid_columnconfigure(0, weight=0)   # label column: don't grow
form.grid_columnconfigure(1, weight=1)   # entry column: take all extra
form.grid_rowconfigure(2, weight=1)      # row 2 (the textarea row) takes extra height
```

`weight` is relative — `weight=2` gets twice the share of `weight=1`.
A row or column with no weight (or `weight=0`) stays at its requested
size; only weighted cells absorb leftover space.

`minsize=` (also on `grid_*configure`) sets a floor: the row/column
won't collapse smaller than `minsize`, even if its widgets shrink.

---

## `place` mechanics

`place` positions a child at an absolute or fractional position
inside the parent.

```python
widget.place(
    x=10, y=20,            # absolute pixel offset
    relx=0.5, rely=0.0,    # fractional offset (0..1) of parent dimension
    anchor="n",            # which point of the widget aligns to (x, y)
    width=100, relwidth=0.4,    # mix absolute and fractional sizing
)
```

`place` doesn't negotiate with siblings — it places exactly where you
say. That's both its strength (overlays, drop indicators, draggable
items) and its weakness (no automatic reflow when content changes).

Don't reach for `place` to lay out a normal form or panel. Use it for
the cases where `pack`/`grid` actively get in the way: floating UI on
top of a canvas, custom popovers, snap-to-grid editors.

---

## Geometry propagation

When a parent is asked "how big do you want to be?" it ordinarily
answers with the bounding size of its packed/gridded children. This
is **propagation** — the children's requested sizes flow up to the
parent.

You can turn it off:

```python
frame.pack_propagate(False)   # use frame.grid_propagate(False) for grid containers
frame.configure(width=400, height=300)
```

With propagation off, the frame keeps its configured `width`/`height`
regardless of what's inside. This is how you build a fixed-height
chrome bar that doesn't shrink to fit its content, or a
fixed-aspect-ratio canvas region.

Common gotcha: setting only `width=` (no `height=`) on a frame and
then calling `pack_propagate(False)` produces a zero-height frame —
height defaults to 0, propagation is off, no children to resize from.
Set both, or leave propagation on.

---

## Layout timing

Geometry resolves *during the event loop's idle pass*, not at the
moment of the `pack`/`grid`/`place` call. Two consequences:

- Widget sizes are unreliable in `__init__` and immediately after
  geometry calls. `widget.winfo_width()` returns the last laid-out
  width, which is `1` until layout has run.
- The `<Configure>` virtual event fires after each geometry resolution
  pass, with `event.width` and `event.height` set to the new
  dimensions. This is the right hook for size-dependent code.

Two `winfo` calls answer subtly different questions:

| Call | Returns |
|---|---|
| `widget.winfo_reqwidth()` | What the widget *asked* for, based on its content |
| `widget.winfo_width()` | What the geometry manager *gave* it after laying out |

In a constructor or right after a `grid` call, both are stale. Force
layout with `update_idletasks()` if you must read them synchronously:

```python
frame.pack(fill="both", expand=True)
frame.update_idletasks()
print(frame.winfo_width(), frame.winfo_height())
```

But the cleanest pattern is to bind `<Configure>` and react when
geometry actually settles:

```python
def on_resize(event):
    redraw_canvas(event.width, event.height)

canvas.bind("<Configure>", on_resize)
```

See [Event Loop → `update` vs `update_idletasks`](event-loop.md) for
the broader timing model.

---

## ttkbootstrap layout containers

ttkbootstrap ships two declarative wrappers that absorb the
boilerplate of `pack` and `grid` for the most common layouts:

- `PackFrame` — auto-applies `pack` to children with a configurable
  `direction` (vertical or horizontal) and a `gap` between siblings.
  See [Widgets → PackFrame](../widgets/layout/packframe.md).
- `GridFrame` — auto-flows children into a declared `columns` (or
  `rows`) count, with weight tokens and a `gap` between cells. See
  [Widgets → GridFrame](../widgets/layout/gridframe.md).

```python
import ttkbootstrap as ttk

app = ttk.App()
form = ttk.GridFrame(app, columns=2, gap=8, padding=12)
ttk.Label(form, text="Name").grid()
ttk.Entry(form).grid()
ttk.Label(form, text="Email").grid()
ttk.Entry(form).grid()
form.pack(fill="both", expand=True)
```

Both containers cooperate with `<Configure>` and propagation
correctly, and both are subclasses of `Frame`, so the surface tokens
(`accent`, `surface`, `show_border`, `padding`) work as on any other
container.

---

## Common pitfalls

**Mixing managers in one parent.** Calling `child1.pack(...)` and
`child2.grid(...)` in the same parent deadlocks the negotiation. Pick
one per container.

**Reading size before layout.** `winfo_width()` in a constructor or
immediately after a `grid()` call returns `1`. Bind `<Configure>` or
call `update_idletasks()` first.

**Forgetting `weight`.** Rows and columns without a weight don't
expand when the parent grows — they stay at their natural size and
the extra space pools at the edge of the grid. If your form looks
"stuck" in the top-left after a resize, that's the cause.

**Propagation surprises.** A child packed with `expand=True, fill="x"`
inside a `Frame` that has `pack_propagate(False)` ignores the
propagation hint at the parent level — the child still expands, but
the parent's bounding-box doesn't grow. Read both directions: the
child's request, and what the parent allows.

**`place` in resizable layouts.** A `place`-d child doesn't reflow
when siblings change. Use it for genuine overlays, not as a "skip the
pack/grid figuring" shortcut.

---

## Next steps

- [Widget Lifecycle](widget-lifecycle.md) — when geometry resolves
  during construction, theme change, and destruction.
- [Capabilities → Layout](../capabilities/layout/index.md) — the
  containers, spacing, and scrolling capabilities.
- [Guides → Layout](../guides/layout.md) — how to choose between
  PackFrame, GridFrame, and raw `pack`/`grid`.
- [Guides → Spacing & Alignment](../guides/spacing-and-alignment.md) —
  recommended spacing tokens and visual rhythm.
