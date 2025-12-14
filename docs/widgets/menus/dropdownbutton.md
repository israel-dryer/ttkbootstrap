---
title: DropdownButton
icon: fontawesome/solid/caret-down
---

# DropdownButton

`DropdownButton` is a compact, button-first control that opens a contextual menu when activated. It’s ideal for toolbars, “More actions” buttons, and small groups of related actions where you want discoverable options without permanently occupying space.

<!--
IMAGE: DropdownButton with open menu
Suggested: Primary DropdownButton showing a ContextMenu with commands, a separator, and a checkbutton
Theme variants: light / dark
-->

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.Window()

items = [
    ttk.ContextMenuItem("command", text="Open", icon="folder2-open", command=lambda: print("Open")),
    ttk.ContextMenuItem("command", text="Save", icon="floppy", command=lambda: print("Save")),
    ttk.ContextMenuItem("separator"),
    ttk.ContextMenuItem("checkbutton", text="Show grid", value=True),
]

btn = ttk.DropdownButton(app, text="Actions", items=items, bootstyle="primary")
btn.pack(padx=20, pady=20)

app.mainloop()
```

<!--
IMAGE: Basic DropdownButton example
Suggested: “Actions” button with dropdown menu visible
-->

---

## What problem it solves

Desktop UIs frequently need to group related actions without cluttering the interface. `DropdownButton` provides:

- A familiar button interaction model
- A flexible popdown menu with commands, checkbuttons, radiobuttons, and separators
- A consistent event and styling model across platforms

---

## Core concepts

### Button activation vs item selection

There are two distinct interaction layers:

- **Button activation** — the button itself behaves like a normal button.
- **Menu item selection** — items inside the dropdown emit their own actions.

You can either attach logic directly to each item, or centralize handling with a single callback.

---

### The dropdown menu

Internally, `DropdownButton` uses a widget-backed context menu rather than a native Tk `Menu`. This allows:

- Rich styling
- Icons per item
- Checkbutton and radiobutton support
- Consistent cross-platform behavior

By default, the menu opens below the button and aligns naturally with its left edge. Positioning can be customized if needed.

<!--
IMAGE GROUP: Dropdown positioning
- Default dropdown (below-left)
- Alternate alignment example (below-right)
-->

---

## Common options & patterns

### Providing initial items

```python
btn = ttk.DropdownButton(app, text="Actions", items=[
    ttk.ContextMenuItem("command", text="New", command=lambda: print("New")),
    ttk.ContextMenuItem("separator"),
    ttk.ContextMenuItem("command", text="Exit", command=app.destroy),
])
```

---

### Adding and managing items dynamically

`DropdownButton` exposes the menu item API directly:

```python
btn = ttk.DropdownButton(app, text="More")

btn.add_command(text="Open", icon="folder2-open", command=lambda: print("Open"))
btn.add_checkbutton(text="Show grid", value=True)
btn.add_separator()
btn.add_command(text="Exit", icon="x-lg", command=app.destroy)
```

Also available:

- `add_radiobutton(...)`
- `add_item(...)`, `add_items(...)`
- `insert_item(...)`, `remove_item(...)`, `move_item(...)`
- `configure_item(...)`
- `items(...)` (get or replace all items)

---

### Handling selections with `on_item_click`

Instead of per-item callbacks, you can route all selections through one handler:

```python
def on_menu_item(data: dict):
    # Example payload:
    # {"type": "command", "text": "Open", "value": None}
    print(data)

btn.on_item_click(on_menu_item)
```

To remove the handler:

```python
btn.off_item_click()
```

!!! tip "Centralize menu logic"
    Use `on_item_click(...)` for dynamic menus or when you want a single action router.

<!--
IMAGE: Item click callback flow
Suggested: Diagram showing one handler receiving different item payloads
-->

---

### Controlling the dropdown indicator

You can hide the dropdown affordance or customize its icon:

```python
btn = ttk.DropdownButton(app, text="Actions", show_dropdown_button=False)
```

```python
btn.configure(dropdown_button_icon="chevron-down")
```

---

## Events and keyboard behavior

The dropdown opens when:

- the user clicks the button
- the user presses **Enter**

The menu will not open if the widget is disabled or readonly.

!!! note "Readonly state"
    A readonly DropdownButton remains visible but does not open its menu. This is useful for temporarily disabling actions without changing layout.

---

## UX guidance

- Use DropdownButton for small, related action groups (3–8 items).
- Group related items with separators.
- Use checkbuttons or radiobuttons for stateful options.

!!! tip "Avoid menu overload"
    If a menu grows large or requires search, consider a dialog or dedicated view instead.

---

## When to use / when not to

**Use DropdownButton when:**

- You want a compact action launcher
- Actions are secondary to the main workflow
- You need toggleable or grouped actions

**Avoid DropdownButton when:**

- You need a persistent selection control (use `OptionMenu` or `SelectBox`)
- The action list is long or dynamic
- You need native menubar integration

---

## Related widgets

- **ContextMenu** — the menu used internally (also useful for right-click menus)
- **MenuButton** — the lower-level base widget
- **OptionMenu** — value-selection dropdown
- **SelectBox** — advanced selection control
