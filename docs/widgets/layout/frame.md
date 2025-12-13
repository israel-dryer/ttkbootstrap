---
title: Frame
icon: fontawesome/regular/square-full
---


# Frame

`Frame` is a themed container that mirrors `ttk.Frame` but adds bootstyle, surface color, and border helpers so your layout building blocks stay in sync with the rest of the application.

---

## Overview

ttkbootstrap frames:

- accept `bootstyle`, `surface_color`, and `style_options` to match panel treatments and animated surfaces across themes.
- continue to expose `padding`, `relief`, `borderwidth`, `width`, `height`, `cursor`, and other native options for layout control.
- support `show_border` to toggle a subtle border without defining a custom style.
- behave exactly like their ttk counterpart in grid/pack/place layouts while leaning on ttkbootstrap’s style builder for consistent colors.

Use `Frame` whenever you need a layout surface whose background or border should honor the active theme rather than the default system colors.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

top_frame = ttk.Frame(app, padding=16, bootstyle="secondary-soft")
top_frame.pack(fill="x", pady=12)
ttk.Label(top_frame, text="Ingredients", font="bold").pack(side="left")

content = ttk.Frame(app, padding=16, bootstyle="white-space", show_border=True)
content.pack(fill="both", expand=True, padx=16, pady=8)
ttk.Label(content, text="Content goes here").pack()

app.mainloop()
```

---

## Layout & borders

- Nest `Frame` widgets with grid/pack/place to build cards, sections, and docked panels. They grant the same geometry semantics as `ttk.Frame`.
- `show_border=True` flips on a themed border token; combine with `surface_color` to match panels from your design system.
- Use `style_options` for extra tokens (`{"class": "Card"}`) when you need more refined styling from the builder.
- Pair frames with `LabelFrame`, `PanedWindow`, or `Notebook` for more structured layouts.

---

## When to use Frame

Pick `Frame` whenever you need a container that respects theme-aware surfaces or has Bootstyle-managed borders. For alignment-only wrappers, `ttk.Frame` works, but prefer `ttkbootstrap.Frame` if you want consistency with buttons, labels, and other themed primitives.

For floating content, consider `Toplevel` or `Dialog` controls.

---

## Related widgets

- `LabelFrame` (framed group with title)
- `PanedWindow` (split layouts)
- `Frame` (wait already here; keep in list for completeness)
