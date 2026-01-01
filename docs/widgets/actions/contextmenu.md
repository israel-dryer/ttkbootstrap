---
title: ContextMenu
---

# ContextMenu

`ContextMenu` is a widget-backed pop-up menu for right-click and contextual actions.

Unlike Tk’s native `Menu`, it is composed of ttkbootstrap widgets. This makes it fully
themeable (light/dark), enables icons, and allows richer layout and interaction patterns.

---

## Quick start

Create a menu, add items, and show it in response to a right-click.

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.ContextMenu(app)
menu.add_command(text="Open", icon="folder-open", command=lambda: print("Open"))
menu.add_command(text="Rename", command=lambda: print("Rename"))
menu.add_separator()
menu.add_command(text="Delete", icon="trash", command=lambda: print("Delete"))

def on_right_click(event):
    menu.show((event.x_root, event.y_root))

app.bind("<Button-3>", on_right_click)
app.mainloop()
```

---

## When to use

Use `ContextMenu` when:

- actions are contextual to a widget, list row, or region
- you want theme-consistent menus across platforms
- you want icons or richer item styling

### Consider a different control when…

- you want a native OS menu → use Tk’s `Menu` via [MenuButton](menubutton.md)
- you want a button-first action with a small menu → use [DropdownButton](dropdownbutton.md)

---

## Menu items

### Command items

Use command items for standard actions.

```python
menu.add_command(text="Open", command=on_open)
```

### Check items

Use check items for independent on/off options.

```python
menu.add_checkbutton(text="Show hidden files", value=True)
menu.add_checkbutton(text="Pin to sidebar", value=False)
```

### Radio items

Use radio items for selecting one option from a set.

```python
sort_var = ttk.StringVar(value="name")
menu.add_radiobutton(text="Sort by name", value="name", variable=sort_var)
menu.add_radiobutton(text="Sort by date", value="date", variable=sort_var)
```

---

## Behavior

- `show(position)` displays the menu at a screen coordinate `(x, y)`.
- `hide()` programmatically closes the menu.
- The menu hides automatically when the user clicks outside.
- Item commands fire on click and close the menu.

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

!!! link "See [Virtual Events](../../capabilities/virtual-events.md) for interaction events emitted by ttkbootstrap widgets."

---

## Icons

Menu items use the same icon system as other ttkbootstrap widgets.

```python
menu.add_command(text="Settings", icon="gear", command=on_settings)
```

!!! link "See [Icons & Imagery](../../capabilities/icons.md) for icon sizing, DPI handling, and recoloring behavior."

---

## Localization

If localization is enabled, menu item labels can be message tokens.

```python
menu.add_command(text="menu.open", command=on_open)
menu.add_command(text="menu.delete", command=on_delete)
```

!!! link "See [Localization](../../capabilities/localization.md) for how message tokens are resolved and language switching works."

---

## Positioning patterns

### Attach to a target widget

```python
menu = ttk.ContextMenu(
    app,
    target=my_button,
    anchor="nw",
    attach="se",
    offset=(5, 5)
)
menu.show()
```

### Show at pointer location

```python
menu.show((event.x_root, event.y_root))
```

---

## Advanced patterns

### Dynamic menus

Build context-sensitive menus by creating a new menu or conditionally adding items.

```python
def on_right_click(event):
    menu = ttk.ContextMenu(root)
    menu.add_command(text="Open", command=on_open)
    if can_delete():
        menu.add_command(text="Delete", command=on_delete)
    menu.show((event.x_root, event.y_root))
```

### Centralized item handling

Register a single callback to route menu actions.

```python
def on_item_click(info):
    print(info["text"], info["value"])

menu.on_item_click(on_item_click)
```

!!! link "See [API Reference → ContextMenu](../../reference/widgets/ContextMenu.md) for full item management and callback APIs."

---

## Additional resources

### Related widgets

- [DropdownButton](dropdownbutton.md)
- [MenuButton](menubutton.md)
- [Button](button.md)

### Framework concepts

- [Icons & Imagery](../../capabilities/icons-and-imagery.md)
- [Virtual Events](../../capabilities/virtual-events.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)
- [Localization](../../capabilities/localization.md)

### API reference

- [`ttkbootstrap.ContextMenu`](../../reference/widgets/ContextMenu.md)
- [`ttkbootstrap.ContextMenuItem`](../../reference/widgets/ContextMenuItem.md)
