---
title: Layout
---

# Layout

This guide covers how to organize widgets on screen — grouping, spacing, alignment, and resizing — using ttkbootstrap's three layout primitives.

ttkbootstrap takes an opinionated approach to layout. Rather than tuning low-level geometry options on every widget, you compose **purpose-built containers** that capture layout intent in their constructor.

---

## The three layout primitives

| Container    | Geometry | Use it when                                                     |
| ------------ | -------- | --------------------------------------------------------------- |
| `Frame`      | any      | you want a plain container and will manage geometry yourself    |
| `PackFrame`  | `pack`   | content flows in one direction (vertical stack, horizontal bar) |
| `GridFrame`  | `grid`   | content needs to align across rows and columns                  |

`PackFrame` and `GridFrame` are thin layers over Tk's `pack` and `grid`. They:

- apply container-level defaults (gap, sticky, fill) so children call `pack()` / `grid()` without arguments
- handle row/column wrapping (auto-placement) for grid
- keep spacing rules in **one place** — the container — instead of scattered across each child

You can always fall back to `Frame` and call `pack()` / `grid()` directly. Do that when you're porting Tk code, debugging a layout, or your geometry is too custom for the helpers.

---

## Frame: plain container

`Frame` is the unstyled, geometry-agnostic container. It accepts any geometry manager and adds nothing on top of `ttk.Frame` except the design-system styling tokens (`accent`, `surface`, `show_border`, `padding`).

```python
import ttkbootstrap as ttk

app = ttk.App()

frame = ttk.Frame(app, padding=12)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Name").grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(frame).grid(row=0, column=1, sticky="ew", padx=8, pady=4)
frame.columnconfigure(1, weight=1)

app.mainloop()
```

This is the pattern any Tk tutorial would teach. It works, but every child carries its own `padx`/`pady`/`sticky` and the column weight is set on the container by hand. The next two sections show how `PackFrame` and `GridFrame` collapse that boilerplate.

!!! link "See the [Spacing & Alignment](spacing-and-alignment.md) guide for the underlying `pack` / `grid` mental model."

---

## PackFrame: linear layout

`PackFrame` is the right choice when content flows in **one direction** — a vertical form, a horizontal toolbar, a sidebar, a button row.

You declare the direction and spacing once on the container, then call `pack()` on children with no arguments.

```python
import ttkbootstrap as ttk

app = ttk.App()

form = ttk.PackFrame(app, direction="vertical", gap=8, padding=12)
form.pack(fill="both", expand=True)

ttk.Label(form, text="Username").pack()
ttk.Entry(form).pack()
ttk.Label(form, text="Password").pack()
ttk.Entry(form, show="*").pack()
ttk.Button(form, text="Login", accent="primary").pack()

app.mainloop()
```

### Constructor options

- **`direction`** — `"vertical"` (default), `"horizontal"`, `"row"`, `"column"`, `"row-reverse"`, `"column-reverse"`. The `*-reverse` variants pack from the opposite edge.
- **`gap`** — pixels of space inserted between adjacent children. Applied as `pady` for vertical layouts and `padx` for horizontal layouts.
- **`padding`** — interior padding around all children (inherited from `Frame`).
- **`fill_items`** — default `fill` value (`"x"`, `"y"`, `"both"`, `"none"`) applied to every child.
- **`expand_items`** — default `expand` value (`True` / `False`) applied to every child.
- **`anchor_items`** — default `anchor` for every child.
- **`propagate`** — set to `False` to fix the frame's size and prevent it from resizing to its children.

Per-call options on `pack()` always override the container defaults.

### Horizontal layouts

```python
import ttkbootstrap as ttk

app = ttk.App()

toolbar = ttk.PackFrame(app, direction="horizontal", gap=4, padding=4)
toolbar.pack(fill="x")

ttk.Button(toolbar, text="New").pack()
ttk.Button(toolbar, text="Open").pack()
ttk.Button(toolbar, text="Save").pack()

app.mainloop()
```

