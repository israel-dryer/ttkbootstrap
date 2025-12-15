---
title: Separator
icon: fontawesome/solid/grip-lines
---

# Separator

`Separator` is a themed wrapper around `ttk.Separator` used to create subtle visual divisions between sections of a user interface. It’s a **non-interactive layout primitive** that improves readability and structure without adding visual noise.

<!--
IMAGE: Separator horizontal and vertical
Suggested: Horizontal separator between form sections and vertical separator in a toolbar
Theme variants: light / dark
-->

---

## Basic usage

Create a horizontal separator between sections:

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="General").pack(anchor="w", padx=20, pady=(20, 6))

ttk.Separator(app, orient="horizontal").pack(fill="x", padx=20)

ttk.Label(app, text="Advanced").pack(anchor="w", padx=20, pady=(12, 0))

app.mainloop()
```

Create a vertical separator (commonly used in toolbars or side panels):

```python
import ttkbootstrap as ttk

app = ttk.App()

toolbar = ttk.Frame(app, padding=6)
toolbar.pack(fill="x")

ttk.Button(toolbar, text="New").pack(side="left")
ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=6)
ttk.Button(toolbar, text="Open").pack(side="left")

app.mainloop()
```

<!--
IMAGE: Basic Separator example
Suggested: Horizontal separator in a settings panel and vertical separator in a toolbar
-->

---

## What problem it solves

Large or complex UIs benefit from visual structure. `Separator` solves this by:

- Creating a clear but subtle boundary between related UI sections
- Improving scanability without heavy borders or containers
- Supporting both horizontal and vertical orientations
- Integrating with ttkbootstrap’s theme system for consistent appearance

Separators are especially useful when spacing alone isn’t enough to convey grouping.

---

## Core concepts

### Orientation

The `orient` option controls the separator direction:

- `"horizontal"` — divides content top-to-bottom
- `"vertical"` — divides content left-to-right

```python
ttk.Separator(app, orient="horizontal")
ttk.Separator(app, orient="vertical")
```

---

### Separator vs borders

Separators are **decorative dividers**, not containers:

- Use **Separator** to divide sections within the same container
- Use **Frame / LabelFrame** when you need a grouping container or background

A good rule: separators divide *content*, frames contain *content*.

---

## Common options & patterns

### Styling with bootstyle

Apply a semantic style token:

```python
ttk.Separator(app, bootstyle="secondary")
```

You can also provide an explicit ttk style name via `style=...`, which overrides `bootstyle`.

<!--
IMAGE: Separator bootstyle variants
Suggested: Multiple separators with different bootstyles
-->

---

### Padding and layout

Separators are typically paired with padding in the layout manager:

```python
ttk.Separator(app).pack(fill="x", padx=20, pady=10)
```

Spacing around the separator is often more important than the separator itself for good visual rhythm.

---

## Events

`Separator` is non-interactive and does not emit meaningful events. In most cases, you should not bind events to it.

---

## UX guidance

- Use separators sparingly — they should clarify structure, not dominate it
- Prefer horizontal separators for vertical layouts (forms, settings pages)
- Prefer vertical separators in toolbars or horizontal action rows

!!! tip "Less is more"
    If spacing alone communicates grouping clearly, you may not need a separator at all.

---

## When to use / when not to

**Use Separator when:**

- You need a clear visual division between sections
- Content density is high and grouping needs reinforcement
- You want a lighter alternative to boxed layouts

**Avoid Separator when:**

- A container or panel would communicate grouping better
- Overuse would create visual clutter
- The UI already has strong spacing and alignment cues

---

## Related widgets

- **Frame** — layout container
- **LabelFrame** — labeled group container
- **PanedWindow** — resizable division between regions
