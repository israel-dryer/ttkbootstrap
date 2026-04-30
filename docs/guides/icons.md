---
title: Icons
---

# Icons

This guide is the practical reference for using icons in a ttkbootstrap
application: how to attach an icon to a widget, when to use the dict form for
extra control, and how state-based icon overrides work.

For the resolution pipeline (providers, caching, DPI rasterization, theme
recoloring) see [Capabilities → Icons](../capabilities/icons/icons.md). This
guide assumes that pipeline and focuses on what application code does with it.

---

## The mental model

Icons are **named resources**, not file paths. You pass a name; the framework
resolves, recolors, scales, and caches the rendered image.

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Button(app, text="Settings", icon="gear").pack(padx=20, pady=20)

app.mainloop()
```

The same name (`"gear"`) renders correctly in light and dark themes, on
standard and high-DPI displays, in the right size for the widget, and in the
right colour for its current state — without your code doing anything.

Think of icons the way you think of color tokens:

| Concept | You write | Framework resolves |
|---------|-----------|-------------------|
| Color | `accent="danger"` | theme-appropriate red |
| Icon | `icon="trash"` | themed, scaled, cached image |

Application code stays semantic; the system handles rendering.

---

## Attaching an icon to a widget

Most widgets that show text — buttons, labels, menu items — also accept
`icon=`:

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Button(app, text="Save", icon="check").pack(padx=10, pady=4)
ttk.Button(app, text="Delete", icon="trash", accent="danger").pack(padx=10, pady=4)
ttk.Label(app, text="Unsaved changes", icon="exclamation-triangle").pack(padx=10, pady=4)

app.mainloop()
```

The icon appears to the left of the text. The label widget treats it
decoratively; on a button the icon and text together form the click target.

### Icon-only widgets

When the icon alone communicates the action (close, refresh, settings), pass
`icon_only=True` so the widget removes the padding reserved for text:

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Button(app, icon="plus", icon_only=True).pack(side="left", padx=4, pady=20)
ttk.Button(app, icon="x-lg", icon_only=True, accent="secondary").pack(side="left", padx=4, pady=20)

app.mainloop()
```

Reserve icon-only for symbols that are universally recognized (close,
minimize, search, plus). Anything ambiguous should keep its label.

---

## The dict form: when you need control

A string is enough for most uses. When you need to override size, color, or
provide per-state overrides, pass a dict instead:

```python
ttk.Button(app, text="Settings", icon={"name": "gear", "size": 18})
```

Available keys:

| Key | Purpose |
|-----|---------|
| `name` | Icon identifier (required) |
| `size` | Size in pixels (default: derived from widget; DPI-scaled) |
| `color` | Override color (hex string or theme token) |
| `state` | Per-state icon overrides (list of `(state_expr, override)` tuples) |

Examples:

```python
import ttkbootstrap as ttk

app = ttk.App()

# Larger than default
ttk.Button(app, text="Big", icon={"name": "star", "size": 24}).pack()

# Pinned color (rarely needed — let the theme decide)
ttk.Button(app, text="Tinted", icon={"name": "heart", "color": "#ff0066"}).pack()

app.mainloop()
```

Setting an explicit `color` opts out of theme-driven recolouring, so the icon
keeps that color across light and dark themes. Use it sparingly — usually the
default (derived from the widget's foreground) is what you want.

---

## State-based icon overrides

Some widgets show different visuals in different states. Use the `state` key
to swap the icon (or its color) when the widget enters that state:

```python
import ttkbootstrap as ttk

app = ttk.App()

# Outline bell when off, filled bell when on
ttk.CheckToggle(
    app,
    text="Notifications",
    icon={
        "name": "bell-slash",
        "state": [
            ("selected", {"name": "bell-fill"}),
        ],
    },
).pack(padx=20, pady=20)