### Container-level fill defaults

Use `fill_items` / `expand_items` when every child should stretch the same way:

```python
import ttkbootstrap as ttk

app = ttk.App()

stack = ttk.PackFrame(app, direction="vertical", gap=6, fill_items="x", padding=12)
stack.pack(fill="both", expand=True)

# No per-child fill needed — every child fills horizontally
ttk.Entry(stack).pack()
ttk.Entry(stack).pack()
ttk.Entry(stack).pack()

app.mainloop()
```

---

## GridFrame: structured layout

`GridFrame` is the right choice when widgets need to **line up across rows and columns** — label/value forms, settings panels, dashboards, property inspectors.

You declare the column (and optionally row) structure on the container; children are placed in order with `grid()` and **wrap to the next row automatically** once the columns fill.

```python
import ttkbootstrap as ttk

app = ttk.App()

grid = ttk.GridFrame(
    app,
    columns=["auto", 1],
    gap=(12, 6),
    sticky_items="ew",
    padding=12,
)
grid.pack(fill="both", expand=True)

# Auto-placement: each grid() call advances column-then-row
ttk.Label(grid, text="Name").grid()
ttk.Entry(grid).grid()
ttk.Label(grid, text="Email").grid()
ttk.Entry(grid).grid()
ttk.Button(grid, text="Save", accent="primary").grid(columnspan=2)

app.mainloop()
```

### Column and row size specs

`columns` and `rows` accept either a count (`columns=3`) or a list of size specs:

| Spec      | Meaning                                                                  |
| --------- | ------------------------------------------------------------------------ |
| `int`     | Weight: relative share of leftover space (`0` = no expansion, `1`+ = expand) |
| `"auto"`  | Size to content; do not expand                                           |
| `"100px"` | Minimum size in pixels                                                   |

`columns=["auto", 1]` produces a typical label/input form: the first column hugs its labels, the second absorbs all extra width.

`columns=[1, 1, 1]` produces three equal columns.

`columns=3` is shorthand for `columns=[1, 1, 1]`.

### Constructor options

- **`columns`** / **`rows`** — column/row count or list of size specs (above).
- **`gap`** — `int` for the same gap in both directions, or a `(column_gap, row_gap)` tuple.
- **`sticky_items`** — default `sticky` value applied to every child (e.g. `"ew"`, `"nsew"`).
- **`auto_flow`** — `"row"` (default), `"column"`, `"row-dense"`, `"column-dense"`, or `"none"`. Controls how auto-placement walks the grid.
- **`propagate`** — set to `False` to fix the frame's size.
- **`padding`** — interior padding (inherited from `Frame`).

### Auto-placement and spanning

Calls to `grid()` without `row=` / `column=` use auto-placement: the next free cell, walking left-to-right then top-to-bottom (or as configured by `auto_flow`).

`columnspan` and `rowspan` are honored by auto-placement — the spanning widget takes the next free area large enough, and subsequent children continue after it:

```python
import ttkbootstrap as ttk

app = ttk.App()

grid = ttk.GridFrame(app, columns=3, gap=8, sticky_items="ew", padding=12)
grid.pack(fill="both", expand=True)

ttk.Label(grid, text="Title").grid(columnspan=3)   # full width
ttk.Entry(grid).grid()                              # row 1, col 0
ttk.Entry(grid).grid()                              # row 1, col 1
ttk.Entry(grid).grid()                              # row 1, col 2

app.mainloop()
```

Pass `row=` and `column=` explicitly to override auto-placement and place a widget anywhere.

### Adjusting rows and columns after construction

If you need to tweak weight or minsize for a specific row or column after the fact, use `configure_row()` / `configure_column()`:

```python
grid = ttk.GridFrame(app, columns=2)
grid.configure_column(1, weight=2, minsize=200)
```

---

## Common patterns

### Label–value form

`PackFrame` works for stacked forms; `GridFrame` aligns labels across rows.

