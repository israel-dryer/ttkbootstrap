---
title: ScrollView
icon: fontawesome/solid/border-top-left
---


# ScrollView

`ScrollView` is a canvas-backed scroll container that extends `Frame` so you can drop in scrollable areas with consistent bootstyle scrollbars, mouse-wheel support, and smart visibility modes.

---

## Overview

Key capabilities:

- Supports `direction='vertical'`, `'horizontal'`, or `'both'` for 1D/go multi-axis scrolling with Shift+wheel handling.
- Scrollbars respect `bootstyle`, `surface_color`, and the `scrollbar_style` override, keeping the track and thumb in the theme palette.
- Visibility modes (`always`, `never`, `on-hover`, `on-scroll`) control when scrollbars appear; `autohide_delay` defines how long they stay visible after activity.
- Mouse-wheel bindings are automatically propagated to all child widgets (even nested ones) via bind tags; call `refresh_bindings()` after major content changes.
- Works with `add(widget)`/`remove()` and exposes `xview`/`yview` helpers so you treat it like a usual canvas scroll area.

Use ScrollView whenever you need scrollable cards, documentation panels, or any deeply nested widgets that need consistent scrolling treatment.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

scroll = ttk.ScrollView(
    app,
    direction="vertical",
    show_scrollbar="on-scroll",
    scrollbar_style="secondary",
)
scroll.pack(fill="both", expand=True, padx=16, pady=16)

content = ttk.Frame(scroll.canvas)
for i in range(30):
    ttk.Label(content, text=f"Line {i+1}").pack(anchor="w", pady=2)

scroll.add(content)

app.mainloop()
```

---

## Scrollbar behaviors

- `show_scrollbar` controls visibility: `'always'` keeps them visible, `'never'` hides them entirely, `'on-hover'` reveals them when the pointer enters the view, and `'on-scroll'` shows them during scrolling and auto-hides after `autohide_delay`.
- Adjust `scrollbar_style`/`bootstyle` to align the slider with your theme; set `surface_color` on the containing frame when you need contrast.
- `direction='both'` adds horizontal/vertical scrollbars; horizontal scrolling is available via Shift+wheel or programmatic commands (`xview`, `xview_moveto`).

---

## Content & binding helpers

- Add content with `scroll.add(widget)`; you may only host one widget (typically a `Frame`) inside the canvas, but you can pack/grids more widgets inside that child frame.
- Call `scroll.refresh_bindings()` after dynamically adding many widgets to ensure mouse-wheel support stays intact.
- Use `scroll.enable_scrolling()/disable_scrolling()` if you need to temporarily freeze wheel input (handled automatically based on `show_scrollbar` mode).
- `remove()` detaches the current child and returns it if you need to swap views.

---

## When to use ScrollView

Choose ScrollView for scrollable panels such as log viewers, settings lists, or form bodies with variable length. It removes boilerplate for wiring canvas scrollbars and ensures mouse-wheel works everywhere.

For simple one-off scrolling use `ScrolledText`; for tabular data prefer `TableView` or `TreeView`.

---

## Related widgets

- `Frame` (wrap content before adding)
- `ScrollBar` (custom standalone scrollbars)
- `Label`/`Entry` (common scroll targets)