app.mainloop()
```

Each entry is `(state_expression, override)`, where the override is itself a
dict that may set `name`, `color`, or both. State expressions follow Tk's
ttk-style conventions:

| Expression | Meaning |
|------------|---------|
| `"selected"` | Widget is selected or checked |
| `"disabled"` | Widget is disabled |
| `"hover !disabled"` | Mouse over, not disabled |
| `"pressed !disabled"` | Being clicked |
| `"focus !disabled"` | Has keyboard focus |

Order matters — the first matching expression wins, so list the most specific
states first. Use the unprefixed bare-name form for the base appearance and
state entries to override it:

```python
ttk.Button(app, text="Play", icon={
    "name": "play",
    "state": [
        ("pressed !disabled", {"name": "play-fill"}),
        ("hover !disabled", {"name": "play-fill"}),
    ],
})
```

---

## Patterns

### Toolbar of icon-only buttons

Toolbars are the canonical icon-only context: small, dense, repeated controls
where the icon is the affordance.

```python
import ttkbootstrap as ttk

app = ttk.App()

toolbar = ttk.PackFrame(app, direction="horizontal", gap=4, padding=8)
toolbar.pack(fill="x")

for name in ("folder2-open", "save", "printer", "scissors", "clipboard"):
    ttk.Button(toolbar, icon=name, icon_only=True).pack(side="left")

app.mainloop()
```

### Reinforcing meaning with color

A semantic accent paired with a literal icon makes the intent unambiguous:

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Button(app, text="Delete", icon="trash", accent="danger").pack(pady=4)
ttk.Button(app, text="Confirm", icon="check-circle", accent="success").pack(pady=4)
ttk.Label(app, text="Connection lost", icon="wifi-off", accent="warning").pack(pady=4)

app.mainloop()
```

### Context menu items

`ContextMenu.add_command` accepts an `icon=` argument the same way buttons
do:

```python
import ttkbootstrap as ttk
from ttkbootstrap import ContextMenu

app = ttk.App()

menu = ContextMenu(app)
menu.add_command(text="Cut", icon="scissors", shortcut="Ctrl+X")
menu.add_command(text="Copy", icon="copy", shortcut="Ctrl+C")
menu.add_command(text="Paste", icon="clipboard", shortcut="Ctrl+V")
menu.add_separator()
menu.add_command(text="Delete", icon="trash")

app.mainloop()
```

When the underlying `tk.Menu` is constructed via the framework's declarative
helpers (e.g. `create_menu`), the same `icon=` key is honored on each item
dict.

---

## Icons and themes

Icon color is derived from the active theme's foreground unless you override
it. When the theme switches, every icon recolours automatically — no caches
to invalidate, no per-widget refresh code.

If you set `color` explicitly in an icon spec (a hex string, or a token like
`"primary"`), that becomes a hard pin: the icon keeps that color across theme
changes. That's the right behavior for branded marks but the wrong behavior
for typical UI icons; default to leaving `color` unset.

---

## Icons and localization

Icons reinforce meaning, but they don't translate. For localized applications:

- **Pair icons with translated labels** wherever the action is non-universal
  ("Settings", "Reports", "Profile" — words help in any language).
- **Reserve icon-only for universally recognized symbols** — close,
  minimize, plus, search, play.
- **Test icon meaning across cultures**. Some symbols read differently
  outside their origin context (e.g. mailboxes, hand gestures).

See [Localization](localization.md) for translation patterns.

---

## Anti-patterns

ttkbootstrap's icon system exists so you don't manage these concerns by hand.
Don't reach for them.

| Don't | Why |
|-------|-----|
| Pass file paths to `icon=` | Bypasses theming, scaling, caching |
| Maintain `light/` and `dark/` icon folders | Icons recolour automatically |
| Use `PhotoImage` and resize manually | DPI scaling is automatic |
| Hardcode colours unless intentional | Foreground is theme-driven |
| Recolour images per state by hand | Use the `state` key |

---

## Related guides

- [Capabilities → Icons](../capabilities/icons/icons.md) — provider
  resolution, state integration, DPI pipeline, and caching.
- [Design System → Icons](../design-system/icons.md) — icon vocabulary and
  intent.
- [Styling](styling.md) — color tokens and accent semantics.
- [Theming](theming.md) — theme switching and color derivation.
- [Localization](localization.md) — pairing icons with translated text.
