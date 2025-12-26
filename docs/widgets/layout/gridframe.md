---
title: GridFrame
---

# GridFrame

`GridFrame` is a **layout container** with simplified grid-based layout management and auto-placement.

It extends the ttkbootstrap Frame with automatic grid-based layout management, including support for row/column definitions, gap spacing, auto-placement, and default sticky behavior. Use `GridFrame` when you need a CSS Grid-like layout experience without manually managing grid options.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

# 2x2 grid with gap
grid = ttk.GridFrame(app, columns=2, rows=2, gap=10, padding=20)
grid.pack(fill="both", expand=True)

# Widgets are auto-placed in row-major order
grid.add(ttk.Button(grid, text="Top-Left"))
grid.add(ttk.Button(grid, text="Top-Right"))
grid.add(ttk.Button(grid, text="Bottom-Left"))
grid.add(ttk.Button(grid, text="Bottom-Right"))

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

`GridFrame` inherits all styling options from Frame. Use `bootstyle` for semantic tokens.

```python
ttk.GridFrame(app, bootstyle="secondary", padding=20)
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

### Managing widgets

#### `add(widget, *, row=None, column=None, rowspan=1, columnspan=1, **options)`

Add a widget to the grid. If row/column are not specified, auto-placement is used.

```python
grid = ttk.GridFrame(app, columns=3, gap=8)

# Auto-placed
grid.add(ttk.Button(grid, text="A"))
grid.add(ttk.Button(grid, text="B"))
grid.add(ttk.Button(grid, text="C"))

# Explicit position
grid.add(ttk.Button(grid, text="Footer"), row=1, column=0, columnspan=3)

# With spanning
grid.add(ttk.Label(grid, text="Wide"), columnspan=2)
```

#### `insert(index, widget, **options)`

Insert a widget at a specific index in the managed list.

```python
grid.insert(0, ttk.Label(grid, text="Now first"))
```

#### `remove(widget)`

Remove a widget (ungrids but doesn't destroy).

```python
grid.remove(btn)
```

#### `move(widget, new_index)`

Move a widget to a new position in the managed list.

```python
grid.move(btn, 0)
```

#### `move_to(widget, row, column, rowspan=None, columnspan=None)`

Move a widget to a specific grid position.

```python
grid.move_to(btn, row=0, column=2)
```

#### `update_options(widget, **options)`

Update grid options for a widget.

```python
grid.update_options(btn, sticky="nsew", columnspan=2)
```

#### `clear()`

Remove all widgets.

```python
grid.clear()
```

### Configuring rows and columns

```python
# Configure a specific row
grid.configure_row(0, weight=1, minsize=50)

# Configure a specific column
grid.configure_column(1, weight=2, minsize=100)
```

### Querying widgets

```python
# Get number of managed widgets
count = len(grid)

# Iterate over managed widgets
for widget in grid:
    print(widget)

# Get position of a widget
row, col, rowspan, colspan = grid.get_position(btn)

# Get index of a widget
index = grid.index_of(btn)

# Access managed widgets list
widgets = grid.managed_widgets
```

---

## Behavior

- Widgets are auto-placed in row-major order by default (configurable via `auto_flow`).

- The `add()` method returns the widget for fluent/chaining patterns.

- Removing or reordering widgets automatically regrids remaining widgets.

- Per-widget options in `add()` override container defaults.

- Gap spacing is applied as padding on non-first rows/columns.

- GridFrame extends Frame, so all Frame options (bootstyle, padding, etc.) are available.

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