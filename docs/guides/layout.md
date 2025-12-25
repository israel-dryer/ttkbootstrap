---
title: Layout
---

# Layout

This guide explains how to build layouts in ttkbootstrap using `Frame`, `PackFrame`, and `GridFrame`.

---

## The Layout Problem

Traditional Tkinter layout requires manual geometry management:

```python
# Without layout containers
label1 = ttk.Label(parent, text="First")
label1.pack(side="top", pady=(0, 10))

label2 = ttk.Label(parent, text="Second")
label2.pack(side="top", pady=(0, 10))

label3 = ttk.Label(parent, text="Third")
label3.pack(side="top")  # No padding on last item
```

Every widget needs explicit `pack()` or `grid()` calls. Gaps require manual padding. Reordering means updating multiple lines.

ttkbootstrap's layout containers solve this.

---

## The Three Containers

ttkbootstrap provides three layout containers:

| Container | Purpose | Use When |
|-----------|---------|----------|
| `Frame` | Basic container | You need manual control or a simple wrapper |
| `PackFrame` | Stack layout | Vertical or horizontal lists with consistent gaps |
| `GridFrame` | Grid layout | 2D layouts with rows and columns |

**Recommendation**: Start with `PackFrame` or `GridFrame`. Use `Frame` when you need manual geometry control.

---

## PackFrame: Stack Layouts

`PackFrame` arranges children in a single direction with automatic gap spacing.

### Basic Usage

```python
import ttkbootstrap as ttk

app = ttk.App()

stack = ttk.PackFrame(app, direction="vertical", gap=10, padding=20)
stack.pack(fill="both", expand=True)

stack.add(ttk.Label(stack, text="First"))
stack.add(ttk.Label(stack, text="Second"))
stack.add(ttk.Label(stack, text="Third"))

app.mainloop()
```

Key points:

- `direction="vertical"` stacks top-to-bottom
- `gap=10` adds 10px between each child
- `add()` manages widget placement automatically

### Direction Options

```python
# Vertical (default)
ttk.PackFrame(app, direction="vertical")   # Top to bottom
ttk.PackFrame(app, direction="column")     # Same as vertical

# Horizontal
ttk.PackFrame(app, direction="horizontal") # Left to right
ttk.PackFrame(app, direction="row")        # Same as horizontal

# Reverse
ttk.PackFrame(app, direction="column-reverse")  # Bottom to top
ttk.PackFrame(app, direction="row-reverse")     # Right to left
```

### Default Fill and Expand

Set defaults for all children:

```python
# All children fill horizontally
stack = ttk.PackFrame(app, direction="vertical", gap=10, fill="x")

# All children expand to fill available space
stack = ttk.PackFrame(app, direction="vertical", gap=10, expand=True)
```

Override per-widget:

```python
stack.add(ttk.Label(stack, text="Normal"))
stack.add(ttk.Label(stack, text="Full width"), fill="x")
```

### Managing Widgets

```python
# Add to end
stack.add(widget)

# Insert at position
stack.insert(0, widget)  # Insert at beginning

# Remove (but don't destroy)
stack.remove(widget)

# Reorder
stack.move(widget, 0)  # Move to beginning

# Clear all
stack.clear()
```

!!! link "PackFrame Reference"
    See [`ttkbootstrap.PackFrame`](../reference/widgets/PackFrame.md) for all options.

---

## GridFrame: 2D Layouts

`GridFrame` arranges children in a grid with automatic placement.

### Basic Usage

```python
import ttkbootstrap as ttk

app = ttk.App()

grid = ttk.GridFrame(app, columns=2, gap=10, padding=20)
grid.pack(fill="both", expand=True)

grid.add(ttk.Label(grid, text="Name:"))
grid.add(ttk.Entry(grid))
grid.add(ttk.Label(grid, text="Email:"))
grid.add(ttk.Entry(grid))

app.mainloop()
```

Widgets are placed left-to-right, top-to-bottom automatically.

### Column and Row Configuration

```python
# Equal columns
ttk.GridFrame(app, columns=3)

# Weighted columns (middle gets 2x space)
ttk.GridFrame(app, columns=[1, 2, 1])

# Fixed and flexible
ttk.GridFrame(app, columns=["200px", 1, "auto"])
```

Size specs:

- Integer: relative weight (like CSS `fr` units)
- `"auto"`: size to content
- `"100px"`: fixed pixel size

### Spanning

```python
# Widget spans 2 columns
grid.add(ttk.Label(grid, text="Wide"), columnspan=2)

# Widget spans 2 rows
grid.add(ttk.Label(grid, text="Tall"), rowspan=2)

# Explicit position
grid.add(ttk.Label(grid, text="Footer"), row=2, column=0, columnspan=3)
```

### Default Sticky

Control how widgets fill their cells:

```python
# All widgets stretch to fill cells
grid = ttk.GridFrame(app, columns=2, sticky="nsew")

# Override per-widget
grid.add(ttk.Label(grid, text="Centered"), sticky="")
```

