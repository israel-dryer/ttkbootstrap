---
title: Label
icon: fontawesome/solid/align-left
---


# Label

`Label` wraps `ttk.Label` with localization, icon, bootstyle, and signal support so you can display text or icons that stay in sync with the rest of your themed UI.

---

## Overview

ttkbootstrap labels provide:

- `bootstyle`, `surface_color`, and `style_options` for consistent theming without manual `ttk.Style` work.
- Icon support via `icon`/`icon_only` and `compound` so graphics align with text or replace it entirely.
- Localization helpers (`localize="auto"`, `textsignal`) to react to runtime translations.
- Signal-friendly binding through `textsignal` or `textvariable` (and `SignalMixin`/`TextSignalMixin` under the hood).
- Standard `ttk.Label` options (`padding`, `wraplength`, `foreground`, `relief`, etc.) remain available.

Use `Label` for titles, value displays, or status text where simple formatting and theming matter.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(title="Label Demo", theme="cosmo")

status = ttk.Signal("Ready")

ttk.Label(
    app,
    textsignal=status,
    bootstyle="info",
    icon="circle-check",
    compound="left"
).pack(fill="x", padx=16, pady=(16, 4))

ttk.Button(app, text="Start", command=lambda: status.set("Running...")).pack(padx=16)

app.mainloop()
```

---

## Styling & variants

- `bootstyle` describes intent (`secondary`, `info`, `muted`, etc.) and controls text/icon colors automatically.
- `surface_color` overrides the label background surface when you need contrast against a split layout.
- For icon-only badges, simply set `icon_only=True` when you construct the widget.
- `font`, `foreground`, `justify`, and `anchor` come straight from `ttk.Label` and behave as expected.

Combine labels with `LabelFrame`, `Frame`, or layout managers to build consistent form rows, headers, or status bars.

---

## Icons, localization & signals

- `icon` supports any icon spec understood by the theme and pairs with text via `compound`.
- `icon_only=True` removes extra text padding so icon-only badges stay compact.
- Set `localize=True` or `localize="auto"` to have the label participate in your localization engine.
- `textsignal` (or `textvariable`) keeps the label content reactive to external state, especially when paired with `Signal` objects.
- For plain static labels you can still pass `text` or `image`.

---

## When to use Label

Use `Label` anywhere you would normally use `ttk.Label` but want theme-aware colors, icons, or reactive text. It's ideal for headings, field labels, validation hints (in combination with `Form`), and status indicators.

If you need editable text, swap to `TextEntry`; for button-like actions, consider `Button` or `MenuButton`.

---

## Related widgets

- `Button` (when users click on text)
- `LabelFrame` (for framed sections)
- `Form` (labels paired with fields)
- `TextEntry` (for editable labels)
