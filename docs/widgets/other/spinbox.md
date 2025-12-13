---
title: Spinbox
icon: fontawesome/solid/sort
---


# Spinbox

`Spinbox` wraps `ttk.Spinbox` so you can use bootstyle colors and reactive `Signal` bindings while keeping the same numeric stepping behavior.

---

## Overview

- Supports `from_`, `to`, `increment`, `values`, and `wrap` plus the usual ttk options (`width`, `state`, `cursor`).
- Mixes in `TextSignalMixin` so you can pass a `Signal` or `textvariable` and react to text changes declaratively.
- `format` controls how the displayed text renders, and `style_options` forwards extra builder tokens when you need custom thickness or padding.
- Works with `command` callbacks triggered after each value change and exposes mouse/keyboard stepping automatically.

Use `Spinbox` whenever you need a bootstyle-aware spinner or stepping control without building a full `NumericEntry`.

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap import Signal

app = ttk.App(theme="cosmo")

amount = Signal(5)
spinner = ttk.Spinbox(
    app,
    from_=0,
    to=10,
    textsignal=amount,
    bootstyle="secondary",
    width=10
)
spinner.pack(padx=16, pady=16)

ttk.Label(app, textvariable=amount).pack()

app.mainloop()
```

---

## When to use Spinbox

Choose `Spinbox` for compact numeric steppers where you only need built-in ttk functionality plus theme-aware styling. For richer validation or field-level messaging prefer `NumericEntry`.

---

## Related widgets

- `NumericEntry` (rich, field-oriented spinner)
- `SelectBox` (dropdown alternative)
