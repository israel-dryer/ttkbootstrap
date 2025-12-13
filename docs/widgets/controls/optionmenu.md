---
title: OptionMenu
icon: fontawesome/solid/list-ul
---

# OptionMenu

`OptionMenu` presents a single selected value from a list of options using a button-based dropdown.
In ttkbootstrap v2, `OptionMenu` is implemented as a MenuButton backed by a ContextMenu, providing a modern, theme-aware
alternative to Tk’s classic option menu.

---

## Overview

Use `OptionMenu` when:

- exactly one value should be selected from a list,
- screen space is limited,
- a dropdown interaction is preferred over radio groups.

Unlike Tk’s legacy option menu, ttkbootstrap’s `OptionMenu`:

- uses real widgets instead of menu hacks,
- supports icons, themes, and localization,
- emits structured change events,
- integrates naturally with toolbutton styles.

---

## Quick Example

```python
import ttkbootstrap as ttk

app = ttk.Window()

option = ttk.OptionMenu(
    app,
    value="Daily",
    options=["Daily", "Weekly", "Monthly"],
    bootstyle="primary-outline",
)

option.pack(padx=16, pady=16)
app.mainloop()
```

---

## How It Works

Internally, `OptionMenu` is composed of:

- a MenuButton (visible control)
- a ContextMenu (dropdown list)
- a shared StringVar or signal
- radiobutton-style menu items

This architecture allows the widget to behave like a real control instead of a legacy menu construct.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-optionmenu-structure.png -->
<!-- Button + dropdown menu relationship -->

---

## Value and Options

### Setting the Initial Value

```python
OptionMenu(
    value="Medium",
    options=["Low", "Medium", "High"],
)
```

Values are coerced to strings internally for consistency.

### Updating Options at Runtime

Options can be replaced dynamically:

```python
option.configure(options=["Small", "Medium", "Large"])
```

The underlying menu is rebuilt automatically.

---

## Change Events

When the selected value changes, `OptionMenu` emits a virtual event:

```
<<Changed>>
```

The event includes structured data:

```python
def on_changed(event):
    print(event.data["value"])


option.on_changed(on_changed)
```

---

## Signals and Localization

`OptionMenu` supports both traditional Tk variables and signals.

- `textvariable` binds to a StringVar
- `textsignal` binds to a reactive signal
- `localize` controls localization behavior

The displayed value updates automatically when the signal or variable changes.

---

## Visual Styling

### Bootstyle Variants

`OptionMenu` supports the same bootstyle variants as MenuButton:

- solid
- outline
- ghost
- text

```python
OptionMenu(bootstyle="secondary-ghost")
```

### Dropdown Indicator

The dropdown chevron can be hidden or customized:

```python
OptionMenu(show_dropdown_button=False)
```

```python
OptionMenu(dropdown_button_icon="caret-down-fill")
```

---

## Disabled and Read-Only States

`OptionMenu` respects standard ttk states:

- disabled — menu cannot be opened
- readonly — value cannot be changed

---

## Icons

Icons may be used on the button label:

```python
OptionMenu(
    icon="calendar",
    value="Today",
    options=["Today", "Tomorrow", "Next Week"],
)
```

Icons are recolored automatically to match theme and state.

---

## Common Options

Commonly used options include:

- value
- options
- bootstyle
- icon
- icon_only
- show_dropdown_button
- dropdown_button_icon
- textvariable
- textsignal
- surface_color
- style_options

---

## Related Widgets

- MenuButton — opens a menu without selection state
- ContextMenu — reusable popup menu component
- Radiobutton — explicit single-selection groups
- SelectBox — list-based selection control

