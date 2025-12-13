---
title: Entry
icon: fontawesome/solid/i-cursor
---


# Entry

`Entry` wraps `tkinter.Entry` with the ttkbootstrap mixins so you get themed text inputs, bootstyle-aware backgrounds, and signal/localization helpers while still relying on the raw, single-line widget.

---

## Overview

- Supports every `ttk.Entry` option plus `bootstyle`, `surface_color`, and `style_options` tokens for consistent coloring across your UI.
- Mixes in `TextSignalMixin`, so you can pass `textvariable` or a `Signal` to keep the text reactive without extra glue.
- Honors localization (`localize="auto"`) and icon/value formatting helpers when you attach images or icons.
- Behaves like a normal `ttk.Entry` for geometry managers and keyboard handling, but aligns with your theme tokens.

Use `Entry` anywhere you need a minimal, single-line text field without the additional form/field wrappers provided by `TextEntry` or `PasswordEntry`.

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap import Signal

app = ttk.App(theme="cosmo")

sig = Signal("Hello")
entry = ttk.Entry(app, textsignal=sig, bootstyle="secondary", justify="center")
entry.pack(padx=16, pady=16)

ttk.Button(app, text="Print value", command=lambda: print("value:", sig.get())).pack()

app.mainloop()
```

---

## Styling & signals

- `bootstyle` chooses the accent color (`primary`, `success`, etc.), and `surface_color` tweaks the fill.
- `style_options` forwards builder tokens (e.g., `{"padding": (4, 4)}`) for finer control.
- `textsignal` or `textvariable` ensure other widgets stay in sync with the typed value; `Signal` objects auto-update the entry text.
- For labeled forms, prefer `TextEntry` when you need validation, messaging, or structured events.

---

## Related widgets

- `TextEntry` / `PasswordEntry` (Field-based composites with labels/validation)
- `Form` (layout around Entry controls)
- `ToolTip` (inline guidance for the entry)
