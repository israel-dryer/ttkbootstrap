---
title: LabelFrame
icon: fontawesome/solid/square-pen
---

# LabelFrame

`LabelFrame` is a themed wrapper around `ttk.Labelframe` that provides a bordered container with an embedded caption. It’s ideal for visually grouping related controls (settings sections, form clusters) with a clear label that improves scanability.

<!--
IMAGE: Labeled group box
Suggested: LabelFrame titled “Network” containing a few related controls
Theme variants: light / dark
-->

---

## Basic usage

Use `LabelFrame` to group a set of widgets under a caption:

```python
import ttkbootstrap as ttk

app = ttk.Window()

group = ttk.LabelFrame(app, text="Account", padding=10)
group.pack(fill="x", padx=20, pady=20)

ttk.Label(group, text="Email").pack(anchor="w")
ttk.Entry(group).pack(fill="x", pady=(6, 0))

app.mainloop()
```

<!--
IMAGE: Basic LabelFrame example
Suggested: A labeled frame containing a label + entry
-->

---

## What problem it solves

When a UI has many controls, users benefit from clear visual structure. `LabelFrame` solves this by:

- Creating a visible “group box” boundary around related widgets
- Providing a built-in caption so users can quickly understand what a section controls
- Allowing consistent spacing via `padding`
- Integrating with ttkbootstrap theming (`bootstyle`, surface tokens, and localization)

---

## Core concepts

### LabelFrame vs Frame

Both are containers, but they serve different UX roles:

- **Frame**
  - Pure layout surface (no caption)
  - Best for structural layout: panels, toolbars, pages

- **LabelFrame**
  - Adds a border + caption
  - Best for semantic grouping: settings sections, option groups

If you don’t need a visible group boundary, prefer `Frame` for a cleaner layout.

---

### Caption positioning (labelanchor)

The `labelanchor` option controls where the caption sits around the border.

```python
ttk.LabelFrame(app, text="Advanced", labelanchor="n")
```

Typical anchors include top/left variants (exact support depends on Tk). Use this to match your layout style (e.g., left-aligned captions for dense forms).

<!--
IMAGE: labelanchor variations
Suggested: Same LabelFrame rendered with different labelanchor values
-->

---

## Common options & patterns

### Padding

`padding` adds space inside the group box:

```python
ttk.LabelFrame(app, text="Filters", padding=12)
```

This is the most common option to set on LabelFrame because it ensures content does not crowd the border.

---

### Styling with bootstyle

Use `bootstyle` to apply theme tokens:

```python
ttk.LabelFrame(app, text="Details", bootstyle="secondary")
```

If you provide an explicit `style=...`, it overrides `bootstyle`.

---

### Localization

`LabelFrame` supports `localize` so its caption can participate in your localization system:

```python
ttk.LabelFrame(app, text="settings.network", localize="auto")
```

(Exact key conventions depend on your message catalog setup.)

---

## Events

Like `Frame`, `LabelFrame` is primarily a container. Typical bindings include:

- `<Configure>` for resize-driven behavior
- `<Enter>` / `<Leave>` for hover-driven visuals on a region

```python
group.bind("<Configure>", lambda e: print(e.width, e.height))
```

---

## UX guidance

- Use LabelFrames sparingly — too many borders can make a UI feel busy
- Prefer one LabelFrame per “meaningful section” rather than per field
- Keep captions short and scannable (“Account”, “Network”, “Advanced”)

!!! tip "Clean settings pages"
    If you have many sections, combine LabelFrames with spacing and separators so the page still feels lightweight.

---

## When to use / when not to

**Use LabelFrame when:**

- You want a visible group boundary around related controls
- The caption meaningfully improves scanability
- You’re building settings pages or grouped option UIs

**Avoid LabelFrame when:**

- Grouping is obvious from layout alone (use `Frame` + spacing)
- You need a lightweight, modern “card” look (use a bordered `Frame` pattern)
- Content must scroll as one surface (use scroll containers)

---

## Related widgets

- **Frame** — basic layout container
- **Separator** — subtle division between groups
- **PanedWindow** — split layouts
