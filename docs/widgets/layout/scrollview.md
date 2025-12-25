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

## Quick start

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

## When to use

Use `ScrollView` when:

- you need to scroll a region that contains normal widgets (forms/panels/cards)

- you want to scroll long forms, settings panels, or stacked content

- you want to build resizable layouts where only part of the UI scrolls

- you want to avoid manual Canvas/Scrollbar plumbing

**Consider a different control when:**

- you need a multi-line text editor/log output -- use [ScrolledText](../inputs/scrolledtext.md)

- you need highly customized scrolling or virtualized rendering -- use manual [Canvas](../primitives/canvas.md) + [Scrollbar](scrollbar.md)

---

## Appearance

`ScrollView` is different from `ScrolledText`:

- `ScrollView` scrolls **widgets**

- `ScrolledText` scrolls **text content** (tk.Text)

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

---

## Examples & patterns

### Core concept

A `ScrollView` exposes an interior "content" region (the widget itself acts as the content parent in most APIs).
You pack/grid your widgets into that region; `ScrollView` manages the viewport and scrollbars around it.

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

## Additional resources

### Related widgets

- [Scrollbar](scrollbar.md) -- low-level scrollbar primitive

- [ScrolledText](../inputs/scrolledtext.md) -- scrollable text widget

- [Frame](frame.md) -- common content container inside a scroll view

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- [`ttkbootstrap.ScrollView`](../../reference/widgets/ScrollView.md)