---
title: Scrollbar
icon: fontawesome/solid/grip-lines-vertical
---


# Scrollbar

`Scrollbar` wraps `ttk.Scrollbar` with bootstyle, surface color, and optional style tweaks so the scroll thumb and trough match your theme while still supporting commands, focus, and native geometry.

---

## Overview

Key points:

- Accepts `orient`, `command`, `takefocus`, and other native scrollbar options so you can bind it to canvases, text widgets, TreeViews, etc.
- Adds Bootstyle support (`bootstyle`, `surface_color`, `style_options`) so the thumb/tôngle tone matches your palette (`primary`, `danger-square`, `muted`, etc.).
- Works with all geometry managers and respects `state` (via ttk state map) just like the base widget.
- Can be styled via `style_options` if you need custom thickness, grip color, or other builder tokens without writing raw ttk styles.

Use `Scrollbar` whenever you need themed scrollbars for panels, lists, or canvas views to maintain consistent UI language.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

text = ttk.Text(app, width=40, height=10)
text.pack(side="left", fill="both", expand=True, padx=(16,0), pady=16)

for i in range(50):
    text.insert("end", f"Line {i+1}\n")

scroll = ttk.Scrollbar(
    app,
    orient="vertical",
    command=text.yview,
    bootstyle="secondary",
)
scroll.pack(side="left", fill="y", pady=16, padx=(0,16))

text.configure(yscrollcommand=scroll.set)

app.mainloop()
```

---

## Styling tips

- `bootstyle` defines both thumb and trough colors; pair with `surface_color` when embedding the scrollbar against muted surfaces.
- Use `style_options` to feed builder tokens (e.g., `{"thickness": 12}`) when you need bigger handles or custom spacing.
- `takefocus` determines whether the scrollbar participates in keyboard focus; set it to `False` in mouse-only panels.
- Combine with `Frame`, `ScrollView`, or any canvas/paned view to give your scrolling chrome a polished theme look.

---

## Related widgets

- **ScrollView**
- **ScrolledText**

