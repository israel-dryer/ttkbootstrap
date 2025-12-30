---
title: ButtonGroup
---

# ButtonGroup

`ButtonGroup` groups related actions into a connected row or column of buttons.
It is most common in toolbars, segmented controls, and compact "action clusters" where buttons should read as a unit.

---

## Quick start

Create a group and add buttons. The group handles spacing, connection visuals, and consistent styling.

```python
import ttkbootstrap as ttk

app = ttk.App()

bg = ttk.ButtonGroup(app, color="primary")
bg.pack(padx=20, pady=20)

bg.add(text="Cut", icon="scissors", command=lambda: print("Cut"))
bg.add(text="Copy", icon="copy", command=lambda: print("Copy"))
bg.add(text="Paste", icon="clipboard", command=lambda: print("Paste"))

app.mainloop()
```

---

## When to use

Use `ButtonGroup` when:

- you have multiple actions that are conceptually related
- you want a compact toolbar cluster without separate spacing between buttons
- you want "segmented" visuals without managing per-button layout

### Consider a different control when…

- you need a single/multi selection model → use [ToggleGroup](../selection/togglegroup.md)
- you need unrelated actions that should not look connected → use separate [Button](button.md) widgets

---

## Appearance

The group style is driven by `color` and `variant`. This sets the default for contained buttons.

!!! link "See [Design System → Variants](../../design-system/variants.md) for how variants map consistently across widgets."

```python
ttk.ButtonGroup(app, color="primary").pack(pady=4)
ttk.ButtonGroup(app, color="primary", variant="outline").pack(pady=4)
ttk.ButtonGroup(app, color="primary", variant="ghost").pack(pady=4)
```

---

## Examples & patterns

### Icon-only toolbar group

```python
bg = ttk.ButtonGroup(app, color="secondary", variant="ghost")
bg.pack(pady=10)

bg.add(icon="undo", icon_only=True, command=lambda: print("Undo"))
bg.add(icon="redo", icon_only=True, command=lambda: print("Redo"))
bg.add(icon="trash", icon_only=True, command=lambda: print("Delete"))
```

!!! link "See [Icons & Imagery](../../capabilities/icons-and-imagery.md) for icon sizing, DPI handling, and recoloring behavior."

### Disabling a group

You can disable individual buttons, or set the group `state` so all children inherit it.

```python
bg = ttk.ButtonGroup(app, color="primary", state="disabled")
bg.pack(pady=10)

bg.add(text="Disabled", command=lambda: ...)
```

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Additional resources

### Related widgets

- [Button](button.md)
- [ToggleGroup](../selection/togglegroup.md)
- [RadioGroup](../selection/radiogroup.md)

### Framework concepts

- [Design System → Variants](../../design-system/variants.md)
- [Design System → Icons](../../design-system/icons.md)
- [Icons & Imagery](../../capabilities/icons-and-imagery.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)

### API reference

- [`ttkbootstrap.ButtonGroup`](../../reference/widgets/ButtonGroup.md)