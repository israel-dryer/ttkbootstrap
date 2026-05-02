# Styling Internals

Every ttkbootstrap widget that renders through ttk does so by referring
to a **named style**. The style determines colors, borders, padding,
state-dependent visuals, and the element tree that draws the widget.
ttkbootstrap doesn't replace this system — it generates style names
programmatically from a token model (`accent`, `variant`, `density`,
`surface`) and registers builders that populate the style database at
theme-load time and on every `<<ThemeChanged>>`.

This page covers how the model works underneath: the resolved style
name, the four token axes, the two routing rules (container classes
and orient classes), the element / layout / state-map vocabulary, and
how to read or override styles when you need to.

For the high-level "which token does what" reference, see
[Design System → Variants](../design-system/variants.md). For
hands-on theming, see [Guides → Styling](../guides/styling.md).

---

## Resolved style names

When you construct a ttkbootstrap ttk widget, the bootstyle
constructor wrapper resolves a concrete ttk style name from your
token kwargs and writes it into the widget's `style=` option. You can
read it back with `widget.cget("style")`:

```python
import ttkbootstrap as ttk

app = ttk.App()
ttk.Button(app, text="A").cget("style")
# 'bs[99914b93].Solid.TButton'

ttk.Button(app, text="B", accent="success").cget("style")
# 'bs[99914b93].success.Solid.TButton'

ttk.Button(app, text="C", accent="success", variant="outline").cget("style")
# 'bs[99914b93].success.Outline.TButton'

ttk.Button(app, text="D", density="compact").cget("style")
# 'bs[f2b6cdd3].Solid.TButton'   ← different hash; density changed style_options

ttk.Frame(app, accent="primary").cget("style")
# 'bs[7c2c2c13].primary.TFrame'  ← container reroute (next section)

ttk.Scrollbar(app, orient="vertical", accent="success").cget("style")
# 'bs[0e95f40a].success.Vertical.TScrollbar'  ← orient reroute (next section)
```

The shape is:

```
bs[<hash>].<accent?>.<orient?>.<variant?>.T<Class>
```

| Segment | Meaning |
|---|---|
| `bs[<hash>]` | A short hash of the widget's `style_options` dict (`density`, `show_border`, `thickness`, etc.). Two widgets with the same accent/variant but different density get different hashes — and therefore different styles in Tk's database. |
| `<accent>` | The `accent` token, lowercase (`primary`, `success`, `info`, ...). Omitted when no accent is set. |
| `<orient>` | `Vertical` or `Horizontal`, present only for orient classes (next section). |
| `<variant>` | The variant builder's name (`Solid`, `Outline`, `Ghost`, `Link`, ...). The default builder for a class is its registered default; for buttons that's `Solid`. |
| `T<Class>` | The ttk class name (`TButton`, `TFrame`, `TEntry`, etc.). Always last. |

You don't construct these names yourself. The bootstyle wrapper does
it; the corresponding builder under `style/builders/` populates the
style with colors and layout entries before the widget renders.

---

## The token axes

The four high-level styling kwargs map to specific positions in the
resolved style name:

| Token | Type | Maps to | Examples |
|---|---|---|---|
| `accent` | semantic color name | a segment of the style name | `"primary"`, `"success"`, `"danger"`, `"info"`, `"warning"`, custom theme tokens |
| `variant` | visual variant | a segment of the style name | `"solid"`, `"outline"`, `"ghost"`, `"link"`, `"text"`, `"pill"` (per widget) |
| `density` | spacing scale | the `style_options` hash | `"default"`, `"compact"` |
| `surface` | parent surface token | the `style_options` hash + theme color lookup | `"content"`, `"chrome"`, `"card"`, `"primary"`, ... |

Two more options participate in the hash but aren't full axes:

- `show_border` — adds a 1-px border on container widgets.
- `thickness` (Separator), `arc_range` / `arc_offset` (Meter), and
  similar widget-specific knobs.

---

## Two routing rules

