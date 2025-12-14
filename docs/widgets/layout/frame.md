---
title: Frame
icon: fontawesome/regular/square
---

# Frame

`Frame` is a themed wrapper around `ttk.Frame` that integrates ttkbootstrap’s styling system. It’s the core **layout and grouping container** used to organize widgets, apply padding, and create visual structure in your UI.

<!--
IMAGE: Frame used for layout
Suggested: A simple form section inside a padded Frame (label + entry + buttons)
Theme variants: light / dark
-->

---

## Basic usage

Use `Frame` as a container and place child widgets inside it:

```python
import ttkbootstrap as ttk

app = ttk.Window()

frame = ttk.Frame(app, padding=10)
frame.pack(fill="both", expand=True, padx=20, pady=20)

ttk.Label(frame, text="Settings").pack(anchor="w")
ttk.Entry(frame).pack(fill="x", pady=(6, 0))

app.mainloop()
```

<!--
IMAGE: Basic Frame example
Suggested: A padded container with a visible header label and input
-->

---

## What problem it solves

Frames solve the most common UI problem: **structure**.

They let you:

- Group related widgets (sections, panels, toolbars, footers)
- Apply consistent padding and spacing
- Control layout with `pack` / `grid`
- Provide visual separation (optionally with borders)

ttkbootstrap’s `Frame` adds `bootstyle` and optional border styling so containers look consistent with the active theme.

---

## Core concepts

### Frame is a layout primitive

`Frame` itself is not interactive — it is a **layout surface**. It becomes useful when combined with:

- geometry managers (`pack`, `grid`)
- padding/margins
- themed styling (backgrounds, borders)

If you need a labeled boundary, use `LabelFrame` instead.

---

### Padding and size

The `padding` option adds space *inside* the frame:

```python
ttk.Frame(app, padding=12)
```

You can also request a specific size:

```python
ttk.Frame(app, width=320, height=200)
```

Note: requested sizes are honored only when geometry propagation is disabled or constrained by the parent layout.

---

### Borders with show_border

`Frame` supports a `show_border` style option to draw a border around the container.

```python
panel = ttk.Frame(app, padding=10, show_border=True)
panel.pack(fill="x", padx=20, pady=20)
```

This is implemented as a style option so it remains theme-consistent and does not require manual relief/border juggling.

<!--
IMAGE: Framed panel border
Suggested: Two frames: one plain and one with show_border=True
-->

---

## Common options & patterns

### Using bootstyle

Use `bootstyle` to match the frame with a semantic style token:

```python
ttk.Frame(app, bootstyle="secondary")
```

If you need an explicit ttk style name, you can provide `style=...` which overrides bootstyle.

---

### Building a “panel” layout

A common pattern is a bordered panel with internal padding:

```python
panel = ttk.Frame(app, padding=12, show_border=True)
panel.pack(fill="both", expand=True, padx=20, pady=20)
```

Inside the panel, place content using `grid` for forms or `pack` for stacked layouts.

---

## Events

`Frame` is a container, so you typically don’t bind “business events” to it. Common uses include:

- `<Configure>` when responding to resize
- `<Enter>` / `<Leave>` for hover-driven UI effects on a region

```python
frame.bind("<Configure>", lambda e: print(e.width, e.height))
```

---

## UX guidance

- Use frames to create clear visual sections and reduce cognitive load
- Prefer consistent padding at section boundaries
- Use `show_border=True` sparingly — too many borders can create visual noise

!!! tip "Readable layouts"
    Use a small set of container patterns (page, section, panel, footer) so your UI feels consistent across screens.

---

## When to use / when not to

**Use Frame when:**

- You need a generic container for layout and grouping
- You want to apply padding to a region
- You’re building panels, sections, toolbars, or page layouts

**Avoid Frame when:**

- You need a labeled container (use `LabelFrame`)
- You need scrollable content (use `ScrollView` / `ScrolledFrame` patterns)
- You need interactive selection or navigation (use appropriate controls)

---

## Related widgets

- **LabelFrame** — container with a caption/label
- **PanedWindow** — resizable split layout container
- **ScrollView / ScrolledText** — scrollable containers
- **Separator** — subtle visual division between sections
