---
title: MenuButton
---

# MenuButton

A `MenuButton` is a button-shaped control whose primary purpose is to
**open a menu**. Reach for one for classic menu-bar entries — File,
Edit, View — and any place the menu *is* the interaction rather than
a side affordance on a primary action.

The attached menu is an ordinary Tk `Menu`, so it integrates with
platform conventions (the system menu on macOS; the classic Tk menu
on Windows and Linux) and Tk handles its keyboard navigation. For a
fully themed widget-backed menu with icons, shortcut hints, and rich
state semantics, see [DropdownButton](dropdownbutton.md) or
[ContextMenu](contextmenu.md).

<figure markdown>
![menubutton](../../assets/dark/widgets-menubutton.png#only-dark)
![menubutton](../../assets/light/widgets-menubutton.png#only-light)
</figure>

---

## Basic usage

Build a Tk `Menu`, attach it via `menu=`, and let `MenuButton` post it
when clicked.

```python
import ttkbootstrap as ttk

app = ttk.App()

m = ttk.Menu(app, tearoff=0)
m.add_command(label="Open", command=lambda: print("Open"))
m.add_command(label="Save", command=lambda: print("Save"))
m.add_separator()
m.add_command(label="Exit", command=app.destroy)

ttk.MenuButton(app, text="File", menu=m).pack(padx=20, pady=20)

app.mainloop()
```

---

## Common options

| Option | Purpose |
|---|---|
| `text` | Button label. Treated as a localization key when localization is enabled. |
| `menu` | The Tk `Menu` to post when the button is clicked. |
| `accent` | Semantic color: `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`. |
| `variant` | Visual weight: `solid` (default), `outline`, `ghost`, `text`. **No `link` variant.** |
| `density` | `default` or `compact`. |
| `surface` | Optional surface token; otherwise inherits from the parent. |
| `direction` | Pop direction: `below` (default), `above`, `left`, `right`, `flush`. |
| `icon` / `compound` / `icon_only` | Icon on the button face; chevron sits to the right. |
| `textsignal` | `Signal[str]` driving a reactive button label. |
| `textvariable` | Tk `Variable` alternative to `textsignal`. |

`MenuButton` itself does not fire a `command` on click — the attached
menu's items do.

### Accents and variants

`accent` and `variant` follow the same conventions as
[Button](button.md) — the same accent token reads the same way across
every ttkbootstrap widget. `solid`, `outline`, `ghost`, and `text`
variants are supported.

```python
ttk.MenuButton(app, text="File", accent="primary").pack(pady=4)
ttk.MenuButton(app, text="File", accent="primary", variant="outline").pack(pady=4)
ttk.MenuButton(app, text="File", accent="primary", variant="ghost").pack(pady=4)
```

!!! link "See [Design System → Variants](../../design-system/variants.md) for how accents and variants compose across widgets."

### Density

`density="compact"` reduces internal padding and shrinks the chevron
for menubuttons embedded in dense toolbars.

```python
ttk.MenuButton(app, text="View", density="compact").pack()
```

### Direction

`direction=` controls which side of the button the menu pops out from.
Accepted values are `'below'` (default), `'above'`, `'left'`,
`'right'`, and `'flush'`. Use it when the button sits near a screen
edge or inside a panel that would otherwise clip the menu.

```python
m = ttk.Menu(app, tearoff=0)
m.add_command(label="Recent")
ttk.MenuButton(app, text="More", direction="above", menu=m).pack()
```

### Icons

Icons are integrated through the style system, so they pick up the
button's accent and adapt to hover, focus, and disabled states. By
default the icon sits to the left of the label and the chevron sits
to the right.

```python
m = ttk.Menu(app, tearoff=0)
m.add_command(label="Rename")
m.add_command(label="Delete")

ttk.MenuButton(app, icon="three-dots-vertical", icon_only=True, menu=m).pack(pady=10)
```

!!! link "See [Icons & Imagery](../../capabilities/icons/index.md) for icon sizing, DPI handling, and recoloring behavior."

---

## Behavior

- **Click**, **Space**, or **Enter** posts the attached menu.
- A second click while the menu is visible closes it (Windows/Linux).
  On macOS, the system menu's state machine drives this gesture.
- Once the menu is open, **↑** / **↓** move highlight, **Enter**
  invokes the highlighted item, and **Esc** closes the menu.
- A disabled `MenuButton` ignores activation entirely and is skipped
  during focus traversal.
- Hover, focus, and pressed visuals come from the active theme; no
  extra wiring is required.

!!! note "macOS uses the native menu backend"
    On Aqua, Tk's class binding posts the menu through an NSMenu
    state machine that owns mouse and focus capture. `MenuButton`
    deliberately defers to that binding rather than posting the menu
    manually, so the system menu's selection and dismissal behavior
    is preserved.

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Events

`MenuButton` itself has no `command` — clicking it posts the menu.
Activation hooks live on the menu items: pass `command=` to each
`m.add_command(...)` entry, or back `add_checkbutton` /
`add_radiobutton` items with a Tk `Variable` and react to its trace.

```python
def on_open():
    ...

m = ttk.Menu(app, tearoff=0)
m.add_command(label="Open", command=on_open)

ttk.MenuButton(app, text="File", menu=m).pack()
```

---

## Patterns

### Cascading submenus

A Tk `Menu` can nest other menus through `add_cascade`. The
`MenuButton` hosts the top level; each cascade entry opens its child
menu.

```python
import ttkbootstrap as ttk

app = ttk.App()

submenu = ttk.Menu(app, tearoff=0)
submenu.add_command(label="Recent", command=lambda: print("Recent"))
submenu.add_command(label="Pinned", command=lambda: print("Pinned"))

main = ttk.Menu(app, tearoff=0)
main.add_cascade(label="Open", menu=submenu)
main.add_separator()
main.add_command(label="Save", command=lambda: print("Save"))

ttk.MenuButton(app, text="File", menu=main).pack(padx=20, pady=20)

app.mainloop()
```

### Check and radio entries

Tk's `Menu` supports `add_checkbutton` and `add_radiobutton` items
backed by Tk variables. The variable holds the current value; the
menu item reads and writes it on activation.

```python
import ttkbootstrap as ttk

app = ttk.App()

show_grid = ttk.BooleanVar(value=True)
sort_by = ttk.StringVar(value="name")

m = ttk.Menu(app, tearoff=0)
m.add_checkbutton(label="Show grid", variable=show_grid)
m.add_separator()
m.add_radiobutton(label="Sort by name", value="name", variable=sort_by)
m.add_radiobutton(label="Sort by date", value="date", variable=sort_by)

ttk.MenuButton(app, text="View", menu=m).pack(padx=20, pady=20)

app.mainloop()
```

### Rebuilding the menu at runtime

The attached menu is just a `tk.Menu` — mutate it directly with
`delete` and `add_*`, or build a fresh menu and reattach it via
`configure(menu=...)`. Use the second form when the entire item set
changes (e.g., a "Recent files" menu that depends on the selection).

```python
btn = ttk.MenuButton(app, text="Recent")
btn.pack()

def refresh(paths):
    m = ttk.Menu(btn, tearoff=0)
    for p in paths:
        m.add_command(label=p, command=lambda p=p: print("open", p))
    btn.configure(menu=m)
```

---

## Localization & reactivity

### Localized button label

When localization is enabled, the value passed to `text=` is treated
as a message key and resolved through the active catalog. The button
label updates automatically when the locale changes at runtime; if the
key has no translation, the literal string is shown — so `text="File"`
works whether or not localization is on.

```python
ttk.MenuButton(app, text="menu.file", menu=m).pack()
```

### Reactive button label

Bind a `Signal[str]` via `textsignal` when the label needs to update
dynamically.

```python
label = ttk.Signal("View")
ttk.MenuButton(app, textsignal=label, menu=m).pack()

label.set("Layout")
```

### Localizing menu items

Menu item labels are passed straight through to Tk and are *not*
re-resolved on locale change. To localize them, resolve the messages
at construction time with `MessageCatalog.translate()` (or its alias),
and rebuild the affected menus when the locale switches.

```python
from ttkbootstrap import MessageCatalog

_ = MessageCatalog.translate

m = ttk.Menu(app, tearoff=0)
m.add_command(label=_("menu.open"), command=lambda: print("open"))
m.add_command(label=_("menu.save"), command=lambda: print("save"))

ttk.MenuButton(app, text="menu.file", menu=m).pack()
```

For menus whose item labels participate in the localization lifecycle
the same way the button does, use [DropdownButton](dropdownbutton.md)
or [ContextMenu](contextmenu.md) — those resolve every item's `text=`
through the catalog and refresh on locale change.

!!! link "See [Signals](../../capabilities/signals/index.md) for reactive bindings, and [Localization](../../capabilities/localization.md) for catalogs and locale switching."

---

## When should I use MenuButton?

Use `MenuButton` when:

- the control is primarily a **menu entry point** (File, Edit, View).
- you want native-style menu behavior — Tk-driven keyboard navigation
  and platform conventions.
- the menu shape maps cleanly to Tk's `Menu` model
  (`add_command`, `add_checkbutton`, `add_radiobutton`,
  `add_cascade`, `add_separator`).

Prefer a different control when:

- a primary action plus a small dropdown of related choices →
  use [DropdownButton](dropdownbutton.md).
- the menu should appear on right-click on top of arbitrary content →
  use [ContextMenu](contextmenu.md).
- you want a fully themed menu with icons, shortcut hints, and rich
  state semantics → use [DropdownButton](dropdownbutton.md) or
  [ContextMenu](contextmenu.md). Those use a themed widget-backed
  menu; `MenuButton` uses Tk's native `Menu`.
- a single one-shot action → use [Button](button.md).

---

## Related widgets

- [DropdownButton](dropdownbutton.md) — primary action plus a themed dropdown of choices.
- [ContextMenu](contextmenu.md) — themed pop-up menu, shown on right-click.
- [Button](button.md) — single-action trigger.
- [ButtonGroup](buttongroup.md) — connected row of related buttons.

---

## Reference

- **API reference:** [`ttkbootstrap.MenuButton`](../../reference/widgets/MenuButton.md)
- **Related guides:**
    - [Design System → Variants](../../design-system/variants.md)
    - [Design System → Icons](../../design-system/icons.md)
    - [Icons & Imagery](../../capabilities/icons/index.md)
    - [Signals](../../capabilities/signals/index.md)
    - [Localization](../../capabilities/localization.md)
    - [State & Interaction](../../capabilities/state-and-interaction.md)
