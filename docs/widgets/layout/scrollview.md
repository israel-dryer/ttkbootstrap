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

# Get the content frame and add widgets to it
content = sv.add()
for i in range(30):
    ttk.Label(content, text=f"Row {i+1}").pack(anchor="w", pady=4)

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

### Adding content

Use `add()` to get a content frame for placing widgets.

```python
sv = ttk.ScrollView(app)
sv.pack(fill="both", expand=True)

content = sv.add()  # Returns a Frame
for i in range(30):
    ttk.Label(content, text=f"Item {i+1}").pack(anchor="w", pady=4)
```

Frame options (padding, color, etc.) can be passed directly:

```python
content = sv.add(padding=10, accent="primary")
```

Calling `add()` multiple times returns the same frame (idempotent).

### Custom content widget

You can also pass your own widget to `add()`:

```python
my_frame = ttk.Frame(sv.canvas, padding=16)
sv.add(my_frame)

ttk.Label(my_frame, text="Custom frame with padding").pack()
```

### Scroll direction

Choose vertical, horizontal, or both scrolling depending on content.

```python
ttk.ScrollView(app, scroll_direction='vertical')    # default
ttk.ScrollView(app, scroll_direction='horizontal')
ttk.ScrollView(app, scroll_direction='both')
```

### Scrollbar visibility

Use auto-hide policies to keep UI clean.

```python
ttk.ScrollView(app, scrollbar_visibility='always')    # default
ttk.ScrollView(app, scrollbar_visibility='never')     # hidden but scrolling works
ttk.ScrollView(app, scrollbar_visibility='hover')     # appear on mouse enter
ttk.ScrollView(app, scrollbar_visibility='scroll')    # appear when scrolling
```

### Padding

Add padding to your content frame:

```python
content = sv.add()
inner = ttk.Frame(content, padding=16)
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