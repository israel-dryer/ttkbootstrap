---
title: ContextMenu
icon: fontawesome/solid/ellipsis-vertical
---

# ContextMenu

`ContextMenu` is a lightweight, widget-backed pop-up menu used to present contextual actions. It supports commands, checkbuttons, radiobuttons, icons, separators, and keyboard navigation, while remaining fully styleable and consistent across platforms.

<!--
IMAGE: Context menu on right-click
Suggested: Right-click on a table row showing a ContextMenu with mixed items
Theme variants: light / dark
-->

---

## Basic usage

A `ContextMenu` is typically shown in response to a right-click, but it can be displayed programmatically anywhere.

```python
import ttkbootstrap as ttk

app = ttk.Window()

menu = ttk.ContextMenu(app)
menu.add_command(text="Open", icon="folder2-open", command=lambda: print("Open"))
menu.add_command(text="Rename", icon="pencil")
menu.add_separator()
menu.add_command(text="Delete", icon="trash", command=app.destroy)

def show_menu(event):
    menu.show(event.x_root, event.y_root)

app.bind("<Button-3>", show_menu)

app.mainloop()
```

<!--
IMAGE: Basic ContextMenu example
Suggested: Simple right-click menu with icons and separators
-->

---

## What problem it solves

Desktop applications often need to expose actions that are **contextual**, discoverable on demand, and not part of the primary layout. `ContextMenu` provides:

- A consistent right-click (or programmatic) menu pattern
- Rich, widget-based menu items (icons, checks, radios)
- Full theming and styling support
- Cross-platform behavior without relying on native menus

---

## Core concepts

### Widget-backed menus

Unlike Tk’s native `Menu`, `ContextMenu` is composed of real ttkbootstrap widgets. This enables:

- Full theming and dark/light mode consistency
- Icons and custom layouts per item
- More predictable behavior across platforms

---

### Showing and positioning the menu

A context menu is shown explicitly using screen coordinates:

```python
menu.show(x, y)
```

In most cases, you’ll pass `event.x_root` and `event.y_root` from a mouse event.

The menu automatically:

- Grabs focus while visible
- Closes on outside click
- Closes on Escape

<!--
IMAGE GROUP: ContextMenu positioning
- Menu opening at mouse cursor
- Menu opening near screen edge (auto-adjusted)
-->

---

## Common options & patterns

### Adding items

Items can be added incrementally:

```python
menu.add_command(text="Open", command=lambda: print("Open"))
menu.add_checkbutton(text="Show grid", value=True)
menu.add_radiobutton(text="Mode A", value="a", variable=mode_var)
menu.add_separator()
```

Or defined up front:

```python
items = [
    ttk.ContextMenuItem("command", text="Copy"),
    ttk.ContextMenuItem("command", text="Paste"),
    ttk.ContextMenuItem("separator"),
    ttk.ContextMenuItem("command", text="Delete"),
]

menu = ttk.ContextMenu(app, items=items)
```

---

### Managing items dynamically

`ContextMenu` exposes a full item-management API:

- `add_item(...)`, `add_items(...)`
- `insert_item(...)`, `remove_item(...)`, `move_item(...)`
- `configure_item(...)`
- `items(...)` (get or replace all items)

This is especially useful when the menu contents depend on selection state.

---

### Handling item selection

Each item may have its own `command`, but you can also centralize handling:

```python
def on_item_click(data: dict):
    # Example payload:
    # {"type": "command", "text": "Delete", "value": None}
    print(data)

menu.on_item_click(on_item_click)
```

To unbind:

```python
menu.off_item_click()
```

!!! tip "Single action router"
    Centralize logic with `on_item_click(...)` when menu contents are dynamic or generated at runtime.

<!--
IMAGE: ContextMenu item click payload
Suggested: Annotated diagram showing item metadata passed to handler
-->

---

## Keyboard behavior

While visible, `ContextMenu` supports:

- Arrow keys to navigate items
- Enter to activate
- Escape to close

Focus is automatically managed while the menu is open.

---

## UX guidance

- Use context menus for **secondary or power-user actions**
- Keep menus short and task-focused
- Group related actions with separators
- Avoid placing critical or destructive actions without confirmation

!!! tip "Context is key"
    Only show actions that make sense for the current selection or state.

---

## When to use / when not to

**Use ContextMenu when:**

- Actions depend on the current selection
- You want right-click behavior in tables, lists, or canvases
- Actions should not clutter the main UI

**Avoid ContextMenu when:**

- Actions are primary or frequently used (use buttons or toolbars)
- Discoverability is critical for new users
- Keyboard-only access is the primary interaction mode

---

## Related widgets

- **DropdownButton** — uses `ContextMenu` internally for button-triggered menus
- **MenuButton** — lower-level button primitive
- **Dialogs** — for confirmations and complex actions
