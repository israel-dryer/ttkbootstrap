---
title: Toolbars
---

# Toolbars

A toolbar is a horizontal strip of actions — buttons, labels, status
indicators, search boxes — that sits at the top of a window or pane.
ttkbootstrap's [`Toolbar`](../widgets/application/toolbar.md) is a thin
layout container with helpers for the common building blocks plus
optional window controls for custom titlebars.

This guide covers:

- **AppShell integration** — the primary path: every `AppShell` already
  has a toolbar
- **Standalone toolbars** — when you want a toolbar without an `AppShell`
- **Adding items** — buttons, labels, separators, spacers, custom widgets
- **Layout** — left/right grouping with the spacer idiom
- **Density**
- **Frameless windows and custom titlebars**
- **Keyboard access and pairing with menus and shortcuts**

---

## In an AppShell

The most common toolbar in ttkbootstrap is the one
[`AppShell`](../widgets/application/appshell.md) builds for you.
It sits at the top of the window, wired to the `SideNav`, and is
exposed as `shell.toolbar`:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(1000, 650))
shell.add_page("home", text="Home", icon="house")
shell.add_page("docs", text="Docs", icon="file-earmark-text")

shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)
shell.toolbar.add_button(
    icon="bell",
    command=lambda: ttk.MessageBox.show_info("0 alerts"),
)

shell.mainloop()
```

`AppShell` pre-populates the toolbar with three things — left to right:

1. The hamburger button (toggles the side nav).
2. The title label (`title=` from the `AppShell` constructor).
3. A spacer.

Anything you add through `shell.toolbar.add_*` lands **after the
spacer**, which is why your buttons appear flush against the right
edge. You can keep adding spacers to push later items further right,
or insert a left-anchored item by reaching into `shell.toolbar` and
using `add_widget(..., side='left')`.

If you don't want a toolbar at all, pass `show_toolbar=False`:

```python
shell = ttk.AppShell(title="My App", show_toolbar=False)
```

---

## Standalone toolbars

Outside `AppShell`, `Toolbar` is a regular `Frame` — `pack`, `grid`,
or `place` it wherever you want one:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Toolbars", size=(720, 420))

toolbar = ttk.Toolbar(app)
toolbar.pack(side="top", fill="x")

toolbar.add_button(icon="house", command=lambda: print("home"))
toolbar.add_button(icon="folder", command=lambda: print("open"))
toolbar.add_separator()
toolbar.add_label(text="Untitled.txt", font="heading-sm")
toolbar.add_spacer()
toolbar.add_button(icon="gear", command=lambda: print("settings"))

app.mainloop()
```

Toolbars don't have to live at the top of the window — secondary
toolbars inside a pane or above a list view are common. Pair them with
`density="compact"` (see below) to keep them visually subordinate.

---

## Adding items

`Toolbar` exposes one helper per common item type. Each returns the
created widget so you can keep a reference for later configuration.

| Method | Adds |
|---|---|
| `add_button(icon=, text=, command=, accent=, variant=, ...)` | A `Button` |
| `add_label(text=, icon=, font=, ...)` | A `Label` |
| `add_separator(length=16)` | A vertical `Separator` |
| `add_spacer()` | A flexible expanding space |
| `add_widget(widget, **pack_kwargs)` | Any widget you've already built |

### Buttons

Toolbar buttons default to the `ghost` variant — minimal chrome, no
background — which reads correctly on a chrome surface. Pass `icon`
alone for an icon-only button; pass both `icon` and `text` for a
labelled button:

```python
toolbar.add_button(icon="play", command=play)               # icon only
toolbar.add_button(icon="play", text="Play", command=play)  # icon + label
toolbar.add_button(text="Save", command=save)               # text only
toolbar.add_button(icon="trash", accent="danger", command=delete)
```

Override the default variant per call (`variant="solid"`,
`variant="outline"`) or for the whole toolbar by passing
`button_variant=` to the constructor.

### Labels and separators

```python
toolbar.add_label(text="Project / main", font="heading-sm")
toolbar.add_separator()                # 16 px vertical line (default)
toolbar.add_separator(length=None)     # stretches to toolbar height
```

### Custom widgets

For widgets the helpers don't cover — a search entry, a `SelectBox`,
a `Toggle` — create them with `toolbar.content` as the parent, then
hand them to `add_widget()`:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Custom widgets", size=(720, 80))

toolbar = ttk.Toolbar(app)
toolbar.pack(side="top", fill="x")

search = ttk.TextEntry(toolbar.content, width=24, show_message=False)
toolbar.add_widget(search, padx=8)

theme_picker = ttk.SelectBox(toolbar.content, items=["Light", "Dark"])
toolbar.add_widget(theme_picker)

