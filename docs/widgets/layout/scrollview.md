---
title: ScrollView
---

# ScrollView

`ScrollView` is a **scrollable container** for arbitrary widgets.

It provides a framed content area inside a scrolling viewport, handling scrollbars, mousewheel behavior, and sizing so you can
build scrollable panels and forms without manually wiring a `Canvas` + scrollbars.

<!--
IMAGE: ScrollView with a long form or a list of cards
Theme variants: light / dark
-->

---

## Overview

Use `ScrollView` to:

- scroll long forms, settings panels, or stacked content
- build resizable layouts where only part of the UI scrolls
- avoid manual Canvas/Scrollbar plumbing

`ScrollView` is different from `ScrolledText`:

- `ScrollView` scrolls **widgets**
- `ScrolledText` scrolls **text content** (tk.Text)

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

sv = ttk.ScrollView(app)
sv.pack(fill="both", expand=True, padx=20, pady=20)

# Add content to the scrollable interior
for i in range(30):
    ttk.Label(sv, text=f"Row {i+1}").pack(anchor="w", pady=4)

app.mainloop()
```

---

## Core concept

A `ScrollView` exposes an interior “content” region (the widget itself acts as the content parent in most APIs).
You pack/grid your widgets into that region; `ScrollView` manages the viewport and scrollbars around it.

---

## Common options & patterns

### Scroll direction

If supported by your implementation, choose vertical, horizontal, or both scrolling depending on content.
For code-like content (horizontal scrolling), also set `wrap="none"` on text-based widgets inside.

### Scrollbar visibility

If your implementation supports auto-hide policies (always/never/on-hover/on-scroll), use them to keep UI clean.

### Padding

Wrap your content in an inner `Frame` if you want consistent padding without affecting scroll calculations:

```python
inner = ttk.Frame(sv, padding=16)
inner.pack(fill="both", expand=True)

for i in range(20):
    ttk.Label(inner, text=f"Item {i+1}").pack(anchor="w", pady=4)
```

---

## Behavior

- Mouse wheel scrolling is handled for cross-platform consistency.
- The scroll region updates as content size changes.
- Use `fill="both", expand=True` to let the viewport grow with the window.

---

## When should I use ScrollView?

Use `ScrollView` when:

- you need to scroll a region that contains normal widgets (forms/panels/cards)

Prefer **ScrolledText** when:

- you need a multi-line text editor/log output

Prefer manual `Canvas` + `Scrollbar` when:

- you need highly customized scrolling or virtualized rendering

---

## Related widgets

- **Scrollbar** — low-level scrollbar primitive
- **ScrolledText** — scrollable text widget
- **Frame** — common content container inside a scroll view

---

## Reference

- **API Reference:** `ttkbootstrap.ScrollView`
