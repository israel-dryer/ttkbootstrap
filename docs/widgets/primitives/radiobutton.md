---
title: Radiobutton
icon: fontawesome/solid/circle-dot
---

# Radiobutton

Radiobuttons represent a **mutually exclusive choice** within a group. In ttkbootstrap v2, `Radiobutton` builds on
`ttk.Radiobutton`, adding semantic styling, theme-aware indicators, icon support, localization, and reactive
signals—while preserving standard Tk behavior.

---

## Overview

Radiobuttons are used when a user must choose **exactly one option** from a defined set.

ttkbootstrap radiobuttons:

- share a linked variable or signal
- visually communicate selection clearly
- follow the active theme automatically
- support icons and localization
- integrate cleanly with toolbutton-style UIs

---

## Quick Example

```python
import ttkbootstrap as ttk

choice = ttk.StringVar(value="daily")

ttk.Radiobutton(
    parent,
    text="Daily",
    value="daily",
    variable=choice,
    bootstyle="primary",
).pack(anchor="w")

ttk.Radiobutton(
    parent,
    text="Weekly",
    value="weekly",
    variable=choice,
).pack(anchor="w")
```

---

## Selection Behavior

Radiobuttons work as a group:

- all radiobuttons in the group share the same `variable` or `signal`
- selecting one automatically deselects the others
- each button provides a distinct `value`

This makes radiobuttons ideal for mode selection, preferences, and mutually exclusive settings.

---

## Visual Indicator

Radiobuttons use a circular indicator to represent selection state.

- unselected
- selected
- focused
- disabled

The indicator is recolored dynamically to match the active theme and state.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-radiobutton-indicator-states.png -->
<!-- Normal / selected / focused / disabled -->

---

## Icons and Labels

Radiobuttons may include icons alongside their labels.

```python
ttk.Radiobutton(
    parent,
    text="Wi-Fi",
    icon="wifi",
    value="wifi",
    variable=choice,
)
```

Icons are recolored automatically based on the active theme and widget state.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-radiobutton-icon.png -->

---

## Toolbutton Styles

Radiobuttons also participate in **toolbutton styles**, which are optimized for icon-centric, selectable controls such
as:

- toolbars
- segmented controls
- calendars and date pickers
- mode selectors

Toolbutton styles emphasize selection state over labels and are documented separately.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-radiobutton-toolbutton.png -->
<!-- Segmented or toolbar-style radiobuttons -->

---

## Variables, Signals, and Localization

Radiobuttons can be bound to traditional Tk variables or reactive signals.

- `variable` connects to a `StringVar`, `IntVar`, or similar
- `signal` allows reactive selection updates
- `localize` controls whether labels participate in localization

```python
# Conceptual example
# mode = Signal("list")
# ttk.Radiobutton(text="Grid", value="grid", signal=mode)
```

---

## Common Options

In addition to all standard `ttk.Radiobutton` options, the most commonly used ttkbootstrap options include:

- `text`
- `value`
- `variable` / `signal`
- `bootstyle`
- `icon`
- `state`
- `localize`

---

## Related Widgets

- **Checkbutton** — boolean or toggle-style choices
- **Toolbutton** — selectable toolbar controls
- **Form** — grouped selection inputs
