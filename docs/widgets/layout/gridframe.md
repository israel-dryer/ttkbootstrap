---
title: GridFrame
---

# GridFrame

`GridFrame` is a `Frame` subclass that auto-applies grid defaults to
its children. You declare row and column sizing, gap spacing, default
sticky, and an auto-placement policy on the container; children call
the standard `grid()` method and inherit those defaults without any
per-call boilerplate.

GridFrame intercepts `grid()`, `grid_forget()`, and `grid_remove()` on
its children, so a plain `Button(form).grid()` flows through container
hooks (`_on_child_grid` and friends) that resolve the next free cell,
inject the default sticky, and inject the inter-cell gap as leading
`padx`/`pady`. As a `Frame` subclass, GridFrame inherits the full
theming surface (`surface`, `show_border`, `input_background`) and the
runtime surface cascade.

<figure markdown>
![gridframe](../../assets/dark/widgets-gridframe.png#only-dark)
![gridframe](../../assets/light/widgets-gridframe.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

grid = ttk.GridFrame(
    app, columns=2, rows=2, gap=10, sticky_items="nsew", padding=20
)
grid.pack(fill="both", expand=True)

ttk.Button(grid, text="Top-Left").grid()
ttk.Button(grid, text="Top-Right").grid()
ttk.Button(grid, text="Bottom-Left").grid()
ttk.Button(grid, text="Bottom-Right").grid()

app.mainloop()
```

Each button's plain `grid()` is intercepted by the GridFrame: cells
are filled in row-major order, every child picks up `sticky="nsew"`,
and a 10-pixel gap is inserted between cells.

---

## Layout model

GridFrame imposes a 2D grid on its children. The container's `rows`
and `columns` parameters describe the track layout; `gap` controls
inter-cell spacing; `auto_flow` controls how widgets without explicit
coordinates are placed; `sticky_items` controls how each child
expands inside its cell.

### Track sizing

`rows` and `columns` accept either a count or a list of size specs:

```python
ttk.GridFrame(app, rows=3, columns=3)            # 3x3, equal weights
ttk.GridFrame(app, columns=[1, 2, 1])            # middle column 2x weight
ttk.GridFrame(app, columns=["auto", 1, "120px"]) # mixed sizing
```

Each spec resolves to a `(weight, minsize)` pair on the underlying
Tk row/column:

| Spec     | Resolved `(weight, minsize)` | Meaning                                                     |
| -------- | ---------------------------- | ----------------------------------------------------------- |
| `int n`  | `(n, 0)`                     | Flex weight; like a CSS `fr`. Extra space splits by weight. |
| `"auto"` | `(0, 0)`                     | No flex, no minimum — track sizes to its content.           |
| `"Npx"`  | `(0, N)`                     | No flex, minimum `N` pixels. **Not** a hard cap — a child can request more. |

Passing an integer instead of a list (`columns=4`) is shorthand for
`[1, 1, 1, 1]` — four equal-weight columns. If you don't pass
`rows`/`columns` at all, the container has no track definitions and
auto-placement falls through to a flat row (see below).

You can also adjust a track after construction:

```python
grid.configure_row(0, weight=2, minsize=40)
grid.configure_column(1, weight=0, minsize=120)
```

`configure_row` and `configure_column` are thin wrappers over
`rowconfigure` / `columnconfigure`.

### Auto-placement and `auto_flow`

When a child calls `grid()` without an explicit `row=` and `column=`,
GridFrame finds the next free cell using the active `auto_flow` mode:

| Mode             | Placement order                                         |
| ---------------- | ------------------------------------------------------- |
| `"row"` (default) | Row-major: fill columns in current row, then next row. |
| `"column"`       | Column-major: fill rows in current column, then next column. |
| `"row-dense"`    | Row-major, but search from `(0, 0)` for the smallest free area on every placement (CSS Grid `dense` semantics). |
| `"column-dense"` | Column-major dense packing.                             |
| `"none"`         | Disable auto-placement — every implicit `grid()` lands at `(0, 0)`. Use only when every child sets `row=` and `column=` explicitly. |

`rowspan`/`columnspan` participate in the search: GridFrame looks for
a rectangular free area of the required size and places the widget at
its top-left corner.

```python
grid = ttk.GridFrame(app, columns=3, gap=8, sticky_items="nsew")
ttk.Button(grid, text="A").grid()                     # row=0 col=0
ttk.Button(grid, text="B").grid()                     # row=0 col=1
ttk.Button(grid, text="C").grid()                     # row=0 col=2
ttk.Button(grid, text="D").grid()                     # row=1 col=0
ttk.Label(grid, text="Wide").grid(columnspan=2)       # row=1 col=1, spans 2
ttk.Label(grid, text="Footer").grid(row=2, columnspan=3)  # explicit
```

The cursor wraps to the next row only when `columns` is defined;
without an explicit column count, the placeholder upper bound is
100, so widgets stack along a single row until you set `columns=`.
Define the track count you want.

### Gap

`gap` is between cells. An integer applies the same value to both
axes; a `(col_gap, row_gap)` tuple sets them independently.

```python
ttk.GridFrame(app, columns=3, gap=10)         # 10px both axes
ttk.GridFrame(app, columns=3, gap=(8, 12))    # 8px between columns, 12px between rows
```

The implementation adds the gap as a **leading** `padx` / `pady` on
every cell after the first column / row. Per-call `padx` / `pady` are
merged with the gap rather than overwritten — gap is added to the
leading edge, the trailing edge stays at the user's value:

```python
grid = ttk.GridFrame(app, columns=3, gap=10)
ttk.Button(grid, text="X").grid(padx=4)   # final padx=(14, 4)
```

### Sticky and overrides

`sticky_items` is the default sticky value applied to every child;
per-call `sticky=` overrides it for a single widget:

```python
grid = ttk.GridFrame(app, columns=2, sticky_items="nsew")
ttk.Entry(grid).grid()                       # sticky="nsew"
ttk.Label(grid, text="Hint").grid(sticky="w")  # overrides
```

Per-call `row=` / `column=` similarly override auto-placement, and
all standard Tk grid options (`rowspan`, `columnspan`, `ipadx`,
`ipady`, `in_`) pass through.

---

## Common options

GridFrame extends Frame's option set with six layout-shaping
parameters:

| Option              | Type                          | Default        | Notes                                                   |
| ------------------- | ----------------------------- | -------------- | ------------------------------------------------------- |
| `rows`              | int \| list \| None           | `None`         | Row count or list of size specs (see Track sizing)      |
| `columns`           | int \| list \| None           | `None`         | Column count or list of size specs                      |
| `gap`               | int \| (int, int)             | `0`            | Inter-cell spacing; tuple is `(col_gap, row_gap)`       |
| `sticky_items`      | str \| None                   | `None`         | Default `sticky` for all children                       |
| `auto_flow`         | str                           | `"row"`        | One of `row`, `column`, `row-dense`, `column-dense`, `none` |
| `propagate`         | bool \| None                  | `None`         | If `False`, calls `grid_propagate(False)`               |
| `padding`           | int \| tuple                  | `0`            | Inner spacing inside the GridFrame                      |
| `width`             | int                           | natural        | Requested width in pixels (see `propagate`)             |
| `height`            | int                           | natural        | Requested height in pixels (see `propagate`)            |
| `surface`           | str                           | `"background"` | Surface token: `chrome`, `content`, `card`, `overlay`, `input` |
| `show_border`       | bool                          | `False`        | Draws a 1px theme-aware border                          |
| `input_background`  | str                           | `"content"`    | Surface token cascaded to input descendants             |
| `accent`            | str                           | —              | Accepted; on container classes the bootstyle wrapper rewrites it as a `surface` override |

Of the GridFrame-specific parameters, only `gap` is wired through
the configure-delegate machinery — `frame.configure(gap=12)` triggers
a full re-grid. The other layout options (`rows`, `columns`,
`sticky_items`, `auto_flow`) are read at construction; change tracks
afterwards via `configure_row` / `configure_column`, and treat
`sticky_items` / `auto_flow` as construction-only defaults.

---

## Behavior

**Grid interception.** GridFrame implements `_on_child_grid`,
`_on_child_grid_forget`, and `_on_child_grid_remove`, the hooks
the framework's `GridMixin` calls on the parent before delegating
to Tk. Any ttkbootstrap widget gridded into a GridFrame flows
through those hooks; raw `tkinter` widgets without `GridMixin`
skip the hooks and use unmanaged grid defaults.

**Method chaining.** `grid()`, `grid_configure()`, `grid_forget()`,
and `grid_remove()` all return `self` (from `GridMixin`), so:

```python
btn = ttk.Button(grid, text="Click").grid()
ttk.Entry(grid).grid(columnspan=2).focus_set()
```

**Reconfiguration.** Calling `grid()` again on a widget that's already
managed updates its options and triggers a full re-grid so the
auto-placement cursor stays consistent. Calling `grid()` with no
arguments on a widget that was previously hidden via `grid_remove()`
restores it to its original cell.

**`grid_remove` vs `grid_forget`.** `grid_remove()` hides the widget
but keeps it tracked, so `grid()` later restores it in place.
`grid_forget()` removes the widget from tracking entirely and frees
its cell — the next `grid()` call treats it as a brand-new child.

**Geometry propagation.** `propagate=False` only calls
`grid_propagate(False)` on the GridFrame itself — the inverse of
PackFrame's `propagate=False`, which calls `pack_propagate`. If you
also pack the GridFrame, set `pack_propagate(False)` separately.

```python
grid = ttk.GridFrame(app, columns=2, width=400, height=300, propagate=False)
grid.pack()
grid.pack_propagate(False)   # honor width/height under pack as well
```

**Surface cascade.** Inherited from Frame: when `surface` (or
`input_background`) is reconfigured at runtime, GridFrame walks its
descendants and re-styles every child that was inheriting from the
old surface. Children with an explicit `surface=` are left alone.

---

## Events

GridFrame has no `on_*` event helpers and emits no virtual events.
Like its parent `Frame`, it participates only in the standard Tk
`<Configure>` notification fired on resize:

```python
def on_resize(event):
    print(event.width, event.height)

grid.bind("<Configure>", on_resize)
```

If you need to react to children entering or leaving the layout,
bind to those widgets directly — the container's add/remove hooks
are private and not intended as a subscription surface.

---

## When should I use GridFrame?

Use `GridFrame` when:

- you want a 2D layout with named row and column tracks
- you want auto-placement with optional spanning
- you want consistent gap spacing between cells without setting
  `padx` / `pady` on every `grid()` call
- you want to set a default `sticky` once on the container instead of
  on every child

Prefer **PackFrame** when you have a single-axis stack and don't
need 2D placement. Prefer **Frame** when you need full manual control
over every child's grid options. Prefer **PanedWindow** when users
need to resize the regions at runtime.

---

## Related widgets

- **Frame** — the parent class; raw container with no managed grid
  defaults
- **PackFrame** — `Frame` subclass with auto-pack of children along
  one axis, plus `gap` spacing
- **LabelFrame** — titled bordered container
- **Card** — opinionated `Frame` preset with `accent='card'` and a
  border
- **PanedWindow** — resizable split regions when users need to
  adjust panel sizes
- **Separator** — visual divider between GridFrame children

---

## Reference

- **API reference:** [`ttkbootstrap.GridFrame`](../../reference/widgets/GridFrame.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
