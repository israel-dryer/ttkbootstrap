---
title: GridFrame
---

# GridFrame

`GridFrame` is a **layout container** with simplified grid-based layout management and auto-placement.

It extends the ttkbootstrap Frame with automatic grid-based layout management, including support for row/column definitions, gap spacing, auto-placement, and default sticky behavior. Use `GridFrame` when you need a CSS Grid-like layout experience without manually managing grid options.

Children simply call the standard `grid()` method and automatically receive the frame's default layout options and auto-placement.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

# 2x2 grid with gap
grid = ttk.GridFrame(app, columns=2, rows=2, gap=10, padding=20)
grid.pack(fill="both", expand=True)

# Widgets are auto-placed in row-major order using standard grid()
ttk.Button(grid, text="Top-Left").grid()
ttk.Button(grid, text="Top-Right").grid()
ttk.Button(grid, text="Bottom-Left").grid()
ttk.Button(grid, text="Bottom-Right").grid()

app.mainloop()
```

---

## When to use

Use `GridFrame` when:

- you need a 2D grid layout
- you want CSS Grid-like auto-placement
- you need consistent gap spacing between cells
- you want to define row/column sizes declaratively

**Consider a different control when:**

- you only need a 1D stack -> use [PackFrame](packframe.md)
- you just need a container without layout management -> use [Frame](frame.md)
- you need resizable split regions -> use [PanedWindow](panedwindow.md)

---

## Appearance

### Styling

`GridFrame` inherits all styling options from Frame. Use `color` for semantic tokens.

```python
ttk.GridFrame(app, color="secondary", padding=20)
```

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

---

## Examples & patterns

### `rows` / `columns`

Define the grid structure. Can be an integer (number of equal-weight rows/columns) or a list of size specs.

```python
# Simple 3x3 grid
ttk.GridFrame(app, rows=3, columns=3)

# Custom column weights
ttk.GridFrame(app, columns=[1, 2, 1])  # Middle column gets 2x weight

# Fixed-size and auto columns
ttk.GridFrame(app, columns=["200px", 1, "auto"])
```

Size specs:

- Integer: weight for flexible sizing (like CSS fr units)
- `"auto"`: size to content
- `"100px"`: fixed pixel size

### `gap`

Spacing between cells. Can be uniform or separate column/row gaps.

```python
# Uniform 10px gap
ttk.GridFrame(app, gap=10)

# Different column and row gaps
ttk.GridFrame(app, gap=(8, 12))  # (column_gap, row_gap)
```

### `sticky_items`

Default sticky value for all children.

```python
# All widgets stretch to fill their cell
ttk.GridFrame(app, columns=2, sticky_items="nsew")
```

### `auto_flow`

Control how widgets are auto-placed. Options: `"row"`, `"column"`, `"row-dense"`, `"column-dense"`, `"none"`.

```python
# Fill by rows (default)
ttk.GridFrame(app, columns=3, auto_flow="row")

# Fill by columns
ttk.GridFrame(app, columns=3, auto_flow="column")

# Dense packing (fills gaps)
ttk.GridFrame(app, columns=3, auto_flow="row-dense")
```

### `propagate`

Control whether the frame resizes to fit its contents.

```python
grid = ttk.GridFrame(app, width=400, height=300, propagate=False)
```

### Adding widgets

Children use standard `grid()` to add themselves. The frame automatically applies its defaults and handles auto-placement.

```python
grid = ttk.GridFrame(app, columns=3, gap=8, sticky_items="nsew")

# Auto-placed widgets (row-major order by default)
ttk.Button(grid, text="A").grid()  # row=0, col=0
ttk.Button(grid, text="B").grid()  # row=0, col=1
ttk.Button(grid, text="C").grid()  # row=0, col=2
ttk.Button(grid, text="D").grid()  # row=1, col=0

# Explicit position
ttk.Button(grid, text="Footer").grid(row=2, column=0, columnspan=3)

# With spanning
ttk.Label(grid, text="Wide").grid(columnspan=2)

# Override default sticky
ttk.Label(grid, text="Centered").grid(sticky="")
```

### Method chaining

The `grid()` method returns the widget for chaining:

```python
btn = ttk.Button(grid, text="Click").grid()
btn.configure(command=my_callback)

# Or chain further
ttk.Entry(grid).grid(columnspan=2).focus()
```

### Removing widgets

Use standard `grid_forget()` to remove widgets:

```python
btn = ttk.Button(grid, text="Removable").grid()

# Later, remove it
btn.grid_forget()
```

### Configuring rows and columns

```python
# Configure a specific row
grid.configure_row(0, weight=1, minsize=50)

# Configure a specific column
grid.configure_column(1, weight=2, minsize=100)
```

---

## Behavior

- Widgets are auto-placed in row-major order by default (configurable via `auto_flow`).

- The `grid()` method returns the widget for fluent/chaining patterns.

- Removing widgets automatically adjusts auto-placement for remaining widgets.

- Per-widget options in `grid()` override container defaults.

- Gap spacing is applied as padding on non-first rows/columns.

- GridFrame extends Frame, so all Frame options (color, padding, etc.) are available.

- Standard tkinter grid options (`row`, `column`, `rowspan`, `columnspan`, `sticky`, etc.) work as expected.

---

## Additional resources

### Related widgets

- [PackFrame](packframe.md) -- pack-based layout container
- [Frame](frame.md) -- basic container
- [LabelFrame](labelframe.md) -- container with visible label
- [PanedWindow](panedwindow.md) -- resizable split regions

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)
- [Layout](../../platform/geometry-and-layout.md)

### API reference

- [`ttkbootstrap.GridFrame`](../../reference/widgets/GridFrame.md)