```python
import ttkbootstrap as ttk

app = ttk.App()

form = ttk.GridFrame(app, columns=["auto", 1], gap=(12, 8), sticky_items="ew", padding=16)
form.pack(fill="both", expand=True)

for label in ("Name", "Email", "Phone"):
    ttk.Label(form, text=label).grid(sticky="w")
    ttk.Entry(form).grid()

app.mainloop()
```

### Right-aligned button row

Use a horizontal `PackFrame` with `pack(side="right")` on the leading button:

```python
import ttkbootstrap as ttk

app = ttk.App()

actions = ttk.PackFrame(app, direction="horizontal", gap=8, padding=12)
actions.pack(fill="x")

# pack(side="right") reverses order, so list buttons primary-last
ttk.Button(actions, text="Cancel").pack(side="right")
ttk.Button(actions, text="OK", accent="primary").pack(side="right")

app.mainloop()
```

### Header / content / footer

Vertical `PackFrame` with content stretching to fill the middle:

```python
import ttkbootstrap as ttk

app = ttk.App()

shell = ttk.PackFrame(app, direction="vertical", gap=0)
shell.pack(fill="both", expand=True)

header = ttk.Frame(shell, padding=12, accent="primary")
header.pack(fill="x")
ttk.Label(header, text="My App").pack(anchor="w")

content = ttk.Frame(shell, padding=20)
content.pack(fill="both", expand=True)

footer = ttk.Frame(shell, padding=8)
footer.pack(fill="x")
ttk.Label(footer, text="Status: ready").pack(anchor="w")

app.mainloop()
```

### Sidebar + main

Horizontal `PackFrame` with the sidebar fixed-width and the main area expanding:

```python
import ttkbootstrap as ttk

app = ttk.App()

shell = ttk.PackFrame(app, direction="horizontal", gap=0)
shell.pack(fill="both", expand=True)

sidebar = ttk.Frame(shell, padding=12, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
ttk.Label(sidebar, text="Navigation").pack(anchor="w")

main = ttk.Frame(shell, padding=20)
main.pack(side="left", fill="both", expand=True)
ttk.Label(main, text="Main content").pack(anchor="w")

app.mainloop()
```

### Card grid

Drop `Card` containers into a `GridFrame` for dashboard-style layouts:

```python
import ttkbootstrap as ttk

app = ttk.App()

dashboard = ttk.GridFrame(app, columns=[1, 1, 1], gap=12, sticky_items="nsew", padding=16)
dashboard.pack(fill="both", expand=True)

for title in ("Users", "Sessions", "Errors"):
    card = ttk.Card(dashboard)
    card.grid()
    ttk.Label(card, text=title, font="label").pack(anchor="w")
    ttk.Label(card, text="—").pack(anchor="w")

app.mainloop()
```

---

## Card: a styled container

`Card` is a convenience wrapper around `Frame` with `accent="card"`, `show_border=True`, and `padding=16` applied by default. It's a styling shortcut, not a separate layout primitive — use any geometry manager inside it.

```python
import ttkbootstrap as ttk

app = ttk.App()

card = ttk.Card(app)
card.pack(fill="x", padx=12, pady=12)

ttk.Label(card, text="User Settings", font="label").pack(anchor="w")
ttk.CheckButton(card, text="Enable notifications").pack(anchor="w")
ttk.CheckButton(card, text="Dark mode").pack(anchor="w")

app.mainloop()
```

Use `Card` to group related controls into a visually elevated panel.

---

## Scrollable regions

Scrolling is a **container responsibility**, not a per-widget option. To make any layout scrollable, wrap it in a `ScrollView`.

`ScrollView.add()` returns a content `Frame` that lives inside the scrolled viewport — put your normal layout (typically a `PackFrame` or `GridFrame`) inside it.

```python
import ttkbootstrap as ttk

app = ttk.App()

sv = ttk.ScrollView(app)
sv.pack(fill="both", expand=True, padx=12, pady=12)

# add() returns a Frame inside the scrolled region.
content = sv.add()

stack = ttk.PackFrame(content, direction="vertical", gap=6, padding=12)
stack.pack(fill="both", expand=True)

for i in range(40):
    ttk.Label(stack, text=f"Row {i + 1}").pack(anchor="w")

app.mainloop()
```

