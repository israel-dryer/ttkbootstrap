---
title: Scale
icon: fontawesome/solid/sliders
---


# Scale

`Scale` is a **themed ttk.Scale wrapper** that adds ttkbootstrap bootstyle tokens, surface colors, and signal wiring to the familiar slider control.

Use it when you need a thumb slider for numeric input, volume controls, brightness tweaks, or any continuous range selection with consistent, theme-aware styling.

---

## Overview

Key features of `Scale`:

- Exposes all `ttk.Scale` options (`from_`, `to`, `orient`, `length`, `command`, etc.) with themed defaults.
- Supports `bootstyle`, `surface_color`, and `style_options` to tune appearance without touching raw styles.
- Mixes in `SignalMixin`, so you can supply a reactive `Signal` object instead of a `variable`.
- Works with `ttkbootstrap` variables or plain `tk` variables and keeps the `command` callback for imperative hooks.

`Scale` is minimal but flexible, allowing horizontal or vertical tracks, optional notation, and automatic theming.

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap import Signal

app = ttk.App(title="Scale Demo", theme="cosmo")

value_signal = Signal(50)

scale = ttk.Scale(
    app,
    bootstyle="primary",
    from_=0,
    to=100,
    orient="horizontal",
    length=300,
    signal=value_signal,
)
scale.pack(padx=24, pady=24)

label = ttk.Label(app, textvariable=value_signal)
label.pack(pady=(0, 16))

app.mainloop()
```

---

## Appearance & customization

- `bootstyle` defines semantic colors (`primary`, `danger`, etc.) and works without manual style creation.
- `surface_color` overrides the surface token for the track background when you need a darker/light look.
- `style_options` accepts a dict that is forwarded to the style builder (e.g., `{"gripcolor": "secondary"}`).
- The underlying Tcl widget honors `orient="vertical"` plus `length` to draw tall sliders.
- Provide `command` to react imperatively, or use `signal`/`variable` for reactive bindings.

You can also configure `takefocus`, `cursor`, `state`, and other native ttk options as you would with a `ttk.Scale`.

---

## Events, signals & variables

- `command` fires with the new float value whenever the thumb moves.
- Supply a `Signal` from `ttkbootstrap.core.signals` to keep the slider synced with other widgets; the `SignalMixin` auto-updates the bound variable.
- Alternatively, pass a `variable` (Tk `DoubleVar`/`IntVar`) for two-way binding.
- `Scale` emits the standard `<<VariableChanged>>` signal when tied to a `Signal` or Tk variable, making it easy to hook other widgets.

For accessibility, `Scale` honors keyboard controls (arrow keys, PageUp/PageDown) inherited from `ttk.Scale`.

---

## When to use Scale

Choose `Scale` for continuous numeric controls: volume, threshold, progress tuning, or any range input that benefits from a slider. It keeps the interface aligned with ttkbootstrap theming while offering both imperative callbacks and reactive signals.

For discrete choices, consider `SpinnerEntry` or `SelectBox`; for simple numeric typing, use `NumericEntry`.

---

## Related widgets

- `SpinnerEntry`
- `NumericEntry`
- `SelectBox`
- `Form`
