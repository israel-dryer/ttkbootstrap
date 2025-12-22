---
title: MenuButton
---

# MenuButton

`MenuButton` is a styled wrapper around `ttk.Menubutton` that integrates ttkbootstrap’s theming, icon system, and localization features. It represents the **primitive menu-triggering button** upon which higher-level widgets like `DropdownButton` are built.

## Quick start

Use `MenuButton` when you already have (or want to manage) a native `tk.Menu` instance directly.

```python
import ttkbootstrap as ttk
from tkinter import Menu

app = ttk.App()

menu = Menu(app, tearoff=False)
menu.add_command(label="Open", command=lambda: print("Open"))
menu.add_command(label="Save", command=lambda: print("Save"))
menu.add_separator()
menu.add_command(label="Exit", command=app.destroy)

btn = ttk.MenuButton(app, text="File", menu=menu, bootstyle="secondary")
btn.pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use a MenuButton when you need a **traditional, native menu trigger** backed by `tk.Menu` (or when you’re integrating with existing Tk menu code).

### Consider a different control when…

- You want a modern, widget-backed menu with icons/toggles and unified events → use **DropdownButton**
- You need a context (right-click) menu → use **ContextMenu**
- You need a value-selection dropdown → use **OptionMenu** or **SelectBox**

---

## Appearance

MenuButton supports ttkbootstrap’s semantic colors and variants via `bootstyle`, plus the integrated icon system.

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

!!! note "Icons"
    See **Guides → Design System → Icons** for icon sizing, coloring, and state behavior.

---

## Examples & patterns

### Key concepts: MenuButton vs DropdownButton

**MenuButton**
- Uses a native `tk.Menu`
- Lower-level primitive
- Best for menubar-style UI or existing Tk menu code

**DropdownButton**
- Uses a widget-backed `ContextMenu`
- Higher-level control
- Supports icons, checks, radios, and unified item events

In most application UI, prefer **DropdownButton** unless you specifically need a native `tk.Menu`.

### Localization and reactive text

`MenuButton` supports both `textvariable` and `textsignal`:

```python
btn = ttk.MenuButton(app, textsignal=my_signal, localize="auto")
```

---

## Behavior

- Activates via mouse click
- Participates in focus traversal when `takefocus=True`
- Menu navigation is handled by the attached `tk.Menu`

When clicked, MenuButton explicitly receives focus so that focus styling is visible:

```text
<Button-1> → focus_set()
```

!!! note "Native menu behavior"
    Keyboard navigation and accessibility depend on the underlying `tk.Menu` implementation and platform conventions.

---

## Localization & reactivity

Localization behavior is controlled by global application settings and the widget `localize` option. See **Guides → Internationalization → Localization** for the full model.

---

## Related widgets

- **DropdownButton** — higher-level, widget-backed alternative
- **ContextMenu** — widget-backed pop-up menu
- **OptionMenu** — value-selection dropdown

---

## Reference

- **API Reference:** `ttkbootstrap.MenuButton`
- **Related guides:** Design System → Variants, Design System → Icons, Internationalization → Localization
