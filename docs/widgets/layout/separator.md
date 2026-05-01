---
title: Separator
---

# Separator

`Separator` is a thin themed wrapper over `ttk.Separator`. It draws a
1px (configurable) line across one axis, on a transparent background
that picks up the parent surface. Use it to split visually distinct
regions inside a layout — a divider between a toolbar and a content
pane, between sections of a settings panel, or between groups inside
a sidebar.

`Separator` is purely structural: it has no focus, no mouse or
keyboard interactions, and no virtual events. Geometry is decided by
the caller; you stretch it with `fill="x"` (horizontal) or
`fill="y"` (vertical) on the geometry manager, or pin a fixed
dimension with `length=`.

<figure markdown>
![separator](../../assets/dark/widgets-separator.png#only-dark)
![separator](../../assets/light/widgets-separator.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Label(app, text="Section A").pack(anchor="w", padx=20, pady=(20, 8))
ttk.Separator(app, orient="horizontal").pack(fill="x", padx=20)
ttk.Label(app, text="Section B").pack(anchor="w", padx=20, pady=(8, 20))

app.mainloop()
```

For a vertical divider — typical between a side rail and the main
content — use `orient="vertical"` and `fill="y"`:

```python
sep = ttk.Separator(app, orient="vertical")
sep.pack(side="left", fill="y", padx=8, pady=8)
```

---

## Common options

`Separator`'s configuration surface is small. The line color is
`accent`, the background fill is `surface`, and the line dimensions
are `thickness` (cross-axis) and `length` (along-axis, optional).
Orientation is locked at construction time.

| Option       | Type        | Default        | Notes                                                          |
| ------------ | ----------- | -------------- | -------------------------------------------------------------- |
| `orient`     | str         | `"horizontal"` | `"horizontal"` or `"vertical"`. Construction-time only — see Behavior |
| `accent`     | str         | `"border"`     | Line color. Default resolves to the surface's border color (muted) |
| `surface`    | str         | inherited      | Background fill behind the line; inherits from the parent if unset |
| `thickness`  | int         | `1`            | Line width in pixels along the cross axis                      |
| `length`     | int \| None | `None`         | Pinned dimension along the orient axis. `None` → stretches with the geometry manager |
| `variant`    | str         | `"default"`    | Only `"default"` is registered; other values raise `BootstyleBuilderError` |
| `style`      | str         | derived        | Explicit ttk style name; overrides `accent` / `surface` / `thickness` / `length` |
| `bootstyle`  | str         | —              | **Deprecated.** Use `accent` instead                            |

### `accent` — line color

```python
ttk.Separator(app, accent="primary").pack(fill="x")
ttk.Separator(app, accent="secondary").pack(fill="x")
```

The default `accent="border"` resolves through the style builder to
`b.border(surface)`, the same muted border color a `Frame(show_border=True)`
draws — so a vanilla separator is intentionally low-contrast and reads
as a section break, not a hard rule.

To pull a separator forward, give it an explicit accent:
`primary`, `success`, `warning`, `danger`, or any other accent token
defined by the active theme.

### `surface` — background fill

```python
section = ttk.Frame(app, surface="card")
ttk.Separator(section).pack(fill="x")
```

`surface` is the fill color *behind* the line. By default it inherits
from the parent (a separator inside a `surface="card"` frame picks
up `card`), so the line appears to sit flush on the container. Set
it explicitly when you need to break that inheritance.

### `thickness` and `length`

```python
ttk.Separator(app, thickness=2).pack(fill="x")               # 2px line, full width
ttk.Separator(app, thickness=4, length=200, orient="horizontal").pack()  # 4px × 200px
```

`thickness` widens the line on its cross axis; `length` pins the
along-axis size. Without `length`, the underlying ttk image element
stretches with the geometry manager (so a horizontal separator
packed with `fill="x"` spans the parent's width). With `length` set,
the image element is built at exactly that size and ignores
geometry-manager fill on that axis.

---

## Behavior

**Non-interactive.** `Separator` does not take focus (Tk's `takefocus`
auto-mode evaluates as non-focusable for ttk.Separator), does not
respond to clicks or keyboard input, and emits no virtual events.
It's a purely visual primitive.

**Stretching vs pinning.** The `default` variant uses an image element
with `sticky="ew"` (horizontal) or `sticky="ns"` (vertical), so an
unsized separator stretches with the geometry manager. Setting
`length=N` builds the image at fixed dimensions, which is useful for
short separators inside a flex container where you don't want the
divider to grow.

**Reconfiguring `orient` after construction is not supported.**
`Separator` participates in `ORIENT_CLASSES`, so the resolved ttk
style name embeds the orientation as a prefix (e.g.
`bs[…].primary.Vertical.TSeparator`). The bootstyle wrapper resolves
that style once at construction time;
`separator.configure(orient="horizontal")` writes the Tk option but
does *not* rebuild the style, leaving the widget rendering with the
wrong axis. Treat `orient` as construction-time only and rebuild the
widget if you need to change orientation.

**Geometry-manager pairing.** The natural usages are
`pack(fill="x")` for a horizontal divider in a vertically-stacked
column, `pack(side="left", fill="y")` for a vertical divider between
two side-by-side regions, and `grid(sticky="ew")` /
`grid(sticky="ns")` for grid-based layouts. A separator with
neither `fill` nor `length` set will collapse to its 40-pixel
internal default — usually not what you want.

---

## Events

`Separator` has no `on_*` event helpers and emits no virtual events.
The only event it participates in is the standard Tk `<Configure>`
notification fired on resize:

```python
def on_resize(event):
    print(event.width, event.height)

separator.bind("<Configure>", on_resize)
```

Since separators don't host children, `<Configure>` is rarely useful
in practice — bind it on the parent container instead.

---

## When should I use Separator?

Use `Separator` when:

- whitespace and alignment alone aren't enough to communicate a
  region break (sections of a settings panel, header / content
  / footer split, groups inside a sidebar)
- you want a vertical divider between a side rail and the main
  content area
- you want a thin, theme-aware divider that adapts to the parent
  surface and the active light/dark mode without manual styling

Prefer **PanedWindow** when the divider needs to be draggable —
`Separator` is fixed. Prefer **Frame(show_border=True)** when the
goal is to outline a region rather than divide two regions: a
bordered card frames its content; a separator splits the space
around it. Prefer plain padding and font weight when the visual
hierarchy already reads clearly without a line.

---

## Related widgets

- **Frame** — themed container; pair with `Separator` to divide
  sections inside the frame
- **LabelFrame** — labeled bordered container; communicates grouping
  with a title rather than a divider line
- **PanedWindow** — draggable divider between resizable panes
- **Sizegrip** — bottom-right resize affordance, the other
  non-interactive primitive in the layout family

---

## Reference

- **API reference:** [`ttkbootstrap.Separator`](../../reference/widgets/Separator.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
