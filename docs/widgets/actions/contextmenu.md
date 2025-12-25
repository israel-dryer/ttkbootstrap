---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: ContextMenu
---

# ContextMenu

`ContextMenu` is a lightweight, widget-backed pop-up menu used to present contextual actions. It supports commands, checkbuttons, radiobuttons, icons, separators, and keyboard navigation, while remaining fully styleable and consistent across platforms.

## Quick start

A `ContextMenu` is typically shown in response to a right-click, but it can also be displayed programmatically.

```python
import ttkbootstrap as ttk

app = ttk.App()

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

---

## When to use

Use a ContextMenu when actions are **contextual**, secondary, or dependent on the current selection.

### Consider a different control when…

- Actions are primary or frequently used → use **Button** or **Toolbar**

- You need a compact action launcher → use **DropdownButton**

- You need native menubar integration → use **MenuButton**

- Actions require multi-step input → use a dialog

---

## Appearance

ContextMenu items are fully styleable and integrate with ttkbootstrap’s theme system.

- Supports icons per item

- Supports checkbuttons and radiobuttons

- Uses the active theme’s colors, spacing, and typography

!!! note "Styling"
    ContextMenu styling follows the same design tokens as other widgets. See **Guides → Design System** for details.

---

## Examples & patterns

### Key concepts: widget-backed menus

Unlike Tk’s native `Menu`, `ContextMenu` is composed of real ttkbootstrap widgets. This enables:

- Full theming and dark/light mode consistency

- Icons and custom layouts per item

- Predictable cross-platform behavior

### Adding items

```python
menu.add_command(text="Open", command=lambda: print("Open"))
menu.add_checkbutton(text="Show grid", value=True)
menu.add_radiobutton(text="Mode A", value="a", variable=mode_var)
menu.add_separator()
```

### Defining items up front

```python
items = [
    ttk.ContextMenuItem("command", text="Copy"),
    ttk.ContextMenuItem("command", text="Paste"),
    ttk.ContextMenuItem("separator"),
    ttk.ContextMenuItem("command", text="Delete"),
]

menu = ttk.ContextMenu(app, items=items)
```

### Managing items dynamically

`ContextMenu` exposes a full item-management API:

- `add_item(...)`, `add_items(...)`

- `insert_item(...)`, `remove_item(...)`, `move_item(...)`

- `configure_item(...)`

- `items(...)` (get or replace all items)

This is especially useful when menu contents depend on selection state.

### Centralized selection handling

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

---

## Behavior

When shown, ContextMenu:

- Grabs focus automatically

- Supports arrow-key navigation

- Activates items with **Enter**

- Closes on **Escape** or outside click

Keyboard and focus behavior are handled internally while the menu is visible.

---

## Localization & reactivity

Menu item labels can participate in localization the same way as other widgets. For the full localization model, see **Guides → Internationalization → Localization**.

---

## Related widgets

- **DropdownButton** — button-triggered menus using ContextMenu internally

- **MenuButton** — native `tk.Menu` based trigger

- **Dialog / MessageDialog** — for confirmations and complex actions

---

## Reference

- **API Reference:** `ttkbootstrap.ContextMenu`

- **Related guides:** Design System → Icons, Internationalization → Localization

---

## Additional resources

### Related widgets

- [Button](button.md)

- [ButtonGroup](buttongroup.md)

- [DropdownButton](dropdownbutton.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.ContextMenu`](../../reference/widgets/ContextMenu.md)