**Container classes** (`TFrame`, `TLabelframe`) treat `accent` as a
shortcut for `surface`. Setting `accent="primary"` on a Frame doesn't
add a `.primary.` segment to the style name — instead the wrapper
captures `surface="primary"` and the resolved name reflects that:

```python
ttk.Frame(app, accent="primary").cget("style")
# 'bs[...].primary.TFrame'
```

The set of container classes is fixed and small:

```python
# style/token_maps.py
CONTAINER_CLASSES = {"TFrame", "TLabelframe"}
```

**Orient classes** (`TProgressbar`, `TScale`, `TScrollbar`,
`TPanedwindow`, `TSeparator`) include orientation in the style name.
A horizontal Scrollbar and a vertical Scrollbar resolve to *different*
styles, because the layout (element ordering, image elements) differs:

```python
# style/token_maps.py
ORIENT_CLASSES = {"TProgressbar", "TScale", "TScrollbar",
                  "TPanedwindow", "TSeparator"}
```

This is also why reconfiguring `orient` after construction does not
restyle the widget — the cached `style=` string would need to be
rebuilt, and the framework's current configure delegates don't do
that. Treat `orient` as construction-time-only (see the bugs list
entries for Scrollbar and Separator).

---

## Elements, layouts, and the style database

Underneath the style name is the **style database**, accessible
through `tkinter.ttk.Style`. The database stores:

- **Layouts** — how a style composes its elements into a tree.
- **Configurations** — option values (background, foreground,
  padding, font, ...) that apply at the style level.
- **Maps** — option values that vary by widget state (`active`,
  `disabled`, `pressed`, `focus`, `selected`, etc.).

You can inspect any style:

```python
from tkinter import ttk

s = ttk.Style()
s.layout("TButton")
# [('Button.border',
#   {'sticky': 'nswe', 'border': '1',
#    'children': [('Button.focus',
#                  {'sticky': 'nswe',
#                   'children': [('Button.padding',
#                                 {'sticky': 'nswe',
#                                  'children': [('Button.label',
#                                                {'sticky': 'nswe'})]})]})]})]
```

That tree describes a Button as a `border` element wrapping a `focus`
ring, wrapping `padding`, wrapping a `label`. Each name (e.g.
`Button.border`) is a registered ttk **element** — image data plus
layout hints contributed by the active theme.

The other two introspection calls:

```python
s.lookup("Solid.TButton", "background")           # → '#0d6efd' or similar
s.lookup("Solid.TButton", "foreground", ["disabled"])
# → the foreground color in the disabled state
```

`lookup` traverses style inheritance (`Solid.TButton` → `TButton` →
`.`) just as widgets do, returning the first match.

---

## State maps

Most state-dependent visuals are expressed as `[(state, value), ...]`
lists registered with `Style.map`:

```python
s.map(
    "Solid.TButton",
    background=[
        ("pressed", "#0a58ca"),
        ("active", "#0b5ed7"),
    ],
    foreground=[("disabled", "#999")],
)
```

When the widget enters the named state (via `widget.state(["active"])`,
the Tcl class binding for hover, etc.), Tk looks up the option's map
and uses the matching value. State names can be combined
(`"!disabled active"` matches "active and not disabled").

This is how `accent` produces meaningfully-different visuals across
the seven user-visible states — the framework's builders register
the right colors per state when they populate the style.

---

## How ttkbootstrap registers styles

A *builder* is a function that populates a style. ttkbootstrap registers
one per (class, variant) pair under `src/ttkbootstrap/style/builders/`:

```python
# excerpt — style/builders/button.py
@BootstyleBuilder.register_builder("solid", "TButton")
def solid(name, options):
    style = ttk.Style()
    accent = options.get("accent", "primary")
    surface = options.get("surface", "content")
    # ... compute fg/bg from accent + theme ...
    style.configure(name, background=bg, foreground=fg, padding=pad)
    style.map(name, background=[("pressed", ...), ("active", ...)])
```

