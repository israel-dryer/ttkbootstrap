---
title: ToolTip
icon: fontawesome/solid/message
---

# Tooltip

`ToolTip` is a lightweight helper that displays short, contextual information when the user hovers a widget. It provides discoverable guidance without adding permanent visual clutter and supports both mouse-following and anchored positioning modes.

<!--
IMAGE: Basic tooltip on hover
Suggested: Button with mouse-hover tooltip visible
Theme variants: light / dark
-->

---

## Basic usage

Attach a tooltip to any Tk or ttk widget:

```python
import ttkbootstrap as ttk

app = ttk.App()

btn = ttk.Button(app, text="Hover me")
btn.pack(padx=20, pady=20)

ttk.ToolTip(btn, text="This button launches the wizard.")
app.mainloop()
```

The tooltip appears after a short delay when the mouse enters the widget and hides automatically when the mouse leaves or the user clicks.

<!--
IMAGE: Simple tooltip attached to a button
Suggested: Button widget with visible tooltip after hover delay
-->

---

## What problem it solves

Desktop applications often need to explain *what something does* without permanently occupying screen space. `ToolTip` solves this by providing:

- Delayed show-on-hover behavior (prevents flicker)
- Screen-safe positioning
- Optional anchored positioning
- Automatic flipping when near screen edges

---

## Core concepts

### Mouse-following vs anchored tooltips

#### Mouse-following (default)

If no anchor is provided, the tooltip follows the mouse cursor with a small offset.

```python
ttk.ToolTip(btn, text="Follows the cursor")
```

This mode is best for simple hints and icon-only controls.

<!--
IMAGE: Mouse-following tooltip
Suggested: Cursor with tooltip offset following pointer
-->

#### Anchored tooltips

If an `anchor_point` is provided, the tooltip is positioned relative to the widget itself and does **not** track mouse movement.

```python
ttk.ToolTip(
    btn,
    text="Anchored below the button",
    anchor_point="s",
    window_point="n",
)
```

If `window_point` is omitted, the tooltip automatically chooses the opposite side of the anchor for natural placement.

<!--
IMAGE GROUP: Anchored tooltip positioning
- Tooltip anchored south of widget
- Tooltip anchored north of widget
-->

---

### Auto-flip (screen-safe positioning)

Anchored tooltips can automatically flip if they would appear offscreen.

```python
ttk.ToolTip(
    btn,
    text="Smart positioning",
    anchor_point="e",
    auto_flip=True,
)
```

Supported values:

- `True` (default): flip vertically and horizontally
- `"vertical"`: flip up/down only
- `"horizontal"`: flip left/right only
- `False`: disable flipping

This ensures tooltips remain visible even near screen edges.

<!--
IMAGE GROUP: Auto-flip behavior
- Tooltip near bottom edge flipping upward
- Tooltip near right edge flipping left
-->

---

### Styling and content

- Tooltips use a dedicated tooltip style (`*-tooltip`)
- Text uses the `caption` font
- Long text is wrapped automatically using `wraplength`
- An optional image may be displayed below the text

```python
ttk.ToolTip(
    btn,
    text="Wrapped tooltip text",
    wraplength=220,
)
```

<!--
IMAGE: Wrapped tooltip text
Suggested: Narrow tooltip showing multi-line wrapped content
-->

---

## Events and lifecycle

`ToolTip` manages its own low-level event bindings:

- `<Enter>` schedules display
- `<Leave>` cancels and hides
- `<Motion>` updates position (mouse-follow mode only)
- `<ButtonPress>` hides immediately

!!! note "Cleanup"
    If you dynamically create or destroy widgets, call `tooltip.destroy()` to remove bindings and avoid orphaned callbacks.

---

## UX guidance

- Keep tooltip text short and scannable
- Use anchored tooltips near screen edges
- Increase `delay` for frequently-hovered widgets (tables, lists)

!!! tip "Reduce noise"
    For dense UIs, delays of 400–800ms feel calmer and prevent accidental popups.

---

## When to use / when not to

**Use Tooltip when:**

- Explaining icon-only controls
- Adding discoverable help without changing layout

**Avoid Tooltip when:**

- The information is required to complete the task
- Accessibility requires persistent, readable guidance

---

## Related widgets

- **Toast** — transient notifications
- **Dialogs** — confirmations and longer explanations
- **DropdownButton / OptionMenu** — common tooltip targets
