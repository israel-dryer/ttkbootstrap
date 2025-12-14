---
title: PanedWindow
icon: fontawesome/solid/columns
---

# PanedWindow

`PanedWindow` is a themed wrapper around `ttk.PanedWindow` that provides a resizable split layout. It lets users drag a sash to adjust the relative size of two or more panes—perfect for master/detail layouts, editors, and dashboards.

<!--
IMAGE: Horizontal and vertical split
Suggested: Two PanedWindow examples (horizontal split with list/detail, vertical split with editor/output)
Theme variants: light / dark
-->

---

## Basic usage

Create a horizontal split with two panes:

```python
import ttkbootstrap as ttk

app = ttk.Window()

pw = ttk.PanedWindow(app, orient="horizontal")
pw.pack(fill="both", expand=True, padx=20, pady=20)

left = ttk.Frame(pw, padding=10)
right = ttk.Frame(pw, padding=10)

pw.add(left, weight=1)
pw.add(right, weight=3)

ttk.Label(left, text="Navigation").pack(anchor="w")
ttk.Label(right, text="Details").pack(anchor="w")

app.mainloop()
```

Create a vertical split:

```python
import ttkbootstrap as ttk

app = ttk.Window()

pw = ttk.PanedWindow(app, orient="vertical")
pw.pack(fill="both", expand=True, padx=20, pady=20)

top = ttk.Frame(pw, padding=10)
bottom = ttk.Frame(pw, padding=10)

pw.add(top, weight=2)
pw.add(bottom, weight=1)

ttk.Label(top, text="Editor").pack(anchor="w")
ttk.Label(bottom, text="Output").pack(anchor="w")

app.mainloop()
```

<!--
IMAGE: Basic PanedWindow example
Suggested: Horizontal split with visible sash and two labeled panes
-->

---

## What problem it solves

Many desktop applications benefit from user-adjustable layouts. `PanedWindow` solves this by:

- Allowing the user to resize regions with a drag handle (sash)
- Supporting common “split view” patterns (nav/detail, inspector, console, preview)
- Managing multiple panes in a single container

ttkbootstrap adds consistent styling via `bootstyle` so the sash and pane background align with your theme.

---

## Core concepts

### Orientation

`orient` controls the split direction:

- `"horizontal"` → panes are side-by-side (left/right)
- `"vertical"` → panes are stacked (top/bottom)

```python
ttk.PanedWindow(app, orient="horizontal")
ttk.PanedWindow(app, orient="vertical")
```

---

### Adding panes

Panes are added with `.add(widget, **options)`. Common pane options include:

- `weight` — relative resizing behavior
- `minsize` — minimum pane size
- `sticky` — how the pane content fills the space (depends on the pane’s internal layout)

```python
pw.add(left, weight=1, minsize=150)
pw.add(right, weight=3)
```

!!! tip "Put a Frame in each pane"
    Use a `Frame` as the actual pane widget, then lay out your real content inside that frame. This keeps your pane structure stable and makes layout easier.

---

### Padding and requested size

`padding` adds internal padding inside the PanedWindow container:

```python
pw = ttk.PanedWindow(app, padding=6)
```

You can also request an initial size:

```python
pw = ttk.PanedWindow(app, width=800, height=500)
```

---

## Common options & patterns

### Styling with bootstyle

```python
ttk.PanedWindow(app, bootstyle="secondary")
```

If you provide `style=...`, it overrides bootstyle.

---

### Master/detail layout pattern

A very common pattern is:

- left pane: list/tree/table
- right pane: detail view

```python
pw = ttk.PanedWindow(app, orient="horizontal")
pw.add(nav_frame, weight=1, minsize=200)
pw.add(detail_frame, weight=3)
```

<!--
IMAGE: Master/detail layout
Suggested: Left pane with TreeView, right pane with form
-->

---

### Inspector layout pattern

Another common pattern:

- main view
- right-side inspector pane

This works well for editors and workflow designers.

---

## Events

`PanedWindow` is usually used structurally, but you may respond to resize/layout changes via:

- `<Configure>` on the PanedWindow or pane frames

```python
pw.bind("<Configure>", lambda e: None)
```

If you need to respond specifically to sash movement, you can poll pane sizes or bind mouse events around the sash depending on platform constraints.

---

## UX guidance

- Provide sensible default pane weights and minimum sizes
- Don’t nest too many paned windows—two levels max is usually plenty
- Use separators, padding, and consistent pane backgrounds so the split feels intentional

!!! tip "Respect minimum sizes"
    Always set a `minsize` for navigation panes so users can’t collapse them to unusable widths.

---

## When to use / when not to

**Use PanedWindow when:**

- Users benefit from resizing regions (nav/detail, editor/console)
- The layout needs to adapt to different screen sizes
- You want a classic desktop split-view pattern

**Avoid PanedWindow when:**

- The layout should be fixed (use `Frame` + grid/pack)
- You need complex docking/tabbed layouts (consider `Notebook` + panels)
- The content is naturally scroll-based rather than resizable regions

---

## Related widgets

- **Frame** — common pane container
- **Notebook** — tabbed views (often paired with splits)
- **Separator** — subtle visual divisions