When a widget is constructed, the bootstyle wrapper:

1. computes the resolved name (`bs[hash].accent.Variant.TClass`),
2. looks up the registered builder for `(class, variant)`,
3. calls the builder with `(name, options)` to populate the style,
4. sets `widget.style = name`.

The same builder runs again on `<<ThemeChanged>>` for every registered
widget — that's why theme switching repaints instantly.

Themes ship under `src/ttkbootstrap/style/theme_provider.py` as
collections of color tokens. A builder reads the *current* theme's
tokens at the moment it runs, so the same style produces different
colors in different themes without any per-widget bookkeeping.

---

## When to reach for raw ttk styles

The token model covers virtually every "style this widget" need. You
should drop down to raw `ttk.Style().configure(...)` only in two
situations:

- **A one-off cosmetic tweak** the framework doesn't expose — for
  example, restyling a single Treeview row's tag color via
  `tag_configure`. Stay inside that one widget; don't reach across
  the framework's styles.
- **A custom widget** you're building outside the framework. Register
  your own builder via `BootstyleBuilder.register_builder` so the
  widget participates in theme switching automatically.

Configuring an existing framework style directly (for example,
`style.configure("Solid.TButton", background="red")`) works
*momentarily* — but the next `<<ThemeChanged>>` (including theme
switches and any framework-internal repaint trigger) re-runs the
builder and overwrites your changes. If you need a persistent
override, register your own variant.

---

## Inspecting a widget's style at runtime

Three calls cover most debugging needs:

```python
widget.cget("style")              # the resolved ttk style name
widget.winfo_class()              # the ttk class (e.g. 'TButton')
widget.state()                    # current state flags
```

Combined with `ttk.Style().layout(name)` and
`ttk.Style().lookup(name, option, state)`, you can answer:

- "Which style is this widget on?"
- "What colors does that style produce in the current theme?"
- "How does the style change when the user hovers?"

For ttkbootstrap-specific debugging, the captured token attributes
are:

| Attribute | What it stores |
|---|---|
| `widget._accent` | The accent token passed to the constructor (or default) |
| `widget._variant` | The variant token |
| `widget._density` | The density token |
| `widget._surface` | The surface token (captured from parent on Tk-class widgets unless `inherit_surface=False`) |
| `widget._style_options` | The dict that gets hashed into `bs[<hash>]` |

These are not part of the public API but they're stable across the v2
codebase and useful when answering "why is this widget's style
key the way it is?".

---

## Common pitfalls

**Treating `accent` as a foreground color.** It isn't directly. The
builder maps `accent` to *meaningful* colors per widget — for Button
it's the fill; for Badge it's the chip background; for Label it's
the text color. The token expresses *intent*; the builder decides
the rendering.

**Reconfiguring `orient`.** Construction-time only. The cached style
name doesn't get rebuilt; the widget keeps painting in its original
orientation. Tracked in the bugs list for Scrollbar / Separator.

**`widget.configure(background="red")` on a ttk widget.** Most ttk
widgets reject `background` outright — Tcl raises `TclError: unknown
option`. Use the surface token (`surface="..."`), or define your own
variant if you need a non-tokenized color.

**Modifying `Solid.TButton` directly.** Survives until the next
theme change, then gets overwritten. Register a custom variant
instead.

**Cross-class style sharing.** The resolved style name is class-
scoped (`TButton` ≠ `TLabel`); you can't tell a Label to "use
that Button's style." If you need shared colors, use a shared
accent token.

---

## Next steps

- [Design System → Variants](../design-system/variants.md) — the
  user-visible token vocabulary.
- [Design System → Colors](../design-system/colors.md) — what
  semantic colors actually mean.
- [Guides → Styling](../guides/styling.md) — recipes for customizing
  appearance without dropping to raw ttk.
- [Tk vs ttk](tk-vs-ttk.md) — the broader picture of how ttk relates
  to classic Tk and the autostyle wrapper.
