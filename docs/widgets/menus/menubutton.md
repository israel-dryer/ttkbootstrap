---
title: MenuButton
icon: fontawesome/solid/chevron-down
---

# MenuButton

A MenuButton displays a button that opens an associated menu. In ttkbootstrap v2, `MenuButton` extends `ttk.Menubutton`
with bootstyle variants, theme-aware icons, dropdown indicators, and automatic focus handling.

---

## Overview

MenuButtons are commonly used when:

- an action has multiple related choices,
- a compact control is preferred over a full menu bar,
- a button should expose secondary actions.

ttkbootstrap MenuButtons are designed to:

- look and behave like standard buttons,
- clearly indicate the presence of a dropdown menu,
- integrate icons consistently with other controls,
- respond correctly to hover, focus, and disabled states.

---

## Quick Example

```python
import ttkbootstrap as ttk

app = ttk.Window()

menu = ttk.Menu(app, tearoff=0)
menu.add_command(label="Open")
menu.add_command(label="Save")
menu.add_separator()
menu.add_command(label="Exit", command=app.destroy)

ttk.MenuButton(
    app,
    text="File",
    menu=menu,
    bootstyle="primary",
).pack(padx=16, pady=16)

app.mainloop()
```

---

## Visual Structure

A MenuButton consists of:

- a button surface (styled like `Button`)
- optional icon content
- a dropdown chevron indicator
- optional spacer to separate content and indicator

The dropdown indicator is part of the style system and is recolored automatically to match widget state.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-menubutton-structure.png -->
<!-- Button showing label + chevron indicator -->

---

## Bootstyle Variants

MenuButtons support the same semantic variants as regular buttons:

- solid (default)
- outline
- ghost
- text

```python
ttk.MenuButton(text="Options", bootstyle="secondary-outline")
```

Each variant defines:

- surface treatment
- focus ring behavior
- hover and pressed feedback
- chevron color mapping

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-menubutton-variants.png -->
<!-- Same MenuButton rendered in solid / outline / ghost / text -->

---

## Icons

MenuButtons support theme-aware icons via the `icon` option.

```python
ttk.MenuButton(
    text="Settings",
    icon="gear",
    bootstyle="secondary",
)
```

Icons are:

- normalized to a consistent size,
- recolored per widget state,
- aligned with text automatically.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-menubutton-icon.png -->
<!-- MenuButton with icon + label + chevron -->

---

## Icon-Only MenuButtons

For toolbar usage, MenuButtons may be icon-only.

```python
ttk.MenuButton(
    icon="three-dots",
    icon_only=True,
    bootstyle="ghost",
)
```

Icon-only MenuButtons:

- remove extra label padding,
- center the icon,
- remain keyboard-accessible.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-menubutton-icon-only.png -->
<!-- Toolbar row with icon-only MenuButtons -->

---

## Dropdown Indicator Control

The dropdown chevron is configurable through style options:

- show_dropdown_button (default: True)
- dropdown_button_icon (default: caret-down)

These options are forwarded to the style builder.

```python
ttk.MenuButton(
    text="More",
    bootstyle="text",
    style_options={
        "show_dropdown_button": False
    }
)
```

---

## Focus and Interaction

MenuButtons request focus on click to ensure:

- focus rings appear correctly,
- keyboard navigation remains predictable,
- visual state matches interaction state.

This behavior is handled automatically by the widget wrapper.

---

## Menus and Theme Awareness

MenuButton works naturally with:

- standard tk.Menu
- ttkbootstrap menu utilities

For declarative, icon-aware menus that respond to theme changes, see:

- MenuManager
- create_menu

```python
from ttkbootstrap.menu import create_menu
```

---

## Common Options

In addition to standard ttk.Menubutton options, commonly used ttkbootstrap options include:

- bootstyle
- icon
- icon_only
- menu
- direction
- padding
- surface_color
- style_options
- localize

---

## Related Widgets

- Button — basic action button
- DropdownButton — button-like menu pattern
- ContextMenu — right-click menus
- Toolbutton — toolbar-optimized selectable buttons
