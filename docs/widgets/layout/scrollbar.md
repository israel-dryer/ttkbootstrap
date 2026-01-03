---
title: Scrollbar
---

# Scrollbar

`Scrollbar` is the themed scrollbar primitive used to scroll content such as `Text`, `Canvas`, and ttk widgets that support
`xview` / `yview`.

It wraps `ttk.Scrollbar` and participates in ttkbootstrap styling.

<!--
IMAGE: Vertical + horizontal scrollbar next to a Text or Canvas
Theme variants: light / dark
-->

---

## Quick start

### With a Text widget

```python
import tkinter as tk
import ttkbootstrap as ttk

app = ttk.App()

frame = ttk.Frame(app)
frame.pack(fill="both", expand=True, padx=20, pady=20)

text = tk.Text(frame, wrap="none")
text.grid(row=0, column=0, sticky="nsew")

ys = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
ys.grid(row=0, column=1, sticky="ns")

xs = ttk.Scrollbar(frame, orient="horizontal", command=text.xview)
xs.grid(row=1, column=0, sticky="ew")

text.configure(xscrollcommand=xs.set, yscrollcommand=ys.set)

frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

app.mainloop()
```

---

## When to use

Use `Scrollbar` when:

- you need explicit scroll control for a widget that supports view commands

- you're wiring scroll behavior manually (Text, Canvas, custom composites)

**Consider a different control when:**

- you want a scrollable container for arbitrary widgets -- use [ScrollView](scrollview.md)

- you need multi-line text with built-in scrolling -- use [ScrolledText](../inputs/scrolledtext.md)

---

## Appearance

### Styling

Use `accent` (or `style=`) to match your theme:

```python
ttk.Scrollbar(app, accent="secondary")
```

!!! link "Design System"
    For theming details and color tokens, see [Design System](../../design-system/index.md).

---

## Examples & patterns

### `orient`

```python
ttk.Scrollbar(app, orient="vertical")
ttk.Scrollbar(app, orient="horizontal")
```

### `command`

Hook to the target widget's view method (`xview` or `yview`).

```python
ttk.Scrollbar(app, orient="vertical", command=widget.yview)
```

---

## Behavior

- Scrollbars are driven by the target widget's view commands.

- The target widget must also set `xscrollcommand` / `yscrollcommand` to update the scrollbar thumb.

- If you want an out-of-the-box scrollable container, prefer [ScrollView](scrollview.md) or [ScrolledText](../inputs/scrolledtext.md) (for text content).

---

## Additional resources

### Related widgets

- [ScrollView](scrollview.md) -- scroll container for arbitrary widgets

- [ScrolledText](../inputs/scrolledtext.md) -- scrollable text control

- [Canvas](../primitives/canvas.md) / [Text](../primitives/text.md) -- common scroll targets

### Framework concepts

- [Layout Properties](../../capabilities/layout-props.md)

- [Layout](../../platform/geometry-and-layout.md)

### API reference

- [`ttkbootstrap.Scrollbar`](../../reference/widgets/Scrollbar.md)