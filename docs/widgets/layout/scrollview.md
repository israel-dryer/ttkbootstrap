---
title: ScrollView
icon: fontawesome/solid/arrows-up-down-left-right
---

# ScrollView

`ScrollView` is a canvas-based, scrollable container designed for **widget layouts**, not text. It provides a single scrollable region that can host a child container (typically a `Frame`) and enables mouse wheel scrolling across all descendants—including deeply nested widgets.

<!--
IMAGE: ScrollView with overflowing content
Suggested: A ScrollView containing a tall settings form, with scrollbar visible
Theme variants: light / dark
-->

---

## Basic usage

Create a scrollable region and add a single child container (usually a `Frame`). Place all content inside that container:

```python
import ttkbootstrap as ttk

app = ttk.Window()

scroll = ttk.ScrollView(app, direction="vertical", show_scrollbar="on-scroll")
scroll.pack(fill="both", expand=True, padx=20, pady=20)

content = ttk.Frame(scroll.canvas, padding=10)
scroll.add(content)

for i in range(30):
    ttk.Label(content, text=f"Row {i+1}").pack(anchor="w", pady=2)

app.mainloop()
```

<!--
IMAGE: Basic ScrollView example
Suggested: A tall list of rows inside a ScrollView with on-scroll scrollbar visible
-->

---

## What problem it solves

Standard ttk layouts don’t provide a “scrollable frame” out of the box. `ScrollView` solves this by:

- Providing a scrollable region for arbitrary widgets (forms, stacks, panels)
- Enabling mouse wheel scrolling on *all* child widgets (not just the canvas)
- Offering flexible scrollbar visibility modes (always, never, on hover, on scroll)
- Supporting vertical, horizontal, or bidirectional scrolling

---

## Core concepts

### ScrollView hosts exactly one child widget

`ScrollView` is designed around a single hosted widget added via `.add(...)`—typically a `Frame` that contains your layout.

```python
content = ttk.Frame(scroll.canvas)
scroll.add(content)
```

If you need to replace content later, call `remove()` first.

!!! note "One child only"
    `ScrollView` raises an error if you call `add(...)` when a child is already present. This keeps scroll-region logic predictable.

---

### Scroll direction

`direction` controls which scrollbars and mouse wheel gestures are active:

- `"vertical"` — vertical scrolling only
- `"horizontal"` — horizontal scrolling only (use **Shift+MouseWheel**)
- `"both"` — bidirectional scrolling

```python
ttk.ScrollView(app, direction="vertical")
ttk.ScrollView(app, direction="both")
```

---

### Scrollbar visibility modes

`show_scrollbar` controls when scrollbars appear, and they only show when content overflows the viewport:

- `"always"` — show when overflow exists
- `"never"` — hide scrollbars (scrolling still works)
- `"on-hover"` — show while hovering (if overflow exists)
- `"on-scroll"` — show during scrolling, then auto-hide

```python
ttk.ScrollView(app, show_scrollbar="on-hover")
ttk.ScrollView(app, show_scrollbar="on-scroll", autohide_delay=1000)
```

<!--
IMAGE GROUP: Scrollbar visibility modes
- Always (overflow only)
- On-hover (appears on enter)
- On-scroll (appears while scrolling)
-->

---

### Mouse wheel support across descendants

A common issue with scrollable canvases is that mouse wheel only works when the canvas has focus. `ScrollView` solves this by adding a custom bindtag to the canvas and all child widgets, so wheel gestures work even inside nested controls.

If you dynamically add lots of widgets at once and need to refresh bindings manually:

```python
scroll.refresh_bindings()
```

---

## Common options & patterns

### Styling the scrollbars

Use `scrollbar_style` to apply a bootstyle to both scrollbars:

```python
scroll = ttk.ScrollView(app, scrollbar_style="primary")
```

---

### Programmatic scrolling

You can control the view position directly:

```python
scroll.yview_moveto(0.0)   # top
scroll.yview_moveto(1.0)   # bottom
```

Similarly for horizontal scrolling:

```python
scroll.xview_moveto(0.0)
```

---

## Events

`ScrollView` is primarily structural. Common event patterns include:

- `<Configure>` on the hosted content to reflow layouts (usually handled internally)
- `<Configure>` on the scrollview/canvas when responding to viewport changes

In most cases you won’t need custom bindings—scroll region updates and visibility are managed for you.

---

## UX guidance

- Use ScrollView for **forms, settings pages, and widget stacks**
- Prefer vertical-only scrolling for most UIs
- Avoid horizontal scrolling unless your content truly needs it
- Use `on-scroll` or `on-hover` scrollbars to reduce visual noise in clean layouts

!!! tip "Smooth settings pages"
    A common pattern is a full-height ScrollView with an inner padded Frame. Keep consistent padding so content doesn’t touch the edges while scrolling.

---

## When to use / when not to

**Use ScrollView when:**

- You need a “scrollable frame” for arbitrary widgets
- Your content height can exceed the window height (settings pages, inspectors)
- You want mouse wheel scrolling to work anywhere inside the content

**Avoid ScrollView when:**

- You’re scrolling text content (use `ScrolledText`)
- You have a data grid or tree that has its own scrolling (use those widgets’ scrollbars)
- You need virtualized scrolling for huge lists (use a virtual list/data view pattern)

---

## Related widgets

- **Scrollbar** — the scrollbar primitive used internally
- **ScrolledText** — scrollable text widget
- **TreeView / TableView** — structured data views with their own scroll behavior
