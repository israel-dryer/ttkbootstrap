---
title: DropdownButton
---

# DropdownButton

A `DropdownButton` looks and acts like a [Button](button.md), but
clicking it opens a menu of related actions. Reach for one when a
single toolbar slot needs to expose more than one choice — "File",
"Tools", "More actions", or a kebab menu in a card header.

The menu is a [ContextMenu](contextmenu.md) under the hood, so its
items are declared with `ContextMenuItem` and support icons,
shortcuts, separators, checkbuttons, and radiobuttons just like a
context menu does.

<figure markdown>
![dropdownbutton](../../assets/dark/widgets-dropdownbutton.png#only-dark)
![dropdownbutton](../../assets/light/widgets-dropdownbutton.png#only-light)
</figure>

---

## Framework integration

**Design system**

- Accents: `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`.
- Variants: `solid` (default), `outline`, `ghost`, `link`, `text`.
- Density: `default` or `compact`. The same density propagates to the dropdown menu.
- Surface: optional `surface` token; otherwise inherits from the parent.
- The dropdown chevron can be hidden (`show_dropdown_button=False`) or
  swapped (`dropdown_button_icon="ellipsis-vertical"`).

**Signals & events**

- `command=` runs on click in addition to opening the menu — useful
  for telemetry or "open this view" affordances.
- `on_item_click(callback)` registers a single handler that fires for
  any item; the callback receives a dict
  `{"type": ..., "text": ..., "value": ...}`.
- Per-item `command=` callbacks fire too, so widget-level and
  per-item handlers can coexist.
- `textsignal=` accepts a `Signal[str]` to drive a reactive button label.

**Icons**

- `icon=` puts an icon on the button itself, theme- and state-aware.
- Each menu item can carry its own `icon=`.
- `compound` controls icon placement on the button label;
  `icon_only=True` strips label-side padding for a chevron-plus-icon
  control.

**Localization**

- The button's `text=` and each item's `text=` are treated as message
  keys when localization is enabled, and update automatically when
  the active locale changes.

---

## Basic usage

Build a list of `ContextMenuItem` entries and pass them as `items=`.

```python
import ttkbootstrap as ttk

app = ttk.App()

items = [
    ttk.ContextMenuItem("command", text="Open", command=lambda: print("Open")),
    ttk.ContextMenuItem("command", text="Rename", command=lambda: print("Rename")),
    ttk.ContextMenuItem("separator"),
    ttk.ContextMenuItem("command", text="Delete", command=lambda: print("Delete")),
]

ttk.DropdownButton(app, text="File", items=items).pack(padx=20, pady=20)

app.mainloop()
```

You can also build the menu after construction with `add_command()`,
`add_separator()`, `add_checkbutton()`, `add_radiobutton()`, or
`add_item()`. The two styles are equivalent — prefer `items=` when the
set is known up front.

---

## When to use

Use `DropdownButton` when one toolbar or header slot needs to expose a
small set of related actions and the user expects to *click* it, not
right-click it.

### Consider a different control when…

- A single action is enough → use [Button](button.md).
- The control is conceptually "a menu" with no primary action, like a
  classic menu-bar entry → use [MenuButton](menubutton.md).
- The menu should appear on right-click on top of arbitrary content →
  use [ContextMenu](contextmenu.md).
- The user picks one option from a small set that should stay visible →
  use [RadioGroup](../selection/radiogroup.md) or
  [ToggleGroup](../selection/togglegroup.md).
- The "options" need to feed a value into a form →
  use [OptionMenu](../selection/optionmenu.md) or
  [SelectBox](../selection/selectbox.md).

---

## Appearance

### Accents and variants

`accent` and `variant` follow the same conventions as
[Button](button.md) — the same accent token reads the same way across
every ttkbootstrap widget.

```python
ttk.DropdownButton(app, text="Primary", accent="primary", items=[]).pack(pady=4)
ttk.DropdownButton(app, text="Outline", accent="primary", variant="outline", items=[]).pack(pady=4)
ttk.DropdownButton(app, text="Ghost", accent="primary", variant="ghost", items=[]).pack(pady=4)
```

!!! link "See [Design System → Variants](../../design-system/variants.md) for how accents and variants compose across widgets."

### Density

`density="compact"` reduces padding on the button and propagates the
same density to the dropdown menu, so a compact toolbar opens a
compact menu.

```python
ttk.DropdownButton(app, text="More", density="compact", items=[]).pack()
```

### Chevron

A chevron sits to the right of the label by default, signaling the
dropdown affordance.

- `show_dropdown_button=False` removes it — useful for a kebab/ellipsis
  button where the icon already conveys "menu".
- `dropdown_button_icon="ellipsis-vertical"` swaps the chevron for any
  other icon name.

```python
ttk.DropdownButton(
    app,
    icon="ellipsis-vertical",
    icon_only=True,
    show_dropdown_button=False,
    items=[],
).pack()
```

---

## Examples & patterns

### Icons on items

Each `ContextMenuItem` accepts its own `icon=`. Items without an icon
still align with items that have one — the menu reserves the icon
column.

```python
items = [
    ttk.ContextMenuItem("command", text="Settings", icon="gear",
                        command=lambda: print("Settings")),
    ttk.ContextMenuItem("command", text="Help", icon="circle-help",
                        command=lambda: print("Help")),
]
ttk.DropdownButton(app, text="More", items=items).pack(pady=10)
```

!!! link "See [Icons & Imagery](../../capabilities/icons/index.md) for icon sizing, DPI handling, and recoloring behavior."

### Centralized item handling

For logging, analytics, or fan-out routing, register a single
`on_item_click` callback on the button. The callback receives a dict
describing the item that fired.

```python
btn = ttk.DropdownButton(app, text="Actions", items=items)
btn.pack(pady=10)

def route(info):
    # info == {"type": "command", "text": "Open", "value": None}
    print("Clicked:", info["text"])

btn.on_item_click(route)
```

The widget-level callback runs *in addition to* any per-item
`command=` — they don't replace each other.

### Building items at runtime

Mutating methods are forwarded from the underlying
[ContextMenu](contextmenu.md). Items can carry a stable `key=` so they
can be looked up later.

```python
btn = ttk.DropdownButton(app, text="View")
btn.pack()

btn.add_command(text="Compact", key="compact", command=lambda: print("compact"))
btn.add_command(text="Comfortable", key="comfortable", command=lambda: print("comfy"))
btn.add_separator()
btn.add_checkbutton(text="Show grid", key="grid", command=lambda: print("toggle grid"))

# rename an item by key
btn.configure_item("compact", text="Tight")

# replace the whole set
btn.items([
    ttk.ContextMenuItem("command", text="Reset", command=lambda: print("reset")),
])
```

### Shortcuts on items

`add_command()` accepts a `shortcut=` string (e.g., `"Ctrl+S"`) or a
key registered with the shortcuts service. The display string is
rendered right-aligned on the item; binding the actual accelerator on
a window is the caller's job.

```python
btn = ttk.DropdownButton(app, text="File")
btn.pack()

btn.add_command(text="Save", shortcut="Ctrl+S",
                command=lambda: print("save"))
btn.add_command(text="Save As…", shortcut="Ctrl+Shift+S",
                command=lambda: print("save as"))
```

### Positioning the menu

`popdown_options=` is forwarded to the underlying ContextMenu. Use it
to override the default `anchor` / `attach` / `offset` placement when
the menu would otherwise clip a screen edge.

```python
ttk.DropdownButton(
    app,
    text="More",
    items=items,
    popdown_options={"anchor": "ne", "attach": "se", "offset": (0, 4)},
).pack()
```

!!! link "See [ContextMenu → Attach to a widget](contextmenu.md#attach-to-a-widget-instead-of-the-cursor) for the anchor/attach/offset model."

---

## Behavior

- **Click**, **Space**, **Enter**, or **Numpad Enter** opens the menu.
- A `command=` callback (if set on the button) also fires on click —
  it runs alongside opening the menu, not instead of it.
- Once the menu is open, **↑** / **↓** move highlight, **Enter**
  invokes the highlighted item, and **Esc** or a click outside closes
  the menu.
- A disabled or readonly DropdownButton ignores activation — neither
  `command` nor the menu fires.
- Hover, focus, and pressed visuals come from the active theme; no
  extra wiring is required.

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Localization & reactivity

### Localized labels

When localization is enabled, both the button's `text=` and each
item's `text=` are resolved as message keys through the active
catalog. Labels update automatically when the locale changes at
runtime; if a key has no translation, the literal string is shown — so
literal strings keep working whether or not localization is on.

```python
items = [
    ttk.ContextMenuItem("command", text="menu.open", command=lambda: print("open")),
    ttk.ContextMenuItem("command", text="menu.delete", command=lambda: print("delete")),
]
ttk.DropdownButton(app, text="button.file", items=items).pack()
```

### Reactive labels

Bind a `Signal[str]` via `textsignal` when the button label needs to
update dynamically.

```python
label = ttk.Signal("View")
ttk.DropdownButton(app, textsignal=label, items=[]).pack()

label.set("Layout")
```

!!! link "See [Signals](../../capabilities/signals/index.md) for reactive bindings, and [Localization](../../capabilities/localization.md) for catalogs and locale switching."

---

## Additional resources

### Related widgets

- [Button](button.md) — single-action trigger.
- [MenuButton](menubutton.md) — opens a Tk menu (no primary action).
- [ContextMenu](contextmenu.md) — same menu, shown on right-click instead of left.
- [ButtonGroup](buttongroup.md) — connected row of related buttons.
- [OptionMenu](../selection/optionmenu.md), [SelectBox](../selection/selectbox.md) — pick a value for a form.

### Framework concepts

- [Design System → Variants](../../design-system/variants.md)
- [Design System → Icons](../../design-system/icons.md)
- [Icons & Imagery](../../capabilities/icons/index.md)
- [Signals](../../capabilities/signals/index.md)
- [Localization](../../capabilities/localization.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)

### API reference

- [`ttkbootstrap.DropdownButton`](../../reference/widgets/DropdownButton.md)
- [`ttkbootstrap.ContextMenuItem`](../../reference/widgets/ContextMenuItem.md)
- [`ttkbootstrap.ContextMenu`](../../reference/widgets/ContextMenu.md)
