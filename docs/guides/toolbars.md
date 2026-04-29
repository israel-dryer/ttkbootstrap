---
title: Toolbars
---

# Toolbars

A toolbar is a horizontal strip of actions — buttons, labels,
separators, search boxes, status indicators — that sits at the top of a
window or pane. ttkbootstrap's `Toolbar` is a thin layout container with
helpers for the common building blocks plus optional window controls
for custom titlebars.

This guide covers:

- **Building a toolbar** — buttons, labels, separators, custom widgets
- **Layout** — left-to-right flow and right-aligning with `add_spacer()`
- **Density and styling**
- **Window controls** — using `Toolbar` as a custom titlebar
- **AppShell integration**
- **Pairing with menus and shortcuts**

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App(title="Toolbars", size=(720, 420))

toolbar = ttk.Toolbar(app)
toolbar.pack(side="top", fill="x")

toolbar.add_button(icon="house", command=lambda: print("home"))
toolbar.add_button(icon="folder", command=lambda: print("open"))
toolbar.add_separator()
toolbar.add_label(text="Untitled.txt", font="heading-sm")
toolbar.add_spacer()                                         # push the rest right
toolbar.add_button(icon="gear", command=lambda: print("settings"))

app.mainloop()
```

`Toolbar` is a `Frame`, so `pack` / `grid` / `place` work normally —
toolbars don't have to live at the top of the window.

---

## Adding items

`Toolbar` exposes one helper per common item type. All of them return
the created widget, so you can keep a reference for later
configuration.

| Method | Adds |
|---|---|
| `add_button(icon=, text=, command=, accent=, variant=, ...)` | `Button` |
| `add_label(text=, icon=, font=, ...)` | `Label` |
| `add_separator(length=16)` | Vertical `Separator` |
| `add_spacer()` | Flexible expanding space |
| `add_widget(widget, **pack_kwargs)` | Any widget you've already built |

### Buttons

By default toolbar buttons use the `ghost` variant — minimal chrome,
no background. Pass `icon` alone for an icon-only button; pass `text`
for label + icon:

```python
toolbar.add_button(icon="play", command=play)               # icon only
toolbar.add_button(icon="play", text="Play", command=play)  # icon + label
toolbar.add_button(icon="trash", accent="danger", command=delete)
```

Override the default variant per call (`variant="solid"`,
`variant="outline"`) or for the whole toolbar (`button_variant=` on the
constructor).

### Labels and separators

```python
toolbar.add_label(text="Project / main", font="heading-sm")
toolbar.add_separator()                          # 16 px vertical line
toolbar.add_separator(length=None)               # stretches to toolbar height
```

### Custom widgets

For widgets the helpers don't cover — a search entry, a
`SelectBox`, a `Toggle` — create them with `toolbar.content` as the
parent, then hand them to `add_widget()`:

```python
search = ttk.TextEntry(toolbar.content, placeholder="Search...")
toolbar.add_widget(search, padx=8)

theme_picker = ttk.SelectBox(toolbar.content, items=["Light", "Dark"])
toolbar.add_widget(theme_picker)
```

`add_widget()` packs the widget left-to-right, defaulting to
`side="left"` and `padx=2`. Pass `pack` keyword arguments to override.

---

## Layout: left, right, and grouped

Items are packed left-to-right in the order you add them. To push
subsequent items to the right edge, drop in `add_spacer()`:

```python
toolbar.add_button(icon="house")        # left
toolbar.add_button(icon="folder")       # left
toolbar.add_spacer()                    # — empty stretch —
toolbar.add_button(icon="bell")         # right
toolbar.add_button(icon="gear")         # right
```

For three groups (left / center / right), use two spacers around the
middle group:

```python
toolbar.add_button(icon="play")
toolbar.add_spacer()
toolbar.add_label(text="Now playing", font="heading-sm")
toolbar.add_spacer()
toolbar.add_button(icon="gear")
```

---

## Density

Toolbars come in two densities. The default is comfortable for primary
toolbars; `compact` shrinks button padding for secondary or in-pane
toolbars:

```python
ttk.Toolbar(app, density="compact")
```

Per-button density wins over the toolbar default — pass `density=` to
`add_button` for one-off overrides.

---

## Window controls (custom titlebars)

Pass `show_window_controls=True` to add minimize, maximize, and close
buttons on the right edge. This pairs naturally with a frameless
window:

```python
import ttkbootstrap as ttk

app = ttk.App(title="My App", size=(900, 580))
app.overrideredirect(True)              # remove native titlebar

toolbar = ttk.Toolbar(app, show_window_controls=True, draggable=True)
toolbar.pack(side="top", fill="x")

toolbar.add_label(text="My App", font="heading-md")
toolbar.add_spacer()
toolbar.add_button(icon="bell")

app.mainloop()
```

`draggable=True` lets the user move the window by dragging the
toolbar — implicitly enabled when `show_window_controls=True`.

The window-control buttons are reachable through properties so you can
restyle or extend them:

```python
toolbar.minimize_button
toolbar.maximize_button
toolbar.close_button
```

---

## Inside an AppShell

[AppShell](../widgets/application/appshell.md) wires a `Toolbar`,
`SideNav`, and `PageStack` together for you. The toolbar is exposed
through `shell.toolbar` so you can populate it like any other:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(1000, 650))
shell.add_page("home", text="Home", icon="house")
shell.add_page("docs", text="Docs", icon="file-earmark-text")

shell.toolbar.add_spacer()
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)
shell.toolbar.add_button(icon="bell", command=lambda: ttk.MessageBox.show_info("0 alerts"))

shell.mainloop()
```

If you don't want a toolbar at all, pass `show_toolbar=False` to
`AppShell`. To turn it into a custom titlebar, pass
`show_window_controls=True` and `draggable=True` to `AppShell` and they
flow through to the toolbar.

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
- **Keyboard shortcuts.** Register
  [Shortcuts](../reference/app/Shortcuts.md) so power users get a
  keyboard equivalent for every toolbar action — see the
  [App Settings guide](app-settings.md) for the wiring.

---

## Patterns and tips

### Group with spacers, not magic numbers

`add_spacer()` adapts to the window width; padding offsets don't.
Reach for spacers before reaching for `padx=`.

### Reuse the toolbar's `surface`

`Toolbar` already inherits a surface token from its parent. When you
build custom widgets for `add_widget()`, leave their `surface=` unset —
the toolbar's helpers do the same and the result blends correctly when
the theme switches.

### Don't repaint on every action

Capture the returned widget once, then call `configure(...)` on it
rather than removing and re-adding the button. The toolbar is a layout
container; rearranging it triggers a relayout pass.

```python
play_btn = toolbar.add_button(icon="play", command=toggle_play)
# ...
play_btn.configure(icon="pause")
```

---

## Additional resources

- [Toolbar widget reference](../widgets/navigation/toolbar.md)
- [AppShell](../widgets/application/appshell.md) — built-in toolbar
- [SideNav](../widgets/navigation/sidenav.md) — paired with toolbar in
  the typical desktop layout
- [ContextMenu](../widgets/actions/contextmenu.md) — right-click
  actions
- [Navigation guide](navigation.md) — toolbars in context
- [App Structure guide](app-structure.md) — where the toolbar fits in a
  full app
