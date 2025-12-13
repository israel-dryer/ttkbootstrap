---
title: Button
icon: fontawesome/solid/square
---

# Button

Buttons trigger an action. In ttkbootstrap v2, `Button` is a wrapper around `ttk.Button` that adds **Bootstyle tokens**,
**theme-aware icons**, and optional **signals and localization** on top of standard ttk behavior.

---

## Overview

Buttons are one of the most common interactive elements in a desktop application.
ttkbootstrap buttons are designed to:

- follow the active theme automatically,
- express intent through semantic variants (`primary`, `danger`, etc.),
- support icon-only and icon+text usage,
- behave consistently across hover, focus, pressed, and disabled states.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-button-overview.png -->
<!-- A small gallery showing several buttons side-by-side:
     primary, primary-outline, primary-ghost, primary-link, icon+text -->

---

## Quick Example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="solar")

ttk.Button(
    app.window,
    text="Save",
    bootstyle="success",
    command=lambda: print("Saved"),
).pack(padx=16, pady=16)

app.mainloop()
```

---

## Bootstyle Variants

Buttons use **Bootstyle tokens** to describe both intent and treatment.

### Common variants

- **Solid (default)**
  `primary`, `success`, `danger`, `warning`

- **Outline**
  `primary-outline`, `danger-outline`

- **Ghost**
  `primary-ghost`
  Subtle background, often used in toolbars or secondary actions.

- **Text**
  `primary-text`, `foreground-text`
  No background or border.

- **Link**
  `primary-link`
  Styled like a hyperlink, including cursor and underline behavior.

```python
import ttkbootstrap as ttk

ttk.Button(parent, text="Delete", bootstyle="danger-outline")
```

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-button-variants.png -->
<!-- Same label rendered in solid / outline / ghost / text / link -->

---

## Icons

Buttons support both raw Tk images and **theme-aware icons**.

### Icon + Text

```python
import ttkbootstrap as ttk

ttk.Button(
    parent,
    text="Settings",
    icon="gear",
    bootstyle="secondary",
)
```

When an icon is present, the button automatically lays out the icon and label together.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-button-icon-text.png -->
<!-- Side-by-side: text-only button vs icon+text button -->

---

## Icon-Only Buttons

For toolbar-style actions, you can create icon-only buttons:

```python
import ttkbootstrap as ttk

ttk.Button(
    parent,
    icon="trash",
    icon_only=True,
    bootstyle="secondary",
    command=delete_item,
)
```

Icon-only buttons:

- remove extra text padding,
- use a slightly larger default icon size,
- are ideal for compact toolbars.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-button-icon-only.png -->
<!-- A toolbar row with 3–4 icon-only buttons -->

---

## States and Interaction

Buttons follow the standard ttk state model:

- normal
- hover
- pressed
- focused
- disabled

Each state is styled by the active theme to provide clear visual feedback for both mouse and keyboard users.

<!-- IMAGE PLACEHOLDER -->
<!-- widgets-button-states.png -->
<!-- Grid showing normal / hover / pressed / focused / disabled -->

---

## Localization & Signals

Buttons integrate with ttkbootstrap’s localization and reactive systems.

- `localize` controls whether the label participates in localization
- `textsignal` allows the label to update reactively from a signal

```python
import ttkbootstrap as ttk

# Conceptual example
# status = Signal("Save")
# ttk.Button(parent, textsignal=status, bootstyle="success")
```

This is useful for dynamic labels such as “Save”, “Saving…”, or localized text.

---

## Common Options

In addition to all standard `ttk.Button` options, the most commonly used ttkbootstrap options are:

- `bootstyle` – semantic style token (preferred over raw `style=`)
- `icon` – theme-aware icon
- `icon_only` – icon-only button mode
- `compound` – icon/text placement
- `padding`, `width`
- `state`
- `surface_color` – override surface token for this button only

---

## Related Widgets

- **DropdownButton** — button that opens a menu surface
- **MenuButton / OptionMenu** — menu-based selection
- **ContextMenu** — right-click actions
- **Dialogs** — buttons commonly drive dialog actions
- **Toast** — buttons often trigger feedback messages
