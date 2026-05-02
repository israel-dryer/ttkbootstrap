# Tk vs ttk

Tkinter ships two parallel widget systems: **Tk** (the original, often
called "classic Tk") and **ttk** (Themed Tk). They look similar at the API
surface, but they style differently and serve different roles. This page
explains the distinction, names which of each ttkbootstrap actually
re-exports, and describes how the autostyle wrapper covers both.

---

## The two widget systems

Both systems live in `tkinter`:

- **Tk** (`tkinter`) — the original toolkit. Widgets are styled
  imperatively, by passing options like `bg=`, `fg=`, `font=`, and
  `relief=` directly to the constructor or to `configure(...)`. Each
  instance carries its own appearance.
- **ttk** (`tkinter.ttk`) — a themed layer added in Tk 8.5. Widgets are
  styled declaratively through *named styles* (e.g. `"TButton"`,
  `"primary.TButton"`). Appearance lives in a central style database; an
  individual widget references a style by name and otherwise has no
  appearance options.

ttk widgets render with the platform's native look on macOS and Windows
out of the box. Tk widgets render with Tk's own painted chrome, which
looks dated on every platform. That's the practical reason most modern
Tk applications — including ttkbootstrap — are ttk-first.

---

## What ttkbootstrap re-exports

After `import ttkbootstrap as ttk`, the `ttk` namespace mixes three
kinds of names:

**ttkbootstrap subclasses of ttk widgets.** These are the framework's
themed widgets — `ttk.Frame`, `ttk.Button`, `ttk.Entry`, `ttk.Notebook`,
`ttk.Treeview`, etc. They subclass `tkinter.ttk.X` and add the
`accent` / `variant` / `density` / `surface` styling tokens, mixin
behavior, and reactive signal channels.

```python
import ttkbootstrap as ttk
import tkinter.ttk as tkttk

ttk.Frame is tkttk.Frame      # False — ttkbootstrap subclass
ttk.Button is tkttk.Button    # False — ttkbootstrap subclass
ttk.Notebook is tkttk.Notebook  # False — ttkbootstrap subclass
```

**Re-exports of selected Tk widgets.** A handful of classic Tk widgets
have no ttk equivalent and ship as straight identity re-exports —
ttkbootstrap doesn't subclass them; it themes them at construction time
through the autostyle wrapper (next section).

```python
import ttkbootstrap as ttk
import tkinter as tk

ttk.Canvas is tk.Canvas    # True
ttk.Text is tk.Text        # True
ttk.Menu is tk.Menu        # True
ttk.TkFrame is tk.Frame    # True (TkFrame avoids the name clash with ttk.Frame)
hasattr(ttk, "Listbox")    # False — not re-exported; reach via tkinter.Listbox
```

**ttkbootstrap composites.** Higher-level widgets like `App`,
`AppShell`, `TextEntry`, `ListView`, `MessageDialog`, and `Tabs`. These
have no Tk or ttk counterpart — they're built out of one or both
primitives. See [Widgets](../widgets/index.md) for the full surface.

---

## The autostyle wrapper

When ttkbootstrap is imported, two install-time hooks register
constructor wrappers:

- `Bootstyle.override_ttk_widget_constructor` wraps every `ttk.X`
  constructor so it captures `accent` / `variant` / `density` / `surface`
  kwargs, resolves a style name from the registered builder, and sets the
  widget's `style=` to that resolved name.
- `Bootstyle.override_tk_widget_constructor` wraps a fixed list of
  classic Tk widgets so they pick up theme-aware colors at construction
  and re-style on `<<ThemeChanged>>`.

The Tk classes covered by the autostyle wrapper are: `Tk`, `Toplevel`,
`Frame`, `Label`, `Button`, `Entry`, `Text`, `Canvas`, `Checkbutton`,
`Radiobutton`, `Scale`, `Listbox`, `Menu`, `Menubutton`, `Labelframe`,
`Spinbox` (registered in `style/builders_tk/`). Constructing any of
those — even by reaching into `tkinter` directly — runs through the
wrapper:

