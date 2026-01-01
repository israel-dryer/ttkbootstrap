---
title: PackFrame
---

# PackFrame

`PackFrame` is a **layout container** with simplified pack-based layout management.

It extends the ttkbootstrap Frame with automatic pack-based layout management, including support for direction, gap spacing, and default fill/expand behavior. Use `PackFrame` when you want a flex-like layout experience without manually managing pack options.

Children simply call the standard `pack()` method and automatically receive the frame's default layout options.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

# Vertical stack with gap
stack = ttk.PackFrame(app, direction="vertical", gap=10, padding=20)
stack.pack(fill="both", expand=True)

# Add widgets using standard pack()
ttk.Button(stack, text="First").pack()
ttk.Button(stack, text="Second").pack()
ttk.Button(stack, text="Third").pack()

app.mainloop()
```

---

## When to use

Use `PackFrame` when:

- you want a simple vertical or horizontal stack of widgets
- you need consistent gap spacing between children
- you want to set default fill/expand behavior for all children
- you want standard `pack()` calls to work with managed defaults

**Consider a different control when:**

- you need a 2D grid layout -> use [GridFrame](gridframe.md)
- you just need a container without layout management -> use [Frame](frame.md)
- you need a labeled container -> use [LabelFrame](labelframe.md)

---

## Appearance

### Styling

`PackFrame` inherits all styling options from Frame. Use `color` for semantic tokens.

```python
ttk.PackFrame(app, color="secondary", padding=20)
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

### `fill_items` / `expand_items`

Default fill and expand behavior for all children.

```python
# All children fill horizontally
stack = ttk.PackFrame(app, direction="vertical", fill_items="x")

# All children expand to fill available space
stack = ttk.PackFrame(app, direction="vertical", expand_items=True)
```

### `anchor_items`

Default anchor for children.

```python
ttk.PackFrame(app, direction="vertical", anchor_items="w")
```

### `propagate`

Control whether the frame resizes to fit its contents.

```python
# Fixed size frame
stack = ttk.PackFrame(app, width=300, height=400, propagate=False)
```

### Adding widgets

Children use standard `pack()` to add themselves. The frame automatically applies its defaults.

```python
stack = ttk.PackFrame(app, direction="vertical", gap=8, fill_items="x")

# These all use the frame's defaults (fill="x", gap spacing)
ttk.Button(stack, text="Button 1").pack()
ttk.Button(stack, text="Button 2").pack()
ttk.Button(stack, text="Button 3").pack()

# Override defaults for specific widgets
ttk.Label(stack, text="Centered").pack(fill="none", anchor="center")
```

### Method chaining

The `pack()` method returns the widget for chaining:

```python
btn = ttk.Button(stack, text="Click").pack()
btn.configure(command=my_callback)

# Or chain further
ttk.Entry(stack).pack().focus()
```

### Insertion order

Use `before` and `after` to control widget placement:

```python
stack = ttk.PackFrame(app, direction="vertical", gap=10)

first = ttk.Label(stack, text="First").pack()
last = ttk.Label(stack, text="Last").pack()

# Insert between existing widgets
ttk.Label(stack, text="Middle").pack(after=first)
```

### Removing widgets

Use standard `pack_forget()` to remove widgets:

```python
btn = ttk.Button(stack, text="Removable").pack()

# Later, remove it
btn.pack_forget()
```

---

## Behavior

- Widgets are managed in order; gaps are applied automatically between consecutive widgets.

- The `pack()` method returns the widget for fluent/chaining patterns.

- Removing widgets automatically adjusts gap spacing for remaining widgets.

- Per-widget options in `pack()` override container defaults.

- PackFrame extends Frame, so all Frame options (color, padding, etc.) are available.

- Standard tkinter pack options (`before`, `after`, `fill`, `expand`, `anchor`, etc.) work as expected.

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

- [`ttkbootstrap.PackFrame`](../../reference/widgets/PackFrame.md)
