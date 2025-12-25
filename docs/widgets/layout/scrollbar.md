---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


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

## Overview

Use `Scrollbar` when:

- you need explicit scroll control for a widget that supports view commands

- you are building your own scrollable composite

If you want an out-of-the-box scrollable container, prefer **ScrollView** or **ScrolledText** (for text content).

---

## Basic usage

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

## Common options

### `orient`

```python
ttk.Scrollbar(app, orient="vertical")
ttk.Scrollbar(app, orient="horizontal")
```

### `command`

Hook to the target widget’s view method (`xview` or `yview`).

```python
ttk.Scrollbar(app, orient="vertical", command=widget.yview)
```

### Styling

Use `bootstyle` (or `style=`) to match your theme:

```python
ttk.Scrollbar(app, bootstyle="secondary")
```

---

## Behavior

- Scrollbars are driven by the target widget’s view commands.

- The target widget must also set `xscrollcommand` / `yscrollcommand` to update the scrollbar thumb.

---

## When should I use Scrollbar?

Use `Scrollbar` when:

- you’re wiring scroll behavior manually (Text, Canvas, custom composites)

Prefer **ScrollView** when:

- you want a scrollable container for arbitrary widgets

Prefer **ScrolledText** when:

- you need multi-line text with built-in scrolling

---

## Related widgets

- **ScrollView** — scroll container for arbitrary widgets

- **ScrolledText** — scrollable text control

- **Canvas** / **Text** — common scroll targets

---

## Reference

- **API Reference:** `ttkbootstrap.Scrollbar`

---

## Additional resources

### Related widgets

- [Frame](frame.md)

- [LabelFrame](labelframe.md)

- [PanedWindow](panedwindow.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Scrollbar`](../../reference/widgets/Scrollbar.md)
