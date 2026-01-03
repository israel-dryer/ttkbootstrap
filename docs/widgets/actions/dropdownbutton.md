---
title: DropdownButton
---

# DropdownButton

`DropdownButton` is a **button-first** control that opens a menu of related actions.
Use it when the primary action is still a button click, but you want a secondary list of choices available on demand.

---

## Quick start

Provide menu items as `ContextMenuItem` entries. The button can also have its own `command` for the "main" action.

```python
import ttkbootstrap as ttk

app = ttk.App()

items = [
    ttk.ContextMenuItem(text="Open", command=lambda: print("Open")),
    ttk.ContextMenuItem(text="Rename", command=lambda: print("Rename")),
    ttk.ContextMenuItem(separator=True),
    ttk.ContextMenuItem(text="Delete", accent="danger", command=lambda: print("Delete")),
]

ttk.DropdownButton(
    app,
    text="File",
    items=items,
    command=lambda: print("Primary action"),
).pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `DropdownButton` when:

- you have a **primary action** plus a small set of related actions
- you want the options to be **discoverable**, but not always visible
- the control belongs in a **toolbar** or dense header area

### Consider a different control when…

- you want a *single* action → use [Button](button.md)
- the control is primarily "a menu" (not a button) → use [MenuButton](menubutton.md)
- the menu must be shown on right-click / contextual interaction → use [ContextMenu](contextmenu.md)

---

## Appearance

`DropdownButton` supports semantic colors and variants through `accent` and `variant`.

!!! link "See [Design System → Variants](../../design-system/variants.md) for how variants map consistently across widgets."

```python
ttk.DropdownButton(app, text="Primary", accent="primary", items=[]).pack(pady=4)
ttk.DropdownButton(app, text="Outline", accent="primary", variant="outline", items=[]).pack(pady=4)
ttk.DropdownButton(app, text="Ghost", accent="primary", variant="ghost", items=[]).pack(pady=4)
```

---

## Examples & patterns

### Adding icons to items

`ContextMenuItem` supports icons per entry.

```python
items = [
    ttk.ContextMenuItem(text="Settings", icon="gear", command=lambda: print("Settings")),
    ttk.ContextMenuItem(text="Help", icon="circle-help", command=lambda: print("Help")),
]
ttk.DropdownButton(app, text="More", items=items).pack(pady=10)
```

!!! link "See [Icons & Imagery](../../capabilities/icons-and-imagery.md) for icon sizing, DPI handling, and recoloring behavior."

### Handling item clicks

You can attach callbacks at item creation time, or subscribe to item-click events on the widget.

```python
btn = ttk.DropdownButton(app, text="Actions", items=items).pack(pady=10)

# Optional: listen for item clicks at the widget level
# (useful if you want centralized routing/logging).
btn.on_item_click(lambda item: print("Clicked:", item.text))
```

!!! link "See [Callbacks](../../capabilities/callbacks.md) for how ttkbootstrap command callbacks are structured."

---

## Behavior

- The dropdown opens relative to the button and closes when the user clicks away.
- Item commands fire on click, and the menu closes afterward (typical desktop behavior).

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Localization

If localization is enabled, menu labels can be message tokens just like widget `text`.

```python
items = [
    ttk.ContextMenuItem(text="menu.open", command=lambda: ...),
    ttk.ContextMenuItem(text="menu.delete", command=lambda: ...),
]
ttk.DropdownButton(app, text="button.file", items=items).pack()
```

!!! link "See [Localization](../../capabilities/localization.md) for how message tokens are resolved and how language switching works."

---

## Additional resources

### Related widgets

- [Button](button.md)
- [MenuButton](menubutton.md)
- [ContextMenu](contextmenu.md)

### Framework concepts

- [Design System → Variants](../../design-system/variants.md)
- [Design System → Icons](../../design-system/icons.md)
- [Icons & Imagery](../../capabilities/icons-and-imagery.md)
- [Callbacks](../../capabilities/callbacks.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)
- [Localization](../../capabilities/localization.md)

### API reference

- [`ttkbootstrap.DropdownButton`](../../reference/widgets/DropdownButton.md)
- [`ttkbootstrap.ContextMenuItem`](../../reference/widgets/ContextMenuItem.md)