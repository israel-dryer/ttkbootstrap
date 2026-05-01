---
title: Toolbar
---

# Toolbar

`Toolbar` is a **horizontal action-chrome strip** — a `Frame` subclass
with builder helpers for icon buttons, labels, separators, spacers,
and arbitrary widgets. It's the action-host that sits at the top of
a window or pane, not a navigation primitive.

[`AppShell`](appshell.md) constructs one for you and surfaces it as
`shell.toolbar`; that's how most apps will encounter it. Standalone
construction is supported and useful for custom titlebars (with
`show_window_controls=True` + a frameless `Toplevel`) or for any
horizontal action strip inside a panel.

<figure markdown>
![toolbar](../../assets/dark/widgets-toolbar.png#only-dark)
![toolbar](../../assets/light/widgets-toolbar.png#only-light)
</figure>

---

## Basic usage

Items are added left-to-right through `add_*` builders. Use
`add_spacer()` to push subsequent items to the right edge.

```python
import ttkbootstrap as ttk

app = ttk.App()

toolbar = ttk.Toolbar(app, surface="chrome")
toolbar.pack(fill="x")

toolbar.add_button(icon="list", command=lambda: print("menu"))
toolbar.add_separator()
toolbar.add_label(text="My App", font="heading-md")
toolbar.add_spacer()
toolbar.add_button(icon="gear", command=lambda: print("settings"))

app.mainloop()
```

Each builder returns the widget it created, so you can capture and
configure it later:

```python
save = toolbar.add_button(icon="save", command=on_save)
save.configure(state="disabled")
```

---

## Item types

Toolbar exposes five builders. Each forwards the remaining `**kwargs`
to the underlying primitive, so anything that primitive accepts
works here.

| Builder | Adds | Returns |
|---|---|---|
| `add_button(icon=, text=, command=, accent=, variant=, **kwargs)` | A [Button](../actions/button.md). Defaults to icon-only when `icon` is set without `text`. Inherits `density`, `surface`, and `button_variant` from the toolbar (per-call kwargs override). | `Button` |
| `add_label(text=, icon=, font=, **kwargs)` | A [Label](../data-display/label.md). Inherits `surface` from the toolbar. Auto-bound to drag if the toolbar is draggable. | `Label` |
| `add_separator(length=16, **kwargs)` | A vertical [Separator](../layout/separator.md). Pass `length=None` for a full-height stretch separator. | `Separator` |
| `add_spacer()` | A flexible `Frame` that pushes subsequent items to the right (`expand=True, fill="both"`). Auto-bound to drag if draggable. | `Frame` |
| `add_widget(widget, **pack_kwargs)` | Any pre-built widget. Defaults to `side="left", padx=2`; override via `pack_kwargs`. | `Widget` |

### Custom widgets

`add_widget()` packs an existing widget into the toolbar's content
area. **The widget must already be parented to `toolbar.content`** —
otherwise it gets packed wherever its actual parent is, silently.

```python
search = ttk.Entry(toolbar.content)   # parent must be toolbar.content
toolbar.add_widget(search, padx=8)
```

!!! warning "Parent enforcement is silent"
    `add_widget()` does not validate the widget's parent. A widget
    parented to a different frame is still call-`pack`-ed, but it
    appears at the wrong parent — not inside the toolbar. Always
    construct the widget with `toolbar.content` as its parent.

### Stretch separators vs fixed-length

`length=16` (default) is a fixed-pixel divider. `length=None`
stretches the separator to the toolbar's full height — useful as a
hairline that visually anchors a section.

```python
toolbar.add_separator(length=None)   # full-height divider
```

---

## Common options

| Option | Purpose |
|---|---|
| `surface` | Background token for the toolbar. Children of `add_button` / `add_label` inherit it (per-call `surface=` overrides). Defaults to the parent's surface (typically `content`). Common toolbar choices are `chrome` and `card`. |
| `accent` | On Toolbar (a Frame subclass), `accent` is rerouted by the bootstyle constructor to set `surface` instead — it does **not** tint the toolbar's frame. Pass `surface=` directly for clarity. |
| `density` | `'default'` or `'compact'`. Read by `add_button()` for each button's density. Also drives the toolbar's default padding when `padding` is unset (`(3, 1)` for compact, `3` for default). |
| `button_variant` | Default variant for buttons added via `add_button`. Defaults to `'ghost'`. Per-call `variant=` overrides. |
| `show_window_controls` | When `True`, builds minimize / maximize / close buttons on the right edge and **auto-enables `draggable`**. Default `False`. |
| `draggable` | When `True`, `<Button-1>` + `<B1-Motion>` on the toolbar (and on label / spacer items) drag the toplevel window. Default `False`. Auto-enabled when `show_window_controls=True`. |
| `padding` | Internal padding around the toolbar. If unset, derived from `density`. Accepts an int or a `(padx, pady)` tuple. |
| `show_border` | Inherited from `Frame`. Adds a 1px border. |
| `width` / `height` | Optional fixed footprint; rarely needed. |

### Surface and density

```python
ttk.Toolbar(app, surface="chrome").pack(fill="x")
ttk.Toolbar(app, surface="card", density="compact").pack(fill="x")
```

`surface="chrome"` matches the muted top-bar token AppShell uses; it
reads as a separate band against the page background. `density="compact"`
shrinks every button added through `add_button()` and tightens
toolbar padding to `(3, 1)`.

!!! link "See [Design System → Surfaces](../../design-system/surfaces.md) for the full surface palette and intended uses."

### Window controls and dragging

Pair `show_window_controls=True` with an undecorated `App` (or
`Toplevel`) to build a custom titlebar.

```python
app = ttk.App(override_redirect=True)

bar = ttk.Toolbar(app, show_window_controls=True)
bar.pack(fill="x")
bar.add_label(text="My App", font="heading-md")
```

The kwarg name varies by class: [`App`](app.md) accepts
`override_redirect=`, [`Toplevel`](toplevel.md) accepts
`overrideredirect=` (matching Tk's native option), and
[`AppShell`](appshell.md) accepts `frameless=`.

The trio is rendered as ghost icon-only `Button`s with hard-coded
icons (`dash-lg` minimize, `app` / `copy` maximize-restore, `x-lg`
close). `draggable` activates implicitly because window controls
imply a custom titlebar. Reach the buttons via the
`minimize_button`, `maximize_button`, and `close_button` properties
(each returns `None` when controls are hidden).

---

## Behavior

- **Direction is fixed.** Items pack `side="left"` by default. There
  is no vertical orientation — use a [SideNav](../navigation/sidenav.md)
  for vertical chrome, or a `ButtonGroup(orient="vertical")` for a
  vertical action cluster.
- **Density and `button_variant` are read at `add_button()` time.**
  Reconfiguring `density` or `button_variant` after children exist
  affects only subsequent `add_button()` calls — existing buttons
  keep their original values.
- **Surface cascades to known builders.** `add_button()` and
  `add_label()` propagate the toolbar's surface to the child unless
  the call passes `surface=` explicitly. `add_widget()` widgets
  inherit surface through normal parent-surface inheritance (since
  they're parented to `toolbar.content`, which is itself parented
  to the toolbar).
- **Dragging.** When `draggable=True`, `<Button-1>` records the
  pointer position and `<B1-Motion>` repositions the toplevel
  through `geometry(f"+{x}+{y}")`. The bindings are added with
  `add="+"`, so they don't replace any existing button-1 handlers.
  Spacers and labels added through the builders also receive the
  drag bindings — buttons do not (their click handlers take
  precedence).
- **Maximize toggle.** The maximize button toggles
  `winfo_toplevel().state()` between `'zoomed'` and `'normal'` and
  swaps its own icon (`app` ↔ `copy`). `state('zoomed')` is
  Tk's Windows-canonical idiom; macOS accepts the call and visually
  zooms, but on some Linux WMs the call is a no-op. Test on your
  target platform if you ship a custom titlebar.
- **No selection state.** Toolbar holds actions, not a selection.
  No `signal=`, no `variable=`, no `value=` — wire each child's
  `command=` (or bind virtual events on the returned widget) to
  drive your handlers.

---

## Events

Toolbar emits no virtual events of its own. Reactivity lives on the
items:

- Buttons added via `add_button()` invoke their `command=` callback
  on click, exactly like a standalone [Button](../actions/button.md).
- Window control buttons invoke internal handlers
  (`_on_minimize` / `_on_maximize` / `_on_close`); reach the buttons
  through `toolbar.minimize_button` etc. and override their
  `command=` if you need custom behavior.
- For lower-level interactions (right-click, double-click, etc.),
  bind Tk events on the widget returned by the relevant builder.

```python
save = toolbar.add_button(icon="save", command=on_save)
save.bind("<Button-3>", on_save_context_menu)
```

---

## Patterns

### Custom titlebar with a frameless window

Toolbar is the standard ingredient for replacing the OS titlebar.
Construct an undecorated `App` (or `Toplevel`) and pack a Toolbar
with window controls at the top.

```python
import ttkbootstrap as ttk

app = ttk.App(override_redirect=True, size=(900, 600))

bar = ttk.Toolbar(app, show_window_controls=True, surface="chrome")
bar.pack(fill="x")
bar.add_button(icon="list")
bar.add_separator()
bar.add_label(text="My App", font="heading-md")
bar.add_spacer()
bar.add_button(icon="gear")

ttk.Frame(app).pack(fill="both", expand=True)

app.mainloop()
```

The same pattern works on a `Toplevel(overrideredirect=True)` for
secondary windows.

### Composing a menubar

Toolbar has no `add_menu()` builder; ttkbootstrap doesn't ship a
distinct `MenuBar` widget. Compose one by adding
[`MenuButton`](../actions/menubutton.md) (or
[`DropdownButton`](../actions/dropdownbutton.md)) instances via
`add_widget()`.

```python
file_menu = ttk.MenuButton(toolbar.content, text="File", menu=file_dropdown)
toolbar.add_widget(file_menu)

edit_menu = ttk.MenuButton(toolbar.content, text="Edit", menu=edit_dropdown)
toolbar.add_widget(edit_menu)
```

### Dynamic enable/disable

Builders return their widget, so capture the buttons that change
state and configure them later.

```python
save = toolbar.add_button(icon="save", text="Save", command=on_save)
save.configure(state="disabled")

document_dirty.subscribe(lambda dirty: save.configure(
    state="normal" if dirty else "disabled"
))
```

---

## When should I use Toolbar?

Use `Toolbar` when:

- you want a horizontal action strip at the top of a window or pane.
- you're building a custom titlebar with window controls.
- you need a host for mixed content — buttons, labels, separators,
  search inputs, custom widgets.

Prefer a different control when:

- the actions are a tightly connected cluster (Cut/Copy/Paste,
  Bold/Italic/Underline) → use [ButtonGroup](../actions/buttongroup.md)
  for the visual unit.
- you need vertical primary navigation → use
  [SideNav](../navigation/sidenav.md).
- you want tabs across the top → use [Tabs](../navigation/tabs.md)
  or [TabView](../views/tabview.md).
- you're building a full app shell with toolbar + sidebar + pages →
  use [AppShell](appshell.md), which constructs the toolbar for you.

---

## Related widgets

- [AppShell](appshell.md) — uses `Toolbar` as its top bar; the
  primary path most users take.
- [Button](../actions/button.md) — what `add_button()` returns;
  the standalone counterpart.
- [ButtonGroup](../actions/buttongroup.md) — connected cluster of
  buttons. Drop a `ButtonGroup` into a toolbar via `add_widget()`
  for a tight action segment.
- [MenuButton](../actions/menubutton.md),
  [DropdownButton](../actions/dropdownbutton.md) — what to drop in
  via `add_widget()` to compose a menubar.
- [SideNav](../navigation/sidenav.md) — the vertical counterpart
  for primary navigation chrome.

---

## Reference

- **API reference:** [`ttkbootstrap.Toolbar`](../../reference/widgets/Toolbar.md)
- **Related guides:**
    - [Toolbars](../../guides/toolbars.md) — composition recipes
    - [App Structure](../../guides/app-structure.md) — where Toolbar
      fits in a typical layout
    - [Design System → Surfaces](../../design-system/surfaces.md)
