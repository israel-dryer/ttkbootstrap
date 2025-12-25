---
title: PackFrame
---

# PackFrame

`PackFrame` is a **layout container** with simplified pack-based layout management.

It extends the ttkbootstrap Frame with automatic pack-based layout management, including support for direction, gap spacing, and default fill/expand behavior. Use `PackFrame` when you want a flex-like layout experience without manually managing pack options.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

# Vertical stack with gap
stack = ttk.PackFrame(app, direction="vertical", gap=10, padding=20)
stack.pack(fill="both", expand=True)

# Add widgets using the add() method
stack.add(ttk.Button(stack, text="First"))
stack.add(ttk.Button(stack, text="Second"))
stack.add(ttk.Button(stack, text="Third"))

app.mainloop()
```

---

## When to use

Use `PackFrame` when:

- you want a simple vertical or horizontal stack of widgets
- you need consistent gap spacing between children
- you want to set default fill/expand behavior for all children
- you need to dynamically add, remove, or reorder widgets

**Consider a different control when:**

- you need a 2D grid layout -> use [GridFrame](gridframe.md)
- you just need a container without layout management -> use [Frame](frame.md)
- you need a labeled container -> use [LabelFrame](labelframe.md)

---

## Appearance

### Styling

`PackFrame` inherits all styling options from Frame. Use `bootstyle` for semantic tokens.

```python
ttk.PackFrame(app, bootstyle="secondary", padding=20)
```

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

---

## Examples & patterns

### `direction`

Controls the layout direction. Options: `"vertical"`, `"horizontal"`, `"row"`, `"column"`, `"row-reverse"`, `"column-reverse"`.

```python
# Vertical stack (top to bottom)
ttk.PackFrame(app, direction="vertical")

# Horizontal row (left to right)
ttk.PackFrame(app, direction="horizontal")

# Reverse order (bottom to top)
ttk.PackFrame(app, direction="column-reverse")
```

### `gap`

Spacing between children in pixels.

```python
ttk.PackFrame(app, direction="vertical", gap=12)
```

### `fill` / `expand`

Default fill and expand behavior for all children.

```python
# All children fill horizontally
stack = ttk.PackFrame(app, direction="vertical", fill="x")

# All children expand to fill available space
stack = ttk.PackFrame(app, direction="vertical", expand=True)
```

### `anchor`

Default anchor for children.

```python
ttk.PackFrame(app, direction="vertical", anchor="w")
```

### `propagate`

Control whether the frame resizes to fit its contents.

```python
# Fixed size frame
stack = ttk.PackFrame(app, width=300, height=400, propagate=False)
```

### Managing widgets

#### `add(widget, **options)`

Add a widget to the end of the frame. Returns the widget for chaining.

```python
stack = ttk.PackFrame(app, direction="vertical", gap=8)

btn = ttk.Button(stack, text="Click me")
stack.add(btn)

# With per-widget options that override defaults
stack.add(ttk.Label(stack, text="Full width"), fill="x")
```

#### `insert(index, widget, **options)`

Insert a widget at a specific position.

```python
stack.insert(0, ttk.Label(stack, text="Now first"))
```

#### `remove(widget)`

Remove a widget (unpacks but doesn't destroy).

```python
stack.remove(btn)
```

#### `move(widget, new_index)`

Move a widget to a new position.

```python
stack.move(btn, 0)  # Move to first position
```

#### `update_options(widget, **options)`

Update pack options for a widget.

```python
stack.update_options(btn, fill="x", expand=True)
```

#### `clear()`

Remove all widgets.

```python
stack.clear()
```

### Querying widgets

```python
# Get number of managed widgets
count = len(stack)

# Iterate over managed widgets
for widget in stack:
    print(widget)

# Get index of a widget
index = stack.index_of(btn)

# Access managed widgets list
widgets = stack.children
```

---

## Behavior

- Widgets are managed in order; gaps are applied automatically between consecutive widgets.

- The `add()` method returns the widget for fluent/chaining patterns.

- Removing or reordering widgets automatically repacks remaining widgets.

- Per-widget options in `add()` or `insert()` override container defaults.

- PackFrame extends Frame, so all Frame options (bootstyle, padding, etc.) are available.

---

## Additional resources

### Related widgets

- [GridFrame](gridframe.md) -- grid-based layout container
- [Frame](frame.md) -- basic container
- [LabelFrame](labelframe.md) -- container with visible label

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)
- [Layout](../../platform/geometry-and-layout.md)

### API reference

- **API Reference:** `ttkbootstrap.PackFrame`