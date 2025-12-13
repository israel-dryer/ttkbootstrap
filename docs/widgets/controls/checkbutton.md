---
title: CheckButton
icon: fontawesome/solid/square-check
---

# CheckButton

CheckButtons represent a boolean or tri-state choice. In ttkbootstrap v2, `CheckButton` extends `ttk.Checkutton` with
semantic styling, theme-aware indicators, icons, localization, and reactive signals—while remaining fully compatible
with Tk’s native behavior.

---

## Overview

CheckButtons are commonly used in forms, settings panels, and toolbars to represent on/off or optional features.

ttkbootstrap checkbuttons are designed to:

- express intent using semantic styles (`primary`, `success`, etc.)
- support both checkbox and toggle (switch-style) presentations
- integrate with variables or reactive signals
- participate naturally in localization and theming

---

## Quick Example

```python
import ttkbootstrap as ttk

var = ttk.BooleanVar(value=True)

ttk.CheckButton(
    parent,
    text="Enable notifications",
    variable=var,
    bootstyle="primary",
).pack(padx=16, pady=8)
```

---

## Checkbox and Toggle Styles

The same `CheckButton` widget can be rendered in two distinct visual styles depending on intent.

### Checkbox (default)

The classic checkbox style:

- supports checked, unchecked, and indeterminate states
- commonly used in forms and option lists
- emphasizes precision over immediacy

```python
ttk.CheckButton(
    parent,
    text="Send usage data",
    variable=var,
)
```

### Toggle (switch-style)

The toggle style uses a switch metaphor:

- two-state only (on/off)
- commonly used in settings panels
- emphasizes quick enable/disable actions

```python
ttk.CheckButton(
    parent,
    text="Dark mode",
    bootstyle="toggle",
)
```

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-checkbutton-toggle-vs-checkbox.png -->
<!-- Side-by-side comparison of checkbox vs toggle styles -->

---

## States and Interaction

CheckButtons support the full ttk state model:

- selected
- not selected
- alternate (indeterminate)
- disabled
- focused

The active theme controls how these states are rendered, ensuring clear feedback for both mouse and keyboard users.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-checkbutton-states.png -->
<!-- Checked / unchecked / disabled / focused examples -->

---

## Icons and Labels

CheckButtons may include icons alongside their labels.

```python
ttk.CheckButton(
    parent,
    text="Wi-Fi",
    icon="wifi",
    bootstyle="toggle",
)
```

Icons are recolored automatically to match the current theme and widget state.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-checkbutton-icon.png -->
<!-- Toggle-style checkbutton with an icon -->

---

## Variables, Signals, and Localization

CheckButtons can be bound to traditional Tk variables or reactive signals.

- `variable` connects to a `BooleanVar`, `IntVar`, or similar
- `signal` allows state to be driven reactively
- `localize` controls whether the label participates in localization

```python
# Conceptual example
# enabled = Signal(False)
# ttk.CheckButton(text="Sync automatically", signal=enabled)
```

This makes checkbuttons suitable for dynamic settings and localized applications.

---

## Toolbutton Styles

CheckButtons also participate in **toolbutton styles**, which are optimized for icon-centric, selectable UI elements
such as toolbars and context menus.

Toolbutton styles emphasize selection state over labels and are documented separately.

---

## Common Options

In addition to all standard `ttk.Checkbutton` options, the most commonly used ttkbootstrap options include:

- `bootstyle`
- `text`
- `variable` / `signal`
- `onvalue` / `offvalue`
- `icon`
- `state`
- `localize`

---

## Related Widgets

- **RadioButton** — mutually exclusive choices
- **ToolButton** — selectable toolbar buttons
- **Form** — structured input groups
- **ContextMenu** — selectable menu items