!!! link "GridFrame Reference"
    See [`ttkbootstrap.GridFrame`](../reference/widgets/GridFrame.md) for all options.

---

## Frame: Manual Layout

`Frame` is the basic container. Use it when you need full control.

```python
import ttkbootstrap as ttk

app = ttk.App()

frame = ttk.Frame(app, padding=20)
frame.pack(fill="both", expand=True)

# Manual layout
ttk.Label(frame, text="Label").pack(anchor="w")
ttk.Entry(frame).pack(fill="x", pady=(5, 0))
ttk.Button(frame, text="Submit").pack(anchor="e", pady=(10, 0))

app.mainloop()
```

Use `Frame` when:

- you need very specific positioning
- you're building a custom composite widget
- the automatic behavior of PackFrame/GridFrame doesn't fit

!!! link "Frame Reference"
    See [`ttkbootstrap.Frame`](../reference/widgets/Frame.md) for options.

---

## Common Patterns

### Toolbar

```python
toolbar = ttk.PackFrame(app, direction="horizontal", gap=5, padding=(10, 5))
toolbar.pack(fill="x")

toolbar.add(ttk.Button(toolbar, text="New"))
toolbar.add(ttk.Button(toolbar, text="Open"))
toolbar.add(ttk.Button(toolbar, text="Save"))
```

### Form

```python
form = ttk.GridFrame(app, columns=["auto", 1], gap=(10, 8), padding=20)
form.pack(fill="both", expand=True)

form.add(ttk.Label(form, text="Username:"))
form.add(ttk.Entry(form), sticky="ew")

form.add(ttk.Label(form, text="Password:"))
form.add(ttk.Entry(form, show="*"), sticky="ew")

form.add(ttk.Button(form, text="Login"), column=1, sticky="e")
```

### Sidebar + Content

```python
main = ttk.PackFrame(app, direction="horizontal", padding=0)
main.pack(fill="both", expand=True)

# Fixed-width sidebar
sidebar = ttk.PackFrame(main, direction="vertical", gap=5, padding=10)
main.add(sidebar)

sidebar.add(ttk.Button(sidebar, text="Dashboard"))
sidebar.add(ttk.Button(sidebar, text="Settings"))

# Expanding content area
content = ttk.Frame(main, padding=20)
main.add(content, fill="both", expand=True)

ttk.Label(content, text="Content goes here").pack()
```

### Card Grid

```python
cards = ttk.GridFrame(app, columns=3, gap=15, padding=20)
cards.pack(fill="both", expand=True)

for i in range(6):
    card = ttk.LabelFrame(cards, text=f"Card {i+1}", padding=15)
    cards.add(card, sticky="nsew")
    ttk.Label(card, text="Card content").pack()
```

---

## Nesting Containers

Complex layouts combine containers:

```python
app = ttk.App(size=(800, 600))

# Main vertical layout
main = ttk.PackFrame(app, direction="vertical", padding=0)
main.pack(fill="both", expand=True)

# Toolbar
toolbar = ttk.PackFrame(main, direction="horizontal", gap=5, padding=10)
main.add(toolbar, fill="x")
toolbar.add(ttk.Button(toolbar, text="File"))
toolbar.add(ttk.Button(toolbar, text="Edit"))

# Content area (horizontal split)
body = ttk.PackFrame(main, direction="horizontal", padding=0)
main.add(body, fill="both", expand=True)

# Sidebar
sidebar = ttk.PackFrame(body, direction="vertical", gap=5, padding=10)
body.add(sidebar)
sidebar.add(ttk.Label(sidebar, text="Navigation"))

# Main content
content = ttk.Frame(body, padding=20)
body.add(content, fill="both", expand=True)
ttk.Label(content, text="Main content").pack()

# Status bar
status = ttk.Frame(main, padding=(10, 5))
main.add(status, fill="x")
ttk.Label(status, text="Ready").pack(side="left")
```

---

## When to Use Each

| Scenario | Container |
|----------|-----------|
| Vertical list of items | `PackFrame` with `direction="vertical"` |
| Horizontal toolbar | `PackFrame` with `direction="horizontal"` |
| Form with labels + inputs | `GridFrame` with 2 columns |
| Dashboard with cards | `GridFrame` with N columns |
| Custom composite widget | `Frame` with manual layout |
| Simple wrapper | `Frame` |

---

## Summary

- **PackFrame** for 1D stacks (vertical or horizontal)
- **GridFrame** for 2D grids with auto-placement
- **Frame** for manual control or simple containers
- Use `gap` to add consistent spacing
- Use `add()` to let containers manage placement
- Nest containers to build complex layouts

---

## Next Steps

- [App Structure](app-structure.md) — how applications are organized
- [Reactivity](reactivity.md) — connecting widgets with signals
- [Styling](styling.md) — applying consistent styling