Children of the content frame should not try to manage scrolling themselves. The viewport, scrollbars, and mouse-wheel bindings are owned by `ScrollView`.

!!! link "See [ScrollView](../widgets/layout/scrollview.md) for full options (scroll direction, scrollbar visibility modes, autohide)."

---

## Nesting containers

Nesting is normal and expected. Use it to:

- separate layout regions with different policies (header packs horizontally, body grids)
- isolate scrolling, resizing, or padding decisions
- compose larger layouts from smaller, well-scoped pieces

Prefer **shallow, intentional** nesting over deeply nested per-widget configuration.

```python
import ttkbootstrap as ttk

app = ttk.App()

grid = ttk.GridFrame(app, columns=[1, 1], gap=12, padding=12, sticky_items="nsew")
grid.pack(fill="both", expand=True)

# Left column
left = ttk.PackFrame(grid, direction="vertical", gap=6)
left.grid()
ttk.Label(left, text="General", font="label").pack(anchor="w")
ttk.CheckButton(left, text="Enable feature").pack(anchor="w")

# Right column
right = ttk.PackFrame(grid, direction="vertical", gap=6)
right.grid()
ttk.Label(right, text="Advanced", font="label").pack(anchor="w")
ttk.CheckButton(right, text="Verbose logging").pack(anchor="w")

app.mainloop()
```

---

## Method chaining

`pack()` and `grid()` return the widget, so you can chain configuration calls or capture a reference inline:

```python
form = ttk.PackFrame(app, direction="vertical", gap=8)
form.pack(fill="both", expand=True)

# Capture and place in one line
entry = ttk.Entry(form).pack()

# Chain further configuration
ttk.Button(form, text="Submit").pack().configure(command=lambda: None)
```

Chaining is a convenience, not a requirement. Reach for separate statements when the chain hurts readability.

---

## What the layout containers do *not* hide

`PackFrame` and `GridFrame` sit **on top of** `pack` and `grid`. They:

- apply structured defaults
- handle gap spacing
- automate row/column placement (grid only)
- track children for clean reconfiguration

They do not replace Tk's geometry system, and they do not change how `fill`, `expand`, `sticky`, or `weight` work. When you need finer control, drop into raw `pack()` / `grid()` calls — they still work inside these containers.

---

## Common layout mistakes

- **Mixing `pack` and `grid` in the same container.** Tk forbids this and will hang. Pick one per container; nest a `Frame` if you need both.
- **Repeating `padx` / `pady` on every child** instead of setting `gap` on a `PackFrame` / `GridFrame`.
- **Forgetting row/column weight.** `sticky="ew"` only stretches if the column has a non-zero weight (or you used `columns=[1, ...]` / `rows=[...]` on `GridFrame`).
- **Querying widget size before layout has run.** Geometry isn't realized until the event loop processes idle tasks; call `update_idletasks()` first or defer with `after_idle()`.
- **Over-nesting** containers without clear intent — each level of nesting should answer a question (which region scrolls? where does the gap change? which side expands?).

---

## Next steps

- [Spacing & Alignment](spacing-and-alignment.md) — the `pack` / `grid` mental model: padding, sticky, fill, expand, weight.
- [ScrollView](../widgets/layout/scrollview.md) — scrolling as a container responsibility.
- [PackFrame](../widgets/layout/packframe.md) and [GridFrame](../widgets/layout/gridframe.md) — full widget reference for each container.
- [Capabilities: Layout](../capabilities/layout/index.md) — layout as a framework capability: container mechanics, scrolling, lifecycle constraints.

If you're new to ttkbootstrap layout, start with `PackFrame` for linear flows and `GridFrame` for aligned forms. Drop down to `Frame` + raw `pack()` / `grid()` only when the helpers don't fit.
