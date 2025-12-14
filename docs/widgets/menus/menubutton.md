---
title: MenuButton
icon: fontawesome/solid/square-caret-down
---

# MenuButton

`MenuButton` is a styled wrapper around `ttk.Menubutton` that integrates ttkbootstrap’s theming, icon system, and localization features. It represents the **primitive menu-triggering button** upon which higher-level widgets like `DropdownButton` are built.

<!--
IMAGE: MenuButton with attached menu
Suggested: Simple MenuButton with text and icon, menu open below
Theme variants: light / dark
-->

---

## Basic usage

`MenuButton` is used when you already have (or want to manage) a `tk.Menu` instance directly.

```python
import ttkbootstrap as ttk
from tkinter import Menu

app = ttk.Window()

menu = Menu(app, tearoff=False)
menu.add_command(label="Open", command=lambda: print("Open"))
menu.add_command(label="Save", command=lambda: print("Save"))
menu.add_separator()
menu.add_command(label="Exit", command=app.destroy)

btn = ttk.MenuButton(app, text="File", menu=menu, bootstyle="secondary")
btn.pack(padx=20, pady=20)

app.mainloop()
```

<!--
IMAGE: Basic MenuButton example
Suggested: “File” MenuButton with native tk.Menu visible
-->

---

## What problem it solves

Tk’s native `ttk.Menubutton` provides minimal styling and no built-in support for icons, localization, or modern theme tokens. `MenuButton` solves this by:

- Integrating with ttkbootstrap’s `bootstyle` system
- Supporting theme-aware icons
- Participating in localization and reactive text updates
- Providing consistent focus and interaction styling

---

## Core concepts

### MenuButton vs DropdownButton

It’s important to distinguish these two widgets:

**MenuButton**

- Uses a native `tk.Menu`
- Lower-level primitive
- Best when integrating with existing menu code or menubars

**DropdownButton**

- Uses a widget-backed `ContextMenu`
- Higher-level control
- Supports icons, checks, radios, and unified events

In most application UI, prefer **DropdownButton** unless you specifically need a native `tk.Menu`.

---

### Icon and text behavior

`MenuButton` supports all standard ttk menubutton options plus ttkbootstrap extensions:

```python
btn = ttk.MenuButton(
    app,
    text="Options",
    icon="gear",
    compound="left",
    bootstyle="ghost",
)
```

- `icon` is resolved through the ttkbootstrap icon system
- `icon_only=True` removes extra padding reserved for text
- `compound` controls icon/text placement

<!--
IMAGE: MenuButton icon placement
Suggested: Same MenuButton with icon on left vs icon-only mode
-->

---

## Common options & patterns

### Localization and reactive text

`MenuButton` supports both `textvariable` and `textsignal`:

```python
btn = ttk.MenuButton(
    app,
    textsignal=my_signal,
    localize="auto",
)
```

This allows the button label to update automatically when locale or signal values change.

---

### Focus behavior

When clicked, `MenuButton` explicitly receives focus so that focus styling is visible:

```text
<Button-1> → focus_set()
```

This ensures consistent keyboard and accessibility feedback.

---

## Keyboard behavior

- Activates via mouse click
- Participates in focus traversal when `takefocus=True`
- Menu navigation is handled by the attached `tk.Menu`

!!! note "Native menu behavior"
    Keyboard navigation and accessibility depend on the underlying `tk.Menu` implementation and platform conventions.

---

## UX guidance

- Use `MenuButton` for **traditional menus** or when integrating with existing Tk menu code
- Prefer `DropdownButton` for modern, toolbar-style action menus
- Avoid mixing `MenuButton` and `ContextMenu` patterns in the same toolbar

---

## When to use / when not to

**Use MenuButton when:**

- You already rely on `tk.Menu`
- Building a menubar-style UI
- You need platform-native menu behavior

**Avoid MenuButton when:**

- You want rich, widget-based menus with icons and toggles
- You need unified item events
- You want consistent styling across all menu items

---

## Related widgets

- **DropdownButton** — higher-level, widget-backed alternative
- **ContextMenu** — widget-backed pop-up menu
- **OptionMenu** — value-selection dropdown
