---
title: ContextMenu
icon: fontawesome/solid/caret-right
---


# ContextMenu

`ContextMenu` renders a lightweight popup menu that appears near a target widget or at explicit screen coordinates. It ships with commands, checkbuttons, radiobuttons, separators, click-outside dismissal, and full position control while staying styled with your theme.

---

## Overview

- Add menu entries via `add_command`, `add_checkbutton`, `add_radiobutton`, `add_separator` or `add_item`/`add_items` helpers. Each entry is a themed primitive (`Button`, `CheckButton`, `RadioButton`, `Separator`).
- Configure positioning through `anchor` (point on the menu), `attach` (point on the target), `offset`, and direct `position=(x,y)` calls. Legacy negative coordinates work as offsets from screen edges.
- Control size with `minwidth`, `width`, `minheight`, and `height`, and keep the menu on-theme using `bootstyle` tokens on the surrounding `Frame`.
- Events such as `on_item_click(callback)` surface structured payloads (`type`, `text`, `value`), and you can use `hide_on_outside_click` to close automatically when the user clicks elsewhere.

Use `ContextMenu` for right-click menus, toolbar dropdowns, or any temporary command list that should feel native to Tk while matching Bootstrap colors.

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.contextmenu import ContextMenu

app = ttk.App(theme="cosmo")

btn = ttk.Button(app, text="Right click me")
btn.pack(padx=20, pady=20)

menu = ContextMenu(
    master=app,
    target=btn,
    offset=(0, 2),
    items=[
        {"type": "command", "text": "Edit", "icon": "pencil"},
        {"type": "command", "text": "Delete", "icon": "trash"},
        {"type": "separator"},
        {"type": "checkbutton", "text": "Show Grid", "value": True}
    ]
)

btn.bind("<Button-3>", lambda e: menu.show(position=(e.x_root, e.y_root)))
menu.on_item_click(lambda data: print("Clicked", data))

app.mainloop()
```

---

## Items & customization

- Build your initial list via `items` or mutate it later with `add_items`, `insert_item`, `remove_item`, `move_item`, and `configure_item`.
- Pass dictionaries (`{"type":"command","text":"Open","icon":"folder2"}`) or `ContextMenuItem` objects to `add_items()`.
- Use `popdown_options` (when wrapping in DropdownButton) or explicit `anchor`/`attach`/`offset` arguments to fine-tune the geometric relationship with the target. Negative coordinates mirror offsets from the right/bottom edges.
- The menu hides itself after each click or when clicking outside (controlled by `hide_on_outside_click`) and can be shown manually via `show(position=(x,y))` or `show()` relative to the target.

---

## When to use ContextMenu

Choose `ContextMenu` when you want a popup command palette tied to a widget or pointer events. It pairs nicely with `DropdownButton`, `MenuButton`, or right-click handlers. For more persistent menus, consider `MenuButton` or `DropdownButton`; for floating dialogs use `Toast` or `ToolTip`.