app.mainloop()
```

`add_widget()` packs the widget left-to-right, defaulting to
`side="left"` and `padx=2`. Pass any pack keyword arguments to
override — `side="right"` is useful for items that should sit at the
far end without a spacer in front of them.

The `toolbar.content` frame matters: widgets parented directly to
`toolbar` (rather than `toolbar.content`) end up alongside the
window-controls frame and won't lay out the way you expect.

---

## Layout: the spacer idiom

Items are packed left-to-right in the order you add them. To push
subsequent items to the right edge, drop in `add_spacer()`. A spacer
is just an empty `Frame` configured with `expand=True` — it eats all
the slack, so anything added after it ends up on the right:

```python
toolbar.add_button(icon="house")        # left
toolbar.add_button(icon="folder")       # left
toolbar.add_spacer()                    # — empty stretch —
toolbar.add_button(icon="bell")         # right
toolbar.add_button(icon="gear")         # right
```

Use *two* spacers to make a left / center / right layout:

```python
toolbar.add_button(icon="play")         # left
toolbar.add_spacer()
toolbar.add_label(text="Now playing")   # center
toolbar.add_spacer()
toolbar.add_button(icon="gear")         # right
```

Reach for spacers before reaching for `padx=` magic numbers — spacers
adapt to the window width; padding offsets don't.

---

## Density

Toolbars come in two densities:

```python
ttk.Toolbar(app, density="default")     # comfortable — primary toolbars
ttk.Toolbar(app, density="compact")     # tighter — secondary toolbars
```

The toolbar's density is inherited by buttons added through
`add_button`. To override for one button, pass `density=` to that
call:

```python
toolbar = ttk.Toolbar(app, density="compact")
toolbar.add_button(icon="play")                       # compact
toolbar.add_button(icon="cog", density="default")     # comfortable, this one only
```

`AppShell` exposes the same control through its `toolbar_density`
constructor argument:

```python
shell = ttk.AppShell(title="My App", toolbar_density="compact")
```

---

## Frameless windows and custom titlebars

When you want a single integrated chrome bar with no native titlebar,
use a frameless window. The toolbar grows minimize, maximize, and
close buttons on its right edge, and dragging the toolbar moves the
window.

The cleanest path is `AppShell(frameless=True)`, which removes the
native chrome *and* enables window controls and dragging on the
toolbar in one step:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(900, 580), frameless=True)
shell.add_page("home", text="Home", icon="house")
shell.add_page("settings", text="Settings", icon="gear")

shell.toolbar.add_button(icon="bell")

shell.mainloop()
```

For a standalone `Toolbar`, the equivalent is two flags on the
toolbar plus `override_redirect=True` on the window:

```python
import ttkbootstrap as ttk

app = ttk.App(title="My App", size=(900, 580), override_redirect=True)

toolbar = ttk.Toolbar(app, show_window_controls=True, draggable=True)
toolbar.pack(side="top", fill="x")

toolbar.add_label(text="My App", font="heading-md")
toolbar.add_spacer()
toolbar.add_button(icon="bell")

app.mainloop()
```

`draggable=True` is enabled implicitly when `show_window_controls=True`,
so you can omit it in the snippet above. The dragging surface covers
the toolbar background, the spacer, and the title label — clicking on a
button still fires the button.

The window-control buttons are reachable through properties so you can
restyle them or rebind them:

```python
toolbar.minimize_button     # Button | None
toolbar.maximize_button     # Button | None
toolbar.close_button        # Button | None
```

Each is `None` when `show_window_controls=False`.

---

## Keyboard access

Toolbar items are real widgets, so they pick up the standard ttk focus
chain — users can `Tab` between toolbar buttons and press
`Space`/`Return` to fire them. The `Toolbar` itself doesn't add
shortcut bindings; pair it with the
[Shortcuts](../reference/app/Shortcuts.md) registry for app-wide
keyboard equivalents:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Toolbars + shortcuts", size=(720, 420))

toolbar = ttk.Toolbar(app)
toolbar.pack(side="top", fill="x")

def save():
    print("save")

toolbar.add_button(icon="floppy", command=save)

shortcuts = ttk.get_shortcuts()
shortcuts.register("save", "Mod+S", save)
shortcuts.bind_to(app)

app.mainloop()
```

See the [App Settings guide](app-settings.md) for the full Shortcuts
wiring story.

---

## Pairing with menus and shortcuts

Toolbars are one entry point — keep them consistent with the rest of
your app's command surface.

- **Menus.** Use a top-level menu bar (see `MenuManager` in
  [App](../widgets/application/app.md)) for the full action list (File
  / Edit / View / Help). Toolbars surface the most common subset of
  those actions for one-click access. Don't put every menu item on the
  toolbar.
- **Context menus.** [ContextMenu](../widgets/actions/contextmenu.md)
  covers right-click affordances and pairs with toolbar buttons that
  carry the same actions.
- **Shortcuts.** Every toolbar button should have a keyboard
  equivalent for power users.

---

## Patterns and tips

### Capture the widget; don't recreate

Re-adding a button each time its state changes triggers a relayout
pass and breaks any references you held. Capture the returned widget
once and call `configure()` on it instead:

```python
play_btn = toolbar.add_button(icon="play", command=toggle_play)
# ...later...
play_btn.configure(icon="pause")
```

### Let the toolbar's surface flow through

`Toolbar` inherits a surface token from its parent (or `chrome` when
inside an `AppShell`). When you build custom widgets for
`add_widget()`, leave their `surface=` unset — the toolbar's helpers
do the same, and the result blends correctly when the theme switches.

### No automatic overflow

`Toolbar` doesn't currently fold items into a chevron menu when the
window narrows; items stay packed at their natural size and clip
against the window edge. Plan a fixed set of toolbar actions and put
the long tail in a menu or `DropdownButton`.

---

## Additional resources

- [Toolbar widget reference](../widgets/application/toolbar.md)
- [AppShell](../widgets/application/appshell.md) — built-in toolbar
- [SideNav](../widgets/navigation/sidenav.md) — paired with toolbar in
  the typical desktop layout
- [ContextMenu](../widgets/actions/contextmenu.md) — right-click
  actions
- [Navigation guide](navigation.md) — toolbars in context
- [App Structure guide](app-structure.md) — where the toolbar fits in a
  full app
