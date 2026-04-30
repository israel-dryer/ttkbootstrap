---
title: ContextMenu
---

# ContextMenu

A `ContextMenu` is a pop-up menu for right-click and other contextual
actions — file browsers, list rows, text fields, custom canvases.
Unlike Tk's native `Menu`, it composes ttkbootstrap widgets inside a
themed Toplevel, so the menu picks up the active theme, density, and
icon system the same way the rest of the framework does. On macOS it
materializes as a native `tk.Menu` (NSMenu) so popups integrate with
the system; the public API is identical across platforms.

This page covers the `ContextMenu` widget. For a button-first action
with a small dropdown, see [DropdownButton](dropdownbutton.md). For a
menu attached to a button label, see [MenuButton](menubutton.md).

---

## Framework integration

**Design system**

- `density="default"` (default) or `density="compact"` controls item
  typography so menus match the trigger widget's font size.
- Items render with internal `context-item`, `context-check`, and
  `context-radio` variants — the menu picks them automatically and
  they are not configurable per item.

**Signals & events**

- Per-item `command=` runs on activation and the menu closes
  automatically.
- `on_item_click(callback)` registers a single handler that fires for
  every item activation; the callback receives a dict with `type`,
  `text`, and `value` keys. Useful when item handling is centralized.

**Icons**

- Each item accepts an `icon=` name. Items without icons reserve the
  icon column with an `'empty'` placeholder so labels stay aligned.
- Icons re-render on theme change and follow the same recoloring
  rules as the rest of the icon system.

**Localization**

- Each item's `text=` is treated as a message key when localization
  is enabled and updates automatically on locale change. Literal
  strings without a translation pass through unchanged.

**Positioning and triggering**

- `target=` selects the widget the menu attaches to (defaults to
  `master`; pass `target=None` to opt out).
- `trigger=` chooses the activation gesture and auto-binds it to
  `target`. The default `'right-click'` binds the portable gesture:
  `<Button-3>` on Windows/Linux, `<Button-2>` and
  `<Control-Button-1>` on macOS.
- `anchor=`, `attach=`, and `offset=` control alignment when `show()`
  is called without an explicit position.

---

## Basic usage

Create the menu, add items, and let the default
`trigger='right-click'` bind the gesture for you.

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.ContextMenu(app)
menu.add_command(text="Open", icon="folder-open", command=lambda: print("Open"))
menu.add_command(text="Rename", command=lambda: print("Rename"))
menu.add_separator()
menu.add_command(text="Delete", icon="trash", command=lambda: print("Delete"))

app.mainloop()
```

`target=` defaults to `master`, so right-clicking anywhere on the
window opens the menu at the cursor. Pass `target=widget` to attach
the gesture to a single widget instead.

!!! note "Cross-platform right-click"
    Avoid binding `<Button-3>` directly — it does not capture the
    macOS Ctrl+click gesture. The default `trigger='right-click'`
    wraps the platform-correct binding for you.

---

## When to use

Use `ContextMenu` when:

- actions are contextual to a widget, list row, or region
- the menu should follow the app's theme (light/dark, density)
- items need icons, keyboard-shortcut hints, or rich state semantics

### Consider a different control when…

- A button-first action with a small dropdown of choices →
  [DropdownButton](dropdownbutton.md).
- A persistent menu attached to a button label →
  [MenuButton](menubutton.md).
- A primary action that triggers a one-shot operation →
  [Button](button.md).

---

## Appearance

A `ContextMenu` has a single visual silhouette — a bordered,
overlay-surface frame on Win/Linux, the system menu on macOS. The
options that affect appearance are deliberately limited.

### Density

`density="compact"` reduces item padding and label sizing for menus
attached to dense toolbars or compact widgets, so the menu visually
matches its trigger.

```python
menu = ttk.ContextMenu(app, density="compact")
```

### Width

`minwidth=` (default `150`) and `width=` set the menu's pixel width
on the themed backend. Use `minwidth` to keep narrow menus from
collapsing around short labels; use `width` to lock the menu to a
fixed footprint.

```python
menu = ttk.ContextMenu(app, minwidth=200)
```

These options are stored but have no effect on the macOS native
backend — system menus size themselves.

---

## Examples & patterns

### Item types

Four item types cover most menu shapes.

```python
import ttkbootstrap as ttk

app = ttk.App()
menu = ttk.ContextMenu(app)

# Command — standard action
menu.add_command(text="Open", command=lambda: print("Open"))

# Checkbutton — independent on/off option
menu.add_checkbutton(text="Show hidden files", value=True)

# Radiobutton — pick one from a set (share a Variable)
sort_var = ttk.StringVar(value="name")
menu.add_radiobutton(text="Sort by name", value="name", variable=sort_var)
menu.add_radiobutton(text="Sort by date", value="date", variable=sort_var)

# Separator — visual divider
menu.add_separator()

