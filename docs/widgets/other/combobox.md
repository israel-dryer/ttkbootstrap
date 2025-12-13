---
title: Combobox
icon: fontawesome/solid/chevron-down
---

# Combobox

`Combobox` allows users to select a value from a predefined list, optionally allowing free text entry.
In ttkbootstrap v2, `Combobox` extends `ttk.Combobox` with bootstyle variants, theme-aware popdown styling, icons,
localization, and reactive signals, while preserving native Tk behavior.

---

## Overview

Use a Combobox when:

- users should choose from a known set of values,
- screen space is limited compared to list-based controls,
- free-form input may be allowed (non-readonly mode).

ttkbootstrap’s Combobox improves on the native widget by:

- styling the dropdown list to match the active theme,
- recoloring the chevron indicator and field consistently,
- automatically reapplying styles when the theme changes,
- integrating cleanly with signals and localization.

---

## Quick Example

```python
import ttkbootstrap as ttk

app = ttk.Window()

combo = ttk.Combobox(
    app,
    values=["Low", "Medium", "High"],
    state="readonly",
    bootstyle="primary",
)

combo.pack(padx=16, pady=16)
app.mainloop()
```

---

## Editable vs Readonly

Combobox behavior depends on its state.

### Readonly Combobox

- selection is restricted to listed values
- recommended for settings and forms
- prevents invalid input

```python
ttk.Combobox(state="readonly")
```

### Editable Combobox

- users may type arbitrary text
- suitable for filtering or search-like inputs

```python
ttk.Combobox(state="normal")
```

---

## Dropdown Styling

Unlike the standard ttk Combobox, ttkbootstrap styles the popdown listbox:

- background and foreground colors match the active theme
- selection colors respect semantic tokens
- styling is applied lazily on first open
- styles are automatically reapplied on theme changes

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-combobox-popdown.png -->
<!-- Combobox opened, showing themed dropdown list -->

---

## Chevron Indicator

The dropdown chevron is part of the style system:

- recolored per widget state
- disabled styling applied automatically
- sized consistently with other controls

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-combobox-chevron.png -->
<!-- Close-up of chevron in normal vs disabled state -->

---

## Signals and Variables

Combobox supports both Tk variables and reactive signals.

- `textvariable` binds to a Tk variable
- `textsignal` binds to a reactive Signal
- both remain synchronized automatically

```python
# Conceptual example
# selection = Signal("Medium")
# ttk.Combobox(values=levels, textsignal=selection)
```

---

## Localization

Displayed values may participate in localization when `localize` is enabled.
This is useful when the underlying value is stable but the label should be translated.

---

## Common Options

In addition to standard ttk.Combobox options, commonly used ttkbootstrap options include:

- `values`
- `state` (`normal`, `readonly`, `disabled`)
- `bootstyle`
- `surface_color`
- `style_options`
- `textvariable`
- `textsignal`
- `postcommand`

---

## Related Widgets

- **OptionMenu** — value selection via menu
- **SelectBox** — list-based selection control
- **Entry** — free-form text input
- **DropdownButton** — menu-based actions
