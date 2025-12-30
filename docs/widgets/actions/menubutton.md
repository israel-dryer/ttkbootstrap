---
title: MenuButton
---

# MenuButton

`MenuButton` is a **menu-first** control: it displays like a button, but its primary purpose is to **open a Tk menu**.
Use it for classic menu patterns (File/Edit/View), or when the options list is the main interaction.

---

## Quick start

`MenuButton` uses a standard Tk `Menu`.

```python
import ttkbootstrap as ttk
from tkinter import Menu

app = ttk.App()

m = Menu(app, tearoff=0)
m.add_command(label="Open", command=lambda: print("Open"))
m.add_command(label="Save", command=lambda: print("Save"))
m.add_separator()
m.add_command(label="Exit", command=app.destroy)

ttk.MenuButton(app, text="File", menu=m).pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `MenuButton` when:

- the control is primarily a **menu entry point**
- you need native-style menu behavior (keyboard navigation, platform conventions)
- your menu items map well to Tk’s `Menu` model

### Consider a different control when…

- you want a primary action plus a small menu → use [DropdownButton](dropdownbutton.md)
- you want a fully themed, widget-backed menu with icons/layout → use [ContextMenu](contextmenu.md)
- you want a single action → use [Button](button.md)

---

## Appearance

`MenuButton` supports semantic colors and variants through `color` and `variant`.

!!! link "See [Design System → Variants](../../design-system/variants.md) for how variants map consistently across widgets."

```python
ttk.MenuButton(app, text="Menu", color="primary").pack(pady=4)
ttk.MenuButton(app, text="Menu", color="primary", variant="outline").pack(pady=4)
```

---

## Behavior

- `MenuButton` opens the associated Tk `Menu`.
- Menu keyboard navigation and platform conventions are handled by Tk.

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Localization

Tk `Menu` labels can be localized by passing message tokens (or resolved strings) when you build the menu.

```python
m = Menu(app, tearoff=0)
m.add_command(label="menu.open", command=lambda: ...)
ttk.MenuButton(app, text="button.file", menu=m).pack()
```

!!! link "See [Localization](../../capabilities/localization.md) for how message tokens are resolved and how language switching works."

---

## Additional resources

### Related widgets

- [DropdownButton](dropdownbutton.md)
- [ContextMenu](contextmenu.md)
- [Button](button.md)

### Framework concepts

- [Design System → Variants](../../design-system/variants.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)
- [Localization](../../capabilities/localization.md)

### API reference

- [`ttkbootstrap.MenuButton`](../../reference/widgets/MenuButton.md)
