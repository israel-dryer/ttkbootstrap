---
title: ToolTip
icon: fontawesome/solid/message
---


# ToolTip

`ToolTip` creates lightweight, themable popups that follow the mouse or anchor to a specific widget point, perfect for clarifying controls, status indicators, or form fields.

---

## Overview

ToolTip builds a `Toplevel` window styled with Bootstrap tokens and:

- shows after a short `delay` and disappears on hover exit or mouse click,
- follows the cursor by default but can also anchor to a widget edge via `anchor_point`/`window_point`,
- supports custom `bootstyle`, `padding`, `justify`, `wraplength`, and optional `image` content,
- auto-flips when near screen edges so it stays visible.

Use ToolTip whenever you want explanatory text that lives outside the layout without permanent labels or busy toolbars.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

btn = ttk.Button(app, text="Hover me")
btn.pack(padx=20, pady=40)

ttk.ToolTip(btn, text="Default tooltip shows after a short delay")

danger_btn = ttk.Button(app, text="Styled tip")
danger_btn.pack(padx=20, pady=(0, 40))

ttk.ToolTip(
    danger_btn,
    text="Danger tooltips use the danger bootstyle",
    bootstyle="danger",
    wraplength=200,
)

app.mainloop()
```

---

## Positioning & behavior

- By default the tooltip follows the mouse pointer and keeps a small offset (`_MOUSE_OFFSET_X`/`Y`) from the cursor.
- To anchor to the widget, pass `anchor_point` (n/e/s/w/corners) and optionally `window_point`; `auto_flip` keeps it on-screen.
- Customize transparency and stacking via additional `**kwargs` such as `alpha=0.95` or `topmost=True`.
- ToolTip binds `<Enter>/<Leave>/<Motion>/<ButtonPress>` automatically and offers `destroy()` for manual cleanup.

---

## When to use ToolTip

Use ToolTip for lightweight help copy, keyboard shortcut hints, or status badges where a permanent label would clutter the layout.

For persistent callouts consider `Toast`, and for inline validation messages favor `Field` widgets with their `message` areas.

---

## Related widgets

- `Toast` (persistent feedback)
- `Field` (built-in validation messaging)
- `Button` / `Entry` (common tooltip targets)
