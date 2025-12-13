---
title: DropdownButton
icon: fontawesome/solid/caret-down
---


# DropdownButton

`DropdownButton` is a `MenuButton` backed by a `ContextMenu`. It renders a button (with optional icon/text) and pops down a fully featured context menu when clicked, giving you toolbar-style actions with theme-aware styling.

---

## Overview

Highlights:

- Declaratively build the menu using `items` on initialization or call `add_command`, `add_radiobutton`, `add_checkbutton`, `add_separator`, etc., afterward.
- Supports `command`, `image`, `icon`, `icon_only`, `compound`, `padding`, `width`, `underline`, `state`, `takefocus`, and signal/text bindings exactly like `MenuButton`.
- `popdown_options` lets you configure `ContextMenu` positioning (`anchor`, `attach`, `offset`), and `show_dropdown_button` / `dropdown_button_icon` control the chevron.
- Each menu item selection fires `on_item_click(callback)` with the menu data, and `context_menu` exposes the raw `ContextMenu` instance for advanced customization.

Use DropdownButton when you need a compact control that either triggers a single action or opens a menu of related commands (toolbars, action hubs, etc.).

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.contextmenu import ContextMenuItem

app = ttk.App(theme="cosmo")

menu_items = [
    {"text": "New", "icon": "plus"},
    {"text": "Open", "icon": "folder"},
    {"text": "Save", "icon": "save"},
]

dd = ttk.DropdownButton(
    app,
    text="Actions",
    items=[ContextMenuItem(**item) for item in menu_items],
    bootstyle="primary-outline"
)
dd.pack(padx=16, pady=16)

dd.on_item_click(lambda data: print("Selected", data["text"]))

app.mainloop()
```

---

## Items, popdown, & events

- Supply a list of `ContextMenuItem` entries for initial options or mutate them at runtime via `add_items`, `insert_item`, `remove_item`, and other helpers.
- `popdown_options` customize how the dropdown attaches (`anchor`, `attach`, `offset`) or which popdown type is used.
- `show_dropdown_button`/`dropdown_button_icon` let you hide the chevron or replace its glyph.
- Bind `on_item_click` to react when any item is picked; the callback receives the selected item dict, and you can call `off_item_click` to remove the listener.

---

## Styling tips

- Start with `bootstyle` tokens like `primary`, `secondary`, or `ghost` to express intent.
- Use `icon_only=True` with `icon` for toolbar buttons, and set `compound` when you need icon+text combos.
- Pass `popdown_options={'offset': (0, 4)}` to nudge the menu away from the button or change `attach`/`anchor` for toolbar alignments.

---

## When to use DropdownButton

- **Button**
- **MenuButton**