app.mainloop()
```

### Keyboard-shortcut hints and disabled items

`add_command()` accepts `shortcut=` and `disabled=`. The shortcut
display is platform-aware — pass a registered key from the
[`Shortcuts`](../../reference/app/Shortcuts.md) service, a modifier
pattern (`'Mod+S'`), or a literal display string. The hint text is
informational only; it does not bind the keystroke.

```python
menu.add_command(text="Save", shortcut="Mod+S", command=on_save)
menu.add_command(text="Delete", disabled=True, command=on_delete)
```

### Icons

Items use the same icon system as other ttkbootstrap widgets. The
icon column is reserved across the whole menu, so labels stay aligned
even when only some items have icons.

```python
menu.add_command(text="Settings", icon="gear", command=on_settings)
menu.add_command(text="Refresh", icon="arrow-clockwise", command=on_refresh)
menu.add_command(text="About", command=on_about)  # no icon — column still reserved
```

!!! link "See [Icons & Imagery](../../capabilities/icons/index.md) for icon sizing, DPI handling, and recoloring behavior."

### Looking up items by key

Pass `key=` to give an item a stable identifier; otherwise one is
auto-generated. The key works with `item()`, `configure_item()`,
`remove_item()`, `move_item()`, and `insert_item()`. `keys()` returns
the current order.

```python
menu.add_command(text="Save", key="save", command=on_save)
menu.add_command(text="Discard", key="discard", command=on_discard)

# disable just the Save item
menu.configure_item("save", state="disabled")

# remove an item
menu.remove_item("discard")
```

!!! note "Native backend caveat"
    On macOS, `item()` returns the original spec dict instead of a
    Tk widget — there's no per-item widget on the native backend.
    `configure_item()` works the same way on both backends through
    the underlying widget or `entryconfigure` call.

### Centralized item handling

`on_item_click(callback)` registers a single handler that fires for
every item activation. The callback receives a dict with `type`,
`text`, and `value` (the toggled bool for checkbuttons, the radio
value for radiobuttons, `None` for commands).

```python
def handle_click(info):
    print(info["type"], info["text"], info["value"])

menu.on_item_click(handle_click)
```

### Replacing items at runtime

`items()` is both a getter and a setter. Pass a list of
`ContextMenuItem`s to replace the menu's contents — useful when the
items depend on selection or context.

```python
menu = ttk.ContextMenu(app)

def refresh_for(selection):
    items = [ttk.ContextMenuItem(type="command", text="Open")]
    if selection.deletable:
        items.append(ttk.ContextMenuItem(type="command", text="Delete"))
    menu.items(items)
```

### Attach to a widget instead of the cursor

When the menu should align to a widget's edge — a row anchor button,
a toolbar control — pass `target=widget` with `anchor`, `attach`, and
`offset`, then call `show()` (no position) from your own trigger.

```python
menu = ttk.ContextMenu(
    app,
    target=my_button,
    anchor="nw",
    attach="se",
    trigger=None,  # opt out of the default right-click binding
)

my_button.bind("<Button-1>", lambda e: menu.show())
```

`anchor` is the alignment point on the menu; `attach` is the point
on the target. The default `offset` is `(10, 0)` to clear the focus
ring on trigger buttons — pass `offset=(0, 0)` when you want the menu
flush against the target.

---

## Behavior

- The default `trigger='right-click'` binds `<Button-3>` on
  Windows/Linux and `<Button-2>` plus `<Control-Button-1>` on macOS.
- **Down / Up** moves the highlight between actionable items
  (separators are skipped).
- **Enter** activates the highlighted item.
- **Escape** closes the menu without firing a command.
- The menu hides automatically when the user clicks outside, unless
  `hide_on_outside_click=False` is set at construction.
- Item commands fire on click and close the menu; the
  `on_item_click` callback fires too.

!!! note "macOS uses a native menu backend"
    On macOS (Aqua), `ContextMenu` renders as a native NSMenu rather
    than a themed Toplevel. Sizing options (`minwidth`, `width`,
    `minheight`, `height`, `density`) are stored for `cget` parity
    but have no visual effect — system menus control sizing and
    typography. `item()` returns a spec dict, not a widget.

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Localization & reactivity

When localization is enabled, every item's `text=` is treated as a
message key and resolved through the active catalog. Labels update
automatically on locale change. Literal strings that have no
translation pass through unchanged, so a mix of localized and literal
labels works in the same menu.

```python
menu.add_command(text="menu.open", command=on_open)
menu.add_command(text="Delete", command=on_delete)  # literal
```

`ContextMenu` itself does not bind reactive signals to item labels —
items are added imperatively and their text is fixed at construction.
For dynamic labels, rebuild the affected items via `items()` or
`configure_item()`.

!!! link "See [Localization](../../capabilities/localization.md) for catalogs and runtime locale switching."

---

## Additional resources

### Related widgets

- [DropdownButton](dropdownbutton.md) — primary action plus a menu of choices.
- [MenuButton](menubutton.md) — a button that opens a Tk menu.
- [Button](button.md) — single-action trigger.

### Framework concepts

- [Icons & Imagery](../../capabilities/icons/index.md)
- [Localization](../../capabilities/localization.md)
- [State & Interaction](../../capabilities/state-and-interaction.md)

### API reference

- [`ttkbootstrap.ContextMenu`](../../reference/widgets/ContextMenu.md)
- [`ttkbootstrap.ContextMenuItem`](../../reference/widgets/ContextMenuItem.md)
- [`ttkbootstrap.Shortcuts`](../../reference/app/Shortcuts.md) — keyboard-shortcut display lookup.