```python
import tkinter as tk
import ttkbootstrap as ttk

app = ttk.App()
lst = tk.Listbox(app)              # autostyled — picks up theme colors
lst.cget("background")             # the resolved surface color
lst._surface                       # the captured surface token
```

The wrapper accepts two kwargs that gate its behavior:

- `autostyle=False` — skip the styling step entirely (still captures
  `_surface` for caller introspection, but doesn't set theme colors and
  doesn't subscribe to `<<ThemeChanged>>`).
- `inherit_surface=False` — don't pull `_surface` from the parent
  widget. Default is `True`, which means an explicit `surface=`
  argument is silently overridden by the parent's surface unless you
  also pass `inherit_surface=False`. (See the warning on
  [Text](../widgets/primitives/text.md) and
  [Canvas](../widgets/primitives/canvas.md).)

---

## Styling model differences

The two systems remain different even after autostyle:

| Concern | Tk widgets | ttk widgets |
|---|---|---|
| Where styles live | On the widget instance | In a central style database, keyed by name |
| How to recolor | `widget.configure(bg=..., fg=...)` | `style.configure("TButton", background=...)` (or change theme) |
| Per-widget overrides | Set the option on the widget | Define a new named style and assign it via `style="..."` |
| Themed by ttkbootstrap | Yes — colors set at construction, refreshed on theme change | Yes — `accent` / `variant` / `density` / `surface` resolve to a style name |
| Native look | No — Tk paints its own chrome | Yes — ttk uses native theming on macOS and Windows |

The most common trip-up: `ttk.Frame` does not accept `bg=` or
`background=`. The cross-platform way to recolor a ttk container is
`Frame(surface="card")` (or `accent="primary"` for container
classes — see [Styling Internals](ttk-styles-elements.md) for the
mechanics).

---

## When Tk widgets are the right choice

The classic Tk widgets ttkbootstrap re-exports cover the cases ttk
doesn't:

- **`Canvas`** — a drawing primitive. Backs `Meter`, `FloodGauge`, and
  any custom rendering. ttk has no canvas equivalent.
- **`Text`** — a multi-line text widget. Backs `ScrolledText`. ttk has
  no text equivalent.
- **`Menu`** — application menus, popup menus, and `tearoff` menus. ttk
  has no menu widget; menubars and context menus are always Tk.
- **`Listbox`** — a simple selection list (not re-exported at the top
  level; reach via `tkinter.Listbox`). ttkbootstrap's `ListView` is the
  data-bound replacement, but `Listbox` is still useful for small
  static lists.

For every other widget — buttons, frames, entries, tree views, tabbed
panes, scrollbars, spinboxes, progress bars — prefer the ttk version.
ttkbootstrap themes those through the style engine and exposes the
high-level styling tokens.

---

## Practical guidance

- Default to the ttkbootstrap `ttk.X` namespace for everything except
  Canvas, Text, Menu, and Listbox.
- Use the styling tokens (`accent`, `variant`, `density`, `surface`,
  `show_border`) instead of raw ttk style strings or Tk
  `bg=`/`fg=`/`font=` options. The tokens resolve correctly across
  themes; raw colors don't.
- When you do reach for a Tk widget, pass `surface=` explicitly with
  `inherit_surface=False` if you want a non-inherited background — the
  default inheritance silently overrides explicit values.
- Don't mix the two styling models on the same widget. Setting `bg=` on
  a ttk widget is rejected by Tcl; setting `style=` on a Tk widget is
  silently ignored.

---

## Next steps

- [Styling Internals](ttk-styles-elements.md) — what a "named style"
  actually is, how elements compose into a layout, and how
  ttkbootstrap's builders register styles at theme-load time.
- [Widget Lifecycle](widget-lifecycle.md) — how the autostyle wrapper
  fits into construction, restyle, and destruction.
- [Guides → Styling](../guides/styling.md) — recipes for customizing
  appearance.
