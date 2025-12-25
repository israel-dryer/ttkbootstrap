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

title: DropdownButton
---

# DropdownButton

`DropdownButton` is a compact, button-first control that opens a contextual menu when activated. It’s ideal for toolbars, “More actions” buttons, and small groups of related actions where you want discoverable options without permanently occupying space.

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

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

---

## When to use

Use a DropdownButton when you need to **group a small set of related actions** behind a single control.

### Consider a different control when…

- You want a traditional native menu trigger → use **MenuButton**

- You need a context (right-click) menu → use **ContextMenu**

- You need a persistent value selection → use **OptionMenu** or **SelectBox**

- The action list is long or needs search → use a dialog or dedicated view

---

## Appearance

DropdownButton supports the same `bootstyle` color + variant system as Button. Use variants to match the level of emphasis in your UI (e.g., `primary`, `secondary`, `outline`, `ghost`).

!!! note "Variants"
    See **Guides → Design System → Variants** for the full variant model and recommended usage.

### Dropdown indicator

You can hide the dropdown affordance or customize its icon:

```python
btn = ttk.DropdownButton(app, text="Actions", show_dropdown_button=False)
```

```python
btn.configure(dropdown_button_icon="chevron-down")
```

---

## Examples & patterns

### Key concepts: activation vs selection

There are two interaction layers:

- **Button activation** — the button behaves like a normal button.

- **Menu item selection** — items inside the dropdown emit their own actions.

You can attach logic to each item, or route selections through a single callback.

### Providing initial items

```python
btn = ttk.DropdownButton(app, text="Actions", items=[
    ttk.ContextMenuItem("command", text="New", command=lambda: print("New")),
    ttk.ContextMenuItem("separator"),
    ttk.ContextMenuItem("command", text="Exit", command=app.destroy),
])
```

### Adding and managing items dynamically

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

### Centralized selection handling (`on_item_click`)

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

---

## Behavior

The dropdown opens when:

- the user clicks the button

- the user presses **Enter**

The menu will not open if the widget is disabled or readonly.

!!! note "Readonly state"
    A readonly DropdownButton remains visible but does not open its menu. This is useful for temporarily disabling actions without changing layout.

---

## Localization & reactivity

Menu items can be localized the same way as other widgets if you provide localized labels/keys. For the full model, see **Guides → Internationalization → Localization**.

---

## Related widgets

- **ContextMenu** — the menu used internally (also useful for right-click menus)

- **MenuButton** — native `tk.Menu` based trigger

- **OptionMenu** — value-selection dropdown

- **SelectBox** — advanced selection control

---

## Reference

- **API Reference:** `ttkbootstrap.DropdownButton`

- **Related guides:** Design System → Variants, Design System → Icons, Internationalization → Localization

---

## Additional resources

### Related widgets

- [Button](button.md)

- [ButtonGroup](buttongroup.md)

- [ContextMenu](contextmenu.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.DropdownButton`](../../reference/widgets/DropdownButton.md)
