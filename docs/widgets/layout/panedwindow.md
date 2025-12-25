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

title: PanedWindow
---

# PanedWindow

`PanedWindow` is a **resizable split container** that arranges child panes with draggable separators.

It wraps `ttk.Panedwindow` and is used to build layouts like:

- sidebar + content

- navigator + editor + inspector

- vertically stacked regions with adjustable heights

<!--
IMAGE: PanedWindow splitting sidebar/content
Theme variants: light / dark
-->

---

## Overview

Use `PanedWindow` when you want users to control how space is distributed between major regions of your UI.

A paned layout works well when:

- panes have different importance (content gets most space)

- users may want to expand/collapse a region temporarily

- window resizing should feel responsive

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

pw = ttk.PanedWindow(app, orient="horizontal")
pw.pack(fill="both", expand=True)

sidebar = ttk.Frame(pw, padding=12, width=220)
content = ttk.Frame(pw, padding=12)

pw.add(sidebar, weight=0)
pw.add(content, weight=1)

ttk.Label(sidebar, text="Sidebar").pack(anchor="w")
ttk.Label(content, text="Content").pack(anchor="w")

app.mainloop()
```

---

## Core concepts

### Panes

Each child added to a paned window is a *pane*. You can assign weights (if supported) to influence how extra space is distributed.

### Sashes

The draggable separators between panes are called *sashes*. Users drag sashes to resize panes.

---

## Common options

### `orient`

```python
ttk.PanedWindow(app, orient="horizontal")  # left/right
ttk.PanedWindow(app, orient="vertical")    # top/bottom
```

### Adding panes: `add(...)`

```python
pw.add(frame)
pw.add(frame, weight=1)
```

### Removing panes

Use the ttk panedwindow API (varies by implementation/version).

---

## Behavior

- Users drag the sash to resize adjacent panes.

- Panes can be sized by the program (e.g., setting widths/heights + disabling propagation on child frames).

- If you need collapsible panes, pair with explicit show/hide controls and remember prior sash positions.

---

## UX guidance

- Don’t overuse panes—2 (or 3) is usually enough.

- Provide sensible default sizes.

- Consider minimum sizes for panes that contain dense UI (lists, trees, inspectors).

---

## When should I use PanedWindow?

Use `PanedWindow` when:

- users benefit from adjustable regions

- your app has a “workbench” layout (nav/editor/inspector)

Prefer plain layout containers when:

- the layout should be fixed

- resizing regions would add complexity without benefit

---

## Related widgets

- **Frame** — typical pane content container

- **Separator** — lightweight alternative when panes are fixed

- **ScrollView** — scroll content within a pane

---

## Reference

- **API Reference:** `ttkbootstrap.PanedWindow`

---

## Additional resources

### Related widgets

- [Frame](frame.md)

- [LabelFrame](labelframe.md)

- [Scrollbar](scrollbar.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.PanedWindow`](../../reference/widgets/PanedWindow.md)
