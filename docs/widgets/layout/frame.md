---
title: Frame
---

# Frame

`Frame` is a themed container for grouping child widgets and applying
shared surface, border, and input-fill tokens to a region of the UI.
It's a thin wrapper over `ttk.Frame` that participates in the
ttkbootstrap design system: surface tokens cascade to descendants,
borders pick up theme-aware stroke colors, and input children inside
the frame can be fill-coordinated with one option.

`Frame` does not manage child placement automatically — you call
`pack()`, `grid()`, or `place()` on each child yourself. For
self-managing layouts, see [PackFrame](packframe.md) (axis stacks
with gaps) or [GridFrame](gridframe.md) (CSS-Grid-style 2D layouts);
both subclass `Frame` and inherit the same theming surface.

<figure markdown>
![frame](../../assets/dark/widgets-frame.png#only-dark)
![frame](../../assets/light/widgets-frame.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

section = ttk.Frame(app, padding=20)
section.pack(fill="both", expand=True)

ttk.Label(section, text="Account").pack(anchor="w")
ttk.Entry(section).pack(fill="x", pady=(8, 0))

app.mainloop()
```

---

## Common options

`Frame`'s style surface is small and deliberately distinct from the
input/action widgets. The tokens that *do* affect rendering are
`surface`, `show_border`, and `input_background`. The tokens that
*do not* are `accent` and `variant` — they're accepted by the
constructor for API uniformity but silently ignored by the Frame
style builder.

| Option              | Type                | Default        | Notes                                                   |
| ------------------- | ------------------- | -------------- | ------------------------------------------------------- |
| `padding`           | int \| tuple        | `0`            | Inner spacing; `(left, top)` or `(l, t, r, b)` accepted |
| `width`             | int                 | natural        | Requested width in pixels (see propagation note)        |
| `height`            | int                 | natural        | Requested height in pixels (see propagation note)       |
| `surface`           | str                 | `"background"` | Surface token: `chrome`, `content`, `card`, `overlay`, `input` |
| `show_border`       | bool                | `False`        | Draws a 1px theme-aware border around the frame         |
| `input_background`  | str                 | `"content"`    | Surface token cascaded to input descendants             |
| `style`             | str                 | `"TFrame"`     | Explicit ttk style name; overrides theme-token styling  |
| `accent`            | str                 | —              | Accepted but **silently ignored** by the Frame builder  |
| `variant`           | str                 | —              | Accepted but **silently ignored** by the Frame builder  |

### Surface tokens

```python
ttk.Frame(app, surface="card")        # raised card-like region
ttk.Frame(app, surface="chrome")      # toolbar / header strip
ttk.Frame(app, surface="overlay")     # dialog-style fill
```

`surface` is the canonical knob for region color. Available tokens
are defined in the active theme; the built-in palette ships
`chrome`, `content`, `card`, `overlay`, and `input`. For a colored
fill outside the surface palette, set `style=` to a custom-built
ttk style name.

### Borders

```python
ttk.Frame(app, surface="card", show_border=True, padding=12)
```

`show_border` draws a 1px stroke in the theme's `stroke` color
around the frame. Combine with `surface` and `padding` to get
card-style chrome without any custom styling.

### `input_background`

```python
form = ttk.Frame(app, surface="card", input_background="content")
ttk.Entry(form).pack(...)   # fills with the "content" surface,
                            # not the parent "card" surface
```

`input_background` is unique to `Frame` (and its subclasses): it
cascades to every input descendant — `Entry`, `Combobox`, `Spinbox`,
`Field` — so they share a fill independent of the container's
surface. Foreground, border, and focus-ring colors derive from the
chosen fill so contrast is correct automatically.

The default is `"content"` (the app background), which keeps inputs
visually distinct on a `card` or `chrome` container. Override to
`"card"` (or another surface) when you want inputs to flush with
the container.

---

## Behavior

`Frame` is a non-interactive structural widget. It does not respond
to clicks, take keyboard focus by default, or emit any virtual
events; its responsibilities are visual surfacing and child
hosting.

**Geometry propagation.** Like `ttk.Frame`, a `Frame` sizes itself
to its content unless you disable propagation explicitly. The two
toggles are inherited from Tk:

```python
pane = ttk.Frame(app, width=240, height=400)
pane.pack(side="left")
pane.pack_propagate(False)   # honor width/height instead of children
```

Without `pack_propagate(False)` (or `grid_propagate(False)` if you
use grid), the explicit `width=`/`height=` are treated as natural-size
*hints* and are overridden by child requests.

**Surface cascade.** When `surface` (or `input_background`) is
reconfigured at runtime, the change is propagated to descendants
that haven't set their own surface explicitly. Children that
inherited from the old surface re-style; children that were
configured with their own `surface=` are left alone. This is
the runtime hook behind regional theming — set the token on a
container, and the region rebuilds itself.

```python
section = ttk.Frame(app, surface="content")
ttk.Label(section, text="…").pack()
ttk.Entry(section).pack()

section.configure(surface="card")  # Label and Entry restyle
```

---

## Events

`Frame` has no `on_*` event helpers and emits no virtual events.
The only event it participates in is the standard Tk `<Configure>`
notification fired on resize:

```python
def on_resize(event):
    print(event.width, event.height)

frame.bind("<Configure>", on_resize)
```

If you need to react to layout changes elsewhere in your UI, bind
to the relevant child widgets directly — `Frame` is purely a
container surface.

---

## When should I use Frame?

Use `Frame` when:

- you want a themed container with `surface` / `show_border` /
  `input_background` tokens and are willing to call `pack()` /
  `grid()` on each child manually
- you need a parent that cascades a surface or input-fill token to
  a region of the UI
- you're building an ad-hoc layout that doesn't fit the rigid
  PackFrame / GridFrame patterns

Prefer **PackFrame** when you want a single-axis stack of children
with consistent gap spacing. Prefer **GridFrame** when you want a
named-column 2D grid with auto-placement. Prefer **LabelFrame**
when the region needs a visible title.

---

## Related widgets

- **PackFrame** — `Frame` subclass with auto-pack of children along
  one axis, plus `gap` spacing
- **GridFrame** — `Frame` subclass with CSS-Grid-style declarative
  rows/columns and auto-placement
- **LabelFrame** — titled bordered container for labelled groups
- **Card** — opinionated `Frame` preset with header/body/footer
  slots
- **Separator** — visual divider for regions inside a `Frame`
- **PanedWindow** — resizable split regions when users need to
  adjust panel sizes

---

## Reference

- **API reference:** [`ttkbootstrap.Frame`](../../reference/widgets/Frame.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
